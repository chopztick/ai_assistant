from app.core.config import get_settings
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from app.infrastructure.llm.models.agent_models import Deps

# from app.infrastructure.llm.agent_tools import get_current_time, get_current_time_in_timezone, get_user_info

settings = get_settings()

async def get_chat_agent() -> Agent[Deps, str]:
    """
    Dependency to get a LLM agent
    """
    system_prompt="""
        You are a helpful assistant.
        You can answer questions, provide information, and assist with various tasks.
        Use the user information to personalize your responses.
        """

    if settings.llm_provider == "mistral":
        model = MistralModel(model_name=settings.llm_model, provider=MistralProvider(api_key=settings.llm_api_key))
    elif settings.llm_provider == "openai":
        model = OpenAIModel(model_name=settings.llm_model, provider=OpenAIProvider(api_key=settings.llm_api_key))
    elif settings.llm_provider == "anthropic":
        model = AnthropicModel(model_name=settings.llm_model, provider=AnthropicProvider(api_key=settings.llm_api_key))
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}. Supported: openai, mistral, anthropic")


    chat_agent = Agent(model=model, system_prompt=system_prompt, deps_type=Deps)

    # Register tools for the agent
    # chat_agent.tool_plain(get_current_time)
    # chat_agent.tool_plain(get_current_time_in_timezone)
    # chat_agent.tool(get_user_info)

    return chat_agent


    