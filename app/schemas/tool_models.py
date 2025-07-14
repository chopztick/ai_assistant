from pydantic import BaseModel, ConfigDict

class TimeRequest(BaseModel):
    """
    Request model for getting the current time in a specific timezone.
    """
    timezone: str  # e.g., "UTC", "Europe/Paris", "America/New_York"

class UserInfo(BaseModel):
    """
    Model for user information.
    """
    firstname: str
    lastname: str
    email: str

    model_config = ConfigDict(from_attributes=True)
