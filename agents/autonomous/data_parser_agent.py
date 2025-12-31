"""
Autonomous Data Parser Agent
Parses raw product data into structured format
"""
from typing import Dict, Any
from orchestrator.autonomous_agent import AutonomousAgent
from orchestrator.agent_protocol import AgentCapability
from models.data_models import ProductModel


class AutonomousDataParserAgent(AutonomousAgent):
    """
    Autonomous agent that parses raw product data
    
    Capabilities: PARSE_DATA
    Dependencies: None (can execute immediately)
    """
    
    def __init__(self):
        super().__init__(
            agent_id="data_parser",
            capabilities=[AgentCapability.PARSE_DATA],
            dependencies=[]  # No dependencies
        )
    
    def process(self, shared_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse raw product data
        
        Args:
            shared_state: Must contain 'raw_product_data'
            
        Returns:
            Dict with 'product' key containing ProductModel
        """
        raw_data = shared_state.get('raw_product_data')
        
        if not raw_data:
            raise ValueError("No raw_product_data found in shared state")
        
        # Parse product data
        product = self._parse_product(raw_data)
        
        print(f"    → Parsed product: {product.name}")
        print(f"    → Ingredients: {len(product.ingredients)}")
        print(f"    → Benefits: {len(product.benefits)}")
        
        return {"product": product}
    
    def _parse_product(self, raw_data: Dict[str, Any]) -> ProductModel:
        """Parse raw data into ProductModel"""
        
        # Extract and clean data
        name = raw_data.get('product_name', '').strip()
        concentration = raw_data.get('concentration', '').strip()
        
        # Parse skin types
        skin_type_str = raw_data.get('skin_type', '')
        skin_types = [s.strip() for s in skin_type_str.split(',') if s.strip()]
        
        # Parse ingredients
        ingredients_str = raw_data.get('key_ingredients', '')
        ingredients = [i.strip() for i in ingredients_str.split(',') if i.strip()]
        
        # Parse benefits
        benefits_str = raw_data.get('benefits', '')
        benefits = [b.strip() for b in benefits_str.split(',') if b.strip()]
        
        # Parse usage
        usage = raw_data.get('how_to_use', '').strip()
        
        # Parse side effects
        side_effects = raw_data.get('side_effects', '').strip()
        
        # Parse price
        price_str = raw_data.get('price', '₹0')
        price_clean = price_str.replace('₹', '').replace(',', '').strip()
        try:
            price = float(price_clean)
        except:
            price = 0.0
        
        # Create ProductModel
        product = ProductModel(
            name=name,
            concentration=concentration,
            skin_types=skin_types,
            ingredients=ingredients,
            benefits=benefits,
            usage_instructions=usage,
            side_effects=side_effects,
            price=price,
            currency="INR"
        )
        
        return product
