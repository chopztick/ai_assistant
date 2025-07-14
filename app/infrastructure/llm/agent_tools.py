from datetime import datetime
from zoneinfo import ZoneInfo
from app.infrastructure.llm.models.agent_models import Deps
from app.schemas.tool_models import TimeRequest, UserInfo
from pydantic_ai import RunContext


def get_current_time() -> str:
    """Returns the current time as yyyy-MM-dd hh:mm string format."""
    return datetime.now().strftime("%B %d, %Y %H:%M %Z")


def get_current_time_in_timezone(request: TimeRequest) -> str:
    """
    Returns the current time in the requested timezone.
    """
    try:
        tz = ZoneInfo(request.timezone)
        now = datetime.now(tz).replace(microsecond=0)
        return now.strftime("%B %d, %Y %H:%M %Z")
    except Exception:
        return f"Invalid timezone: {request.timezone}"
    
async def get_user_info(context: RunContext[Deps]) -> UserInfo:
    """
    Returns the user information.

    Args:
        context (RunContext[Deps]): The run context containing user information.

    Returns:
        UserInfo: The user information.
    """
    user_id = 1
    user = await context.deps.user_repo.get_user_by_id(user_id)
    return UserInfo.model_validate(user)