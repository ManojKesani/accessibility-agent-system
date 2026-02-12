from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any, List
import config
from langchain_core.rate_limiters import InMemoryRateLimiter

class BaseAgent:
    """Base class for all agents in the system."""
    
    def __init__(self, name: str, role: str, goal: str, backstory: str):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.llm = self._create_llm()


    def _create_llm(self):
        """Create LLM instance with Groq."""
        rate_limiter = InMemoryRateLimiter(
        requests_per_second=config.requests_per_second,  
        check_every_n_seconds=0.1,  # Check every 100ms whether allowed to make a request
    )
        return ChatGroq(
            api_key=config.GROQ_API_KEY,
            model_name=config.MODEL_NAME,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
            # rate_limiter=rate_limiter
        )
    
    def create_prompt(self, template: str) -> ChatPromptTemplate:
        """Create a prompt template."""
        return ChatPromptTemplate.from_messages([
            ("system", f"""You are {self.name}, a {self.role}.
            
Goal: {self.goal}

Background: {self.backstory}

You should always:
- Be thorough and detailed in your analysis
- Provide actionable recommendations
- Follow WCAG guidelines
- Consider user experience impact
"""),
            ("user", template)
        ])
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's task.
        Override this method in subclasses.
        """
        raise NotImplementedError("Subclasses must implement execute method")
    
    def __str__(self):
        return f"{self.name} ({self.role})"
