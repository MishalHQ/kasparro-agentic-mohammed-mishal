"""
DataParser Agent
Responsibility: Parse and validate raw product data
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent
from models.data_models import AgentResult, ProductModel


class DataParserAgent(BaseAgent):
    """
    Parses raw product data into structured ProductModel
    Validates data integrity and normalizes formats
    """
    
    def __init__(self):
        super().__init__("DataParserAgent")
    
    def execute(self, context: Dict[str, Any]) -> AgentResult:
        """
        Parse raw product data
        
        Args:
            context: Must contain 'raw_product_data' key
            
        Returns:
            AgentResult with ProductModel
        """
        return self._wrap_execution(self._parse, context)
    
    def _parse(self, context: Dict[str, Any]) -> ProductModel:
        """Internal parsing logic"""
        raw_data = context.get('raw_product_data')
        
        if not raw_data:
            raise ValueError("No raw_product_data found in context")
        
        # Create ProductModel from raw data
        product = ProductModel.from_dict(raw_data)
        
        # Validate
        if not product.validate():
            raise ValueError("Product validation failed")
        
        print(f"✓ {self.agent_name}: Parsed product '{product.name}'")
        return product
