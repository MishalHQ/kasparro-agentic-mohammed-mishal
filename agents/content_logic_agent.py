"""
ContentLogic Agent
Responsibility: Apply reusable content transformation blocks
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent
from models.data_models import AgentResult, ProductModel
from content_blocks.content_blocks import CONTENT_BLOCKS


class ContentLogicAgent(BaseAgent):
    """
    Applies content transformation blocks to product data
    Supports: benefits, ingredients, usage, safety, comparison
    """
    
    def __init__(self):
        super().__init__("ContentLogicAgent")
        self.blocks = CONTENT_BLOCKS
    
    def execute(self, context: Dict[str, Any]) -> AgentResult:
        """
        Apply content blocks
        
        Args:
            context: Must contain 'product' and 'block_types' (list of block names)
            
        Returns:
            AgentResult with processed content
        """
        return self._wrap_execution(self._apply_blocks, context)
    
    def _apply_blocks(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply specified content blocks"""
        product = context.get('product')
        block_types = context.get('block_types', [])
        
        if not isinstance(product, ProductModel):
            raise ValueError("Product must be ProductModel instance")
        
        if not block_types:
            raise ValueError("No block_types specified")
        
        results = {}
        for block_type in block_types:
            if block_type not in self.blocks:
                raise ValueError(f"Unknown block type: {block_type}")
            
            block = self.blocks[block_type]
            results[block_type] = block.process(product, **context)
            print(f"  ✓ Applied {block_type} block")
        
        print(f"✓ {self.agent_name}: Applied {len(results)} content blocks")
        return results
