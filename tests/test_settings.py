from pydantic import BaseSettings

class DummySettings(BaseSettings):
    database_hostname: str = "test_host"
    database_port: str = "test_port"
    database_password: str = "test_password"
    database_name: str = "test_db"
    database_username: str = "test_user"