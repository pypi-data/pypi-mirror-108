import time
from datetime import datetime
import pyspark.sql.functions as F


class MobilitySummary:

    def __init__(self, delta_loc, adm_col, quality_filter=6, spark=None):
        self.sjr = spark.read.format('delta').option("header", "true").load(delta_loc)
        self.adm_col = adm_col
        self.quality_filter = quality_filter

    @staticmethod
    def quality_control_filter(sdf, records):
        # filter out the IDs which have less than "records" number of records
        d = sdf.groupby('device_id').count().where(F.col('count') >= records)
        sdf = sdf.join(d, on=["device_id"], how="inner")
        return sdf

    @staticmethod
    def extract(sdf, from_date, to_date):
        from_t = time.mktime(datetime.strptime(from_date, "%Y/%m/%d").timetuple())
        to_t = time.mktime(datetime.strptime(to_date, "%Y/%m/%d").timetuple())

        timestamps_t = (from_t, to_t)
        mobility_t = sdf.where(F.col('timestamp').between(*timestamps_t))

        return mobility_t

    @staticmethod
    def get_device_homes(sdf, admin):
        device_admin_counts = sdf.groupby("device_id", admin).count()

        result = device_admin_counts.groupBy('device_id').agg(
            F.max(
                F.struct(F.col('count'), F.col(admin))
            ).alias('max')).select(F.col('device_id'), F.col('max.{}'.format(admin)))
        return result

    def _get_records_per_admin(self, adm_col):
        mobility_record_count = self.sjr.groupBy(adm_col).count()
        mobility_record_count = mobility_record_count.withColumnRenamed("count", "frequency")
        return mobility_record_count

    def _get_devices_per_admin(self, adm_col, from_date, to_date):
        self.sjr = self.extract(self.sjr, from_date, to_date)

        if self.quality_filter > 0:
            self.sjr = self.quality_control_filter(self.sjr, self.quality_filter)

        self.sjr = self.get_device_homes(self.sjr, adm_col)

        mobility_device_count = self.sjr.groupBy(adm_col).agg(F.countDistinct("device_id")) \
            .withColumnRenamed("count(device_id)", "unique_devices")

        return mobility_device_count

    def _get_records_per_date_admin(self, adm_col):
        sjr_with_date = self.sjr.withColumn("date", F.from_unixtime("timestamp", format="yyyy_MM_dd"))
        mobility_record_date_count = sjr_with_date.groupBy(adm_col, 'date').count().withColumnRenamed("count",
                                                                                                      "num_records")
        return mobility_record_date_count

    def _get_devices_per_date_admin(self, adm_col):
        sjr_with_date = self.sjr.withColumn("date", F.from_unixtime("timestamp", format="yyyy_MM_dd"))
        mobility_device_date_count = sjr_with_date.groupBy(adm_col, 'date').agg(
            F.countDistinct("device_id")
        ).withColumnRenamed("count(DISTINCT device_id)", "unique_devices")
        return mobility_device_date_count

    def get_records_per_admin(self):
        return self._get_records_per_admin(self.adm_col)

    def get_records_per_date_admin(self):
        return self._get_records_per_date_admin(self.adm_col)

    def get_devices_per_admin(self, from_date, to_date):
        """
        :param from_date: starting date from which the data is to be taken; dtype: str; format: YYYY/MM/DD; example: '2019/01/01'
        :param to_date: ending date up to which the date is to be taken; dtype: str; format: YYYY/MM/DD; example: '2020/01/01'
        :return: spark dataframe having devices per administrative area in the given date range
        """
        return self._get_devices_per_admin(self.adm_col, from_date, to_date)

    def get_devices_per_date_admin(self):
        return self._get_devices_per_date_admin(self.adm_col)

    def get_frequency_map(self):
        frequency_table = self.sjr.groupBy('device_id') \
            .count() \
            .withColumnRenamed("count", "frequency") \
            .groupBy('frequency') \
            .count() \
            .orderBy(F.asc("frequency"))
        return frequency_table