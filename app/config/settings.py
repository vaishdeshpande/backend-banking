#settings.py: 
"""
This file contains settings and configuration for the application, 
including database credentials and connection details.
"""
from pydantic import BaseSettings
class Settings(BaseSettings):
    database_hostname: str 
    database_port: str 
    database_password: str
    database_name: str 
    database_username: str 

    class Config:
        env_file = ".env"


