from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # SQL Server Configuration
    SQLSERVER_USER: str
    SQLSERVER_PASSWORD: str
    SQLSERVER_SERVER: str
    SQLSERVER_PORT: str = "1433"
    SQLSERVER_DB: str
    
    # Foundry Configuration
    FOUNDRY_BASE_URL: str
    FOUNDRY_API_KEY: str
    FOUNDRY_AGENT_ID: str
    
    # Application Settings
    APP_NAME: str = "FlowPilot Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    @property
    def database_url(self) -> str:
        """
        Construct SQL Server connection string for SQLAlchemy.
        Format: mssql+pyodbc://USER:PASSWORD@SERVER:PORT/DATABASE?driver=ODBC+Driver+17+for+SQL+Server
        """
        return (
            f"mssql+pyodbc://{self.SQLSERVER_USER}:{self.SQLSERVER_PASSWORD}"
            f"@{self.SQLSERVER_SERVER}:{self.SQLSERVER_PORT}/{self.SQLSERVER_DB}"
            f"?driver=ODBC+Driver+17+for+SQL+Server"
        )
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
