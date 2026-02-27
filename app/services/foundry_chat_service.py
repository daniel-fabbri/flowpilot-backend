import httpx
from typing import Dict, Any, Optional
from integrations.foundry_config import foundry_config


async def chat_with_foundry_agent(message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Send a message to the Foundry Agent and get a response.
    
    Args:
        message: The message to send to the agent
        context: Optional context dictionary to provide additional information
        
    Returns:
        Dictionary containing the agent's response
        
    Raises:
        httpx.HTTPError: If the request fails
        httpx.TimeoutException: If the request times out
    """
    endpoint = foundry_config.get_agent_endpoint()
    
    headers = {
        "Authorization": f"Bearer {foundry_config.API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "agent_id": foundry_config.AGENT_ID,
        "message": message,
    }
    
    if context:
        payload["context"] = context
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                endpoint,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException as e:
        return {
            "error": "Request timeout",
            "message": "The request to Foundry Agent timed out",
            "details": str(e)
        }
    except httpx.HTTPStatusError as e:
        return {
            "error": "HTTP error",
            "message": f"Foundry Agent returned status {e.response.status_code}",
            "details": str(e)
        }
    except httpx.RequestError as e:
        return {
            "error": "Request error",
            "message": "Failed to connect to Foundry Agent",
            "details": str(e)
        }
    except Exception as e:
        return {
            "error": "Unknown error",
            "message": "An unexpected error occurred",
            "details": str(e)
        }
