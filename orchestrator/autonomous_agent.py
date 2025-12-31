"""
Autonomous Agent Base Class
Agents are independent, communicate via messages, and make their own decisions
"""
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from orchestrator.agent_protocol import (
    Message, MessageType, AgentCapability, 
    MessageBus, AgentRegistration
)


class AutonomousAgent(ABC):
    """
    Base class for autonomous agents
    
    Key principles:
    1. Agents are independent and self-contained
    2. Agents communicate only via messages
    3. Agents decide when and how to act
    4. Agents can work in parallel
    """
    
    def __init__(self, agent_id: str, capabilities: List[AgentCapability], 
                 dependencies: List[AgentCapability] = None):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.dependencies = dependencies or []
        self.message_bus: Optional[MessageBus] = None
        self.state = {}
        self.is_active = False
        
    def register(self, message_bus: MessageBus):
        """Register agent with message bus"""
        self.message_bus = message_bus
        
        # Subscribe to capabilities
        for capability in self.capabilities:
            message_bus.subscribe(self.agent_id, capability)
        
        print(f"✓ Registered {self.agent_id} with capabilities: {[c.value for c in self.capabilities]}")
    
    def get_registration(self) -> AgentRegistration:
        """Get agent registration info"""
        return AgentRegistration(
            agent_id=self.agent_id,
            capabilities=self.capabilities,
            dependencies=self.dependencies,
            metadata={"state": self.state}
        )
    
    def can_execute(self, shared_state: Dict[str, Any]) -> bool:
        """
        Check if agent can execute based on dependencies
        
        Args:
            shared_state: Shared state containing results from other agents
            
        Returns:
            True if all dependencies are satisfied
        """
        for dep in self.dependencies:
            dep_key = dep.value
            if dep_key not in shared_state:
                return False
        return True
    
    def receive_messages(self) -> List[Message]:
        """Receive messages from bus"""
        if not self.message_bus:
            return []
        
        messages = []
        for capability in self.capabilities:
            messages.extend(
                self.message_bus.get_messages_for(self.agent_id, capability)
            )
        
        # Also get direct messages
        messages.extend(
            self.message_bus.get_messages_for(self.agent_id, None)
        )
        
        return messages
    
    def send_message(self, message: Message):
        """Send message to bus"""
        if self.message_bus:
            message.sender = self.agent_id
            self.message_bus.publish(message)
    
    def broadcast_result(self, capability: AgentCapability, result: Any, metadata: Dict[str, Any] = None):
        """Broadcast result to all interested agents"""
        message = Message(
            type=MessageType.RESULT,
            sender=self.agent_id,
            receiver=None,  # Broadcast
            capability=capability,
            payload={"result": result},
            metadata=metadata or {}
        )
        self.send_message(message)
    
    def request_capability(self, capability: AgentCapability, payload: Dict[str, Any]):
        """Request a capability from other agents"""
        message = Message(
            type=MessageType.REQUEST,
            sender=self.agent_id,
            receiver=None,  # Will be routed by orchestrator
            capability=capability,
            payload=payload
        )
        self.send_message(message)
    
    @abstractmethod
    def process(self, shared_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process agent logic
        
        Args:
            shared_state: Shared state from orchestrator
            
        Returns:
            Results to add to shared state
        """
        pass
    
    def execute(self, shared_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Execute agent if dependencies are satisfied
        
        Args:
            shared_state: Shared state from orchestrator
            
        Returns:
            Results or None if cannot execute
        """
        if not self.can_execute(shared_state):
            return None
        
        try:
            self.is_active = True
            result = self.process(shared_state)
            self.is_active = False
            
            # Broadcast results for each capability
            for capability in self.capabilities:
                self.broadcast_result(capability, result)
            
            return result
            
        except Exception as e:
            self.is_active = False
            error_msg = Message(
                type=MessageType.ERROR,
                sender=self.agent_id,
                payload={"error": str(e)},
                metadata={"exception_type": type(e).__name__}
            )
            self.send_message(error_msg)
            raise
    
    def __repr__(self):
        return f"{self.agent_id}(capabilities={[c.value for c in self.capabilities]})"
