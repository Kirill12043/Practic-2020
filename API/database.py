from influxdb import InfluxDBClient


class DataBaseConfig:
    def __init__(self):
        self.database_address = 'localhost'
        self.database_name = 'tsdb'
        self.database_measure_name = 'measurement_tsdb'
        self.database_epoch = "s"


class DataBaseConnector:
    def __init__(self):
        self._db_a = ''
        self._db_n = ''
        self._db_m_n = ''
        self._db_e = ''
        self._db = None

    def set_configuration(self, database_conf: DataBaseConfig):
        self._db_a = database_conf.database_address
        self._db_n = database_conf.database_name
        self._db_e = database_conf.database_epoch
        self._db_m_n = database_conf.database_measure_name

    def connect(self):
        if self._db is None:
            self._db = InfluxDBClient(self._db_a, database=self._db_n)

    def write(self, data):
        if data:
            mes = [{
                "measurement": self._db_m_n,
                "fields": data
            }]
            if self._db is not None:
                self._db.write_points(mes)

    def get_data(self):
        if self._db is not None:
            ms = self._db.query('SELECT * FROM ' + self._db_m_n, epoch=self._db_e)
            return list(ms.get_points())
