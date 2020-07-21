from .web_api import WebApp

from prog. databaseimport данных DataBaseConnector, DataBaseConfig

database_config = DataBaseConfigDataBaseConfig()
db = DataBaseConnector()
database_config.database_address =  'influx'
db.set_configurationset_configuration(database_config)
db.connect()
WebApp().start()

