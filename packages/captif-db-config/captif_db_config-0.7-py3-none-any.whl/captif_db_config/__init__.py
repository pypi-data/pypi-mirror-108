__version__ = "0.7"

from configparser import ConfigParser
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, drop_database, database_exists


CONFIG_FILENAME = ".captif-db.ini"
CONFIG_FILE = Path.home().joinpath(CONFIG_FILENAME)
DRIVERNAME = "mysql+mysqldb"


class ConfigError(Exception):
    pass


def config():
    config_ = ConfigParser()
    config_.read(CONFIG_FILE)
    return config_


def get_config_param(parameter, raise_exception=True):
    value = config().get("GENERAL", parameter, fallback="")

    if value:
        return value

    if raise_exception:
        raise ConfigError(f"'{parameter}' not defined in the config file")

    return None


class Config:

    HOST = get_config_param("host")
    PORT = get_config_param("port")
    USERNAME = get_config_param("username")
    PASSWORD = get_config_param("password")

    SSL_CA = get_config_param("ssl_ca")
    SSL_CERT = get_config_param("ssl_cert")
    SSL_KEY = get_config_param("ssl_key")

    @classmethod
    def database_connection_str(cls, database):
        return URL.create(
            drivername=DRIVERNAME,
            username=cls.USERNAME,
            password=cls.PASSWORD,
            host=cls.HOST,
            port=cls.PORT,
            database=database,
            query=cls.ssl_args(),
        )

    @classmethod
    def ssl_args(cls):
        return {
            "ssl_ca": cls.SSL_CA,
            "ssl_cert": cls.SSL_CERT,
            "ssl_key": cls.SSL_KEY,
        }


class DbSession:
    database = None  # Database name
    base = None  # SQLAlchemy Base object
    factory = None
    engine = None

    @staticmethod
    def create_engine(database, echo=False):
        return create_engine(
            Config.database_connection_str(database),
            echo=echo,
        )

    @classmethod
    def global_init(cls, test_db=False):
        if cls.factory:
            return

        cls.__check_class_definition()

        if test_db:
            cls.database += "_test"

        engine = cls.create_engine(cls.database, echo=test_db)

        cls.engine = engine
        cls.factory = sessionmaker(bind=engine)

        if database_exists(engine.url):
            if test_db:
                drop_database(engine.url)
                create_database(engine.url)
        else:
            create_database(engine.url)

        cls.base.metadata.create_all(engine)

    @classmethod
    def __check_class_definition(cls):
        if (cls.database is None) or (cls.base is None):
            raise NotImplementedError(
                f"class attributes 'database' and 'base' are not defined in "
                f"{cls.__name__} class definition"
            )
