"""
Agent Communication Protocol
Defines message types and communication patterns for agent interaction
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid


class MessageType(Enum):
    """Types of messages agents can send"""
    REQUEST = "request"           # Request for work
    RESPONSE = "response"         # Response to request
    EVENT = "event"               # Broadcast event
    QUERY = "query"               # Query for information
    RESULT = "result"             # Result of computation
    ERROR = "error"               # Error notification


class AgentCapability(Enum):
    """Capabilities that agents can advertise"""
    PARSE_DATA = "parse_data"
    GENERATE_QUESTIONS = "generate_questions"
    PROCESS_CONTENT = "process_content"
    FILL_TEMPLATE = "fill_template"
    VALIDATE_OUTPUT = "validate_output"


@dataclass
class Message:
    """Message passed between agents"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType = MessageType.REQUEST
    sender: str = ""
    receiver: Optional[str] = None  # None = broadcast
    capability: Optional[AgentCapability] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "type": self.type.value,
            "sender": self.sender,
            "receiver": self.receiver,
            "capability": self.capability.value if self.capability else None,
            "payload": self.payload,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }


@dataclass
class AgentRegistration:
    """Agent registration information"""
    agent_id: str
    capabilities: List[AgentCapability]
    dependencies: List[AgentCapability] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def can_handle(self, capability: AgentCapability) -> bool:
        """Check if agent can handle a capability"""
        return capability in self.capabilities
    
    def needs(self, capability: AgentCapability) -> bool:
        """Check if agent needs a capability"""
        return capability in self.dependencies


class MessageBus:
    """Central message bus for agent communication"""
    
    def __init__(self):
        self.messages: List[Message] = []
        self.subscribers: Dict[str, List[str]] = {}  # capability -> [agent_ids]
        self.message_history: List[Message] = []
    
    def subscribe(self, agent_id: str, capability: AgentCapability):
        """Subscribe agent to messages for a capability"""
        cap_key = capability.value
        if cap_key not in self.subscribers:
            self.subscribers[cap_key] = []
        if agent_id not in self.subscribers[cap_key]:
            self.subscribers[cap_key].append(agent_id)
    
    def publish(self, message: Message):
        """Publish message to bus"""
        self.messages.append(message)
        self.message_history.append(message)
    
    def get_messages_for(self, agent_id: str, capability: Optional[AgentCapability] = None) -> List[Message]:
        """Get messages for an agent"""
        messages = []
        for msg in self.messages:
            # Direct messages
            if msg.receiver == agent_id:
                messages.append(msg)
            # Broadcast messages for subscribed capabilities
            elif msg.receiver is None and capability and msg.capability == capability:
                messages.append(msg)
        return messages
    
    def clear_messages_for(self, agent_id: str):
        """Clear processed messages for an agent"""
        self.messages = [m for m in self.messages if m.receiver != agent_id]
    
    def get_history(self) -> List[Message]:
        """Get message history"""
        return self.message_history.copy()


class AgentRegistry:
    """Registry of all agents and their capabilities"""
    
    def __init__(self):
        self.agents: Dict[str, AgentRegistration] = {}
    
    def register(self, registration: AgentRegistration):
        """Register an agent"""
        self.agents[registration.agent_id] = registration
    
    def find_agents_for(self, capability: AgentCapability) -> List[str]:
        """Find agents that can handle a capability"""
        return [
            agent_id 
            for agent_id, reg in self.agents.items() 
            if reg.can_handle(capability)
        ]
    
    def get_dependencies(self, agent_id: str) -> List[AgentCapability]:
        """Get dependencies for an agent"""
        if agent_id in self.agents:
            return self.agents[agent_id].dependencies
        return []
    
    def get_all_agents(self) -> List[str]:
        """Get all registered agent IDs"""
        return list(self.agents.keys())
