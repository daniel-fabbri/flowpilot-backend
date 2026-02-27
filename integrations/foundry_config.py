from app.core.config import settings


class FoundryConfig:
    """
    Foundry configuration settings.
    """
    BASE_URL: str = settings.FOUNDRY_BASE_URL
    API_KEY: str = settings.FOUNDRY_API_KEY
    AGENT_ID: str = settings.FOUNDRY_AGENT_ID
    
    @classmethod
    def get_agent_endpoint(cls) -> str:
        """
        Get the Foundry Agent endpoint URL.
        """
        return f"{cls.BASE_URL}/api/agents/{cls.AGENT_ID}/chat"


foundry_config = FoundryConfig()
