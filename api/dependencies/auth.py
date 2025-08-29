from typing import Optional
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from core.config import settings

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)


def get_api_key(api_key: str = Security(api_key_header)) -> str:
    """Basic dependency to extract the API key from the header."""
    return api_key


def create_api_key_checker(expected_key: Optional[str]):
    """
    Factory function to create a dependency that checks for a specific API key.
    If the expected_key is not configured (None), this endpoint is disabled.
    """

    def check_api_key(api_key: str = Depends(get_api_key)):
        # If the key is not configured on the server, deny all access.
        if not expected_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="This API endpoint is not configured or is currently disabled.",
            )

        if api_key == expected_key:
            return api_key

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key for this endpoint",
        )

    return check_api_key


# Create specific dependency instances for each API version using the settings
auth_v1 = create_api_key_checker(settings.API_KEY_V1)
auth_v2 = create_api_key_checker(settings.API_KEY_V2)