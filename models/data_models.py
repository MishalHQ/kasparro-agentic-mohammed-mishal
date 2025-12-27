"""
Data Models for the Multi-Agent Content Generation System
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


@dataclass
class ProductModel:
    """
    Core product data model with validation and serialization
    """
    name: str
    concentration: str
    skin_types: List[str]
    ingredients: List[str]
    benefits: List[str]
    usage_instructions: str
    side_effects: str
    price: float
    currency: str = "INR"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "concentration": self.concentration,
            "skin_types": self.skin_types,
            "ingredients": self.ingredients,
            "benefits": self.benefits,
            "usage_instructions": self.usage_instructions,
            "side_effects": self.side_effects,
            "price": self.price,
            "currency": self.currency
        }
    
    def validate(self) -> bool:
        """Validate required fields"""
        if not self.name or not self.ingredients or not self.benefits:
            return False
        if self.price <= 0:
            return False
        return True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProductModel':
        """Create ProductModel from dictionary"""
        # Parse comma-separated values
        skin_types = [s.strip() for s in data.get('skin_type', '').split(',')]
        ingredients = [i.strip() for i in data.get('key_ingredients', '').split(',')]
        benefits = [b.strip() for b in data.get('benefits', '').split(',')]
        
        # Extract price and currency
        price_str = data.get('price', '₹0')
        price = float(''.join(filter(str.isdigit, price_str)))
        currency = 'INR' if '₹' in price_str else 'USD'
        
        return cls(
            name=data.get('product_name', ''),
            concentration=data.get('concentration', ''),
            skin_types=skin_types,
            ingredients=ingredients,
            benefits=benefits,
            usage_instructions=data.get('how_to_use', ''),
            side_effects=data.get('side_effects', ''),
            price=price,
            currency=currency
        )


@dataclass
class Question:
    """
    Question model with category and priority
    """
    id: str
    category: str
    question: str
    priority: int
    answer: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "category": self.category,
            "question": self.question,
            "answer": self.answer,
            "priority": self.priority
        }


@dataclass
class ContentBlock:
    """
    Reusable content block with metadata
    """
    block_type: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "block_type": self.block_type,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "metadata": self.metadata
        }


@dataclass
class ExecutionState:
    """
    Tracks execution state across agents
    """
    context: Dict[str, Any] = field(default_factory=dict)
    completed_agents: List[str] = field(default_factory=list)
    errors: List[Dict[str, Any]] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    
    def update(self, agent_name: str, result: Any):
        """Update state with agent result"""
        self.context[agent_name] = result
        self.completed_agents.append(agent_name)
    
    def get_context(self) -> Dict[str, Any]:
        """Get current execution context"""
        return self.context
    
    def add_error(self, agent_name: str, error: Exception):
        """Log error"""
        self.errors.append({
            "agent": agent_name,
            "error": str(error),
            "timestamp": datetime.now().isoformat()
        })
    
    def get_outputs(self) -> Dict[str, Any]:
        """Get all outputs"""
        return self.context


@dataclass
class AgentResult:
    """
    Standard agent result wrapper
    """
    agent_name: str
    success: bool
    data: Any
    error: Optional[str] = None
    execution_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "agent_name": self.agent_name,
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "execution_time": self.execution_time
        }
