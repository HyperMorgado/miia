from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentSettings(BaseSettings): 
    # infraestructure = {}
    # secrets = {
    #     'jwt': Field(..., env='JWT_SECRET'),
    # }
    # externalAPIs = {}
    
    class Config(SettingsConfigDict):
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True
        allow_population_by_field_name = True
        use_enum_values = True

settings = EnvironmentSettings()