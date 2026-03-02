from pydantic_settings import BaseSettings
from typing import Optional
import urllib


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # SQL Server Configuration (Windows Authentication)
    DB_SERVER: str = "localhost\\SQLEXPRESS"
    DB_NAME: str = "flowpilot_db"
    DB_ENCRYPT: str = "no"
    DB_TRUST_CERT: str = "yes"
    
    # Foundry Configuration
    FOUNDRY_BASE_URL: str = "https://your-foundry-instance.com"
    FOUNDRY_API_KEY: str = "your_foundry_api_key"
    FOUNDRY_AGENT_ID: str = "your_agent_id"
    
    # Application Settings
    APP_NAME: str = "FlowPilot Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    @property
    def database_url(self) -> str:
        """
        Construct SQL Server connection string for SQLAlchemy with Windows Authentication.
        Format: mssql+pyodbc:///?odbc_connect=...
        """
        params = urllib.parse.quote_plus(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.DB_SERVER};"
            f"DATABASE={self.DB_NAME};"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate={self.DB_TRUST_CERT};"
        )
        return f"mssql+pyodbc:///?odbc_connect={params}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
