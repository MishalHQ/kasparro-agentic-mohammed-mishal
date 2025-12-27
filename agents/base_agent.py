"""
Base Agent Interface
All agents inherit from this base class
"""
from abc import ABC, abstractmethod
from typing import Any, Dict
import time
from models.data_models import AgentResult


class BaseAgent(ABC):
    """
    Abstract base class for all agents
    Enforces single responsibility and clear interfaces
    """
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.execution_count = 0
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> AgentResult:
        """
        Execute agent logic
        
        Args:
            context: Execution context from orchestrator
            
        Returns:
            AgentResult with success status and data
        """
        pass
    
    def _wrap_execution(self, func, *args, **kwargs) -> AgentResult:
        """
        Wrapper for execution with timing and error handling
        """
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            self.execution_count += 1
            
            return AgentResult(
                agent_name=self.agent_name,
                success=True,
                data=result,
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return AgentResult(
                agent_name=self.agent_name,
                success=False,
                data=None,
                error=str(e),
                execution_time=execution_time
            )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        return {
            "agent_name": self.agent_name,
            "execution_count": self.execution_count
        }
