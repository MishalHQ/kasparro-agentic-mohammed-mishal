"""
Autonomous Content Processing Agents
Each agent processes specific content types independently
"""
from typing import Dict, Any
import json
from orchestrator.autonomous_agent import AutonomousAgent
from orchestrator.agent_protocol import AgentCapability
from models.data_models import ProductModel
from config import MODEL_NAME, get_openai_client


class BenefitsProcessorAgent(AutonomousAgent):
    """Processes product benefits into detailed content"""
    
    def __init__(self):
        super().__init__(
            agent_id="benefits_processor",
            capabilities=[AgentCapability.PROCESS_CONTENT],
            dependencies=[AgentCapability.PARSE_DATA]
        )
        self.client = get_openai_client()
    
    def process(self, shared_state: Dict[str, Any]) -> Dict[str, Any]:
        """Process benefits content"""
        parse_result = shared_state.get('parse_data')
        product = parse_result.get('product')
        
        prompt = f"""Analyze these skincare benefits and provide detailed information:
Benefits: {', '.join(product.benefits)}
Product: {product.name}

Provide:
1. Primary benefit (most important)
2. Detailed explanation of each benefit (2-3 sentences each)
3. Expected timeline for results
4. Skin concerns addressed

Format as JSON:
{{
    "primary_benefit": "...",
    "detailed_benefits": [{{"benefit": "...", "description": "..."}}],
    "timeline": "...",
    "concerns_addressed": [...]
}}"""
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a skincare expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        result = json.loads(response.choices[0].message.content)
        print(f"    → Processed benefits: {result['primary_benefit']}")
        
        return {"benefits_content": result}


class IngredientsProcessorAgent(AutonomousAgent):
    """Processes product ingredients into detailed content"""
    
    def __init__(self):
        super().__init__(
            agent_id="ingredients_processor",
            capabilities=[AgentCapability.PROCESS_CONTENT],
            dependencies=[AgentCapability.PARSE_DATA]
        )
        self.client = get_openai_client()
    
    def process(self, shared_state: Dict[str, Any]) -> Dict[str, Any]:
        """Process ingredients content"""
        parse_result = shared_state.get('parse_data')
        product = parse_result.get('product')
        
        prompt = f"""Analyze these skincare ingredients:
Ingredients: {', '.join(product.ingredients)}
Product: {product.name}

Provide:
1. Key active ingredients (most important ones)
2. Function of each ingredient
3. Why these ingredients work together
4. Any notable ingredient combinations

Format as JSON:
{{
    "key_actives": [{{"name": "...", "function": "...", "concentration": "..."}}],
    "ingredient_synergy": "...",
    "notable_combinations": [...]
}}"""
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a cosmetic chemist. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        result = json.loads(response.choices[0].message.content)
        print(f"    → Processed {len(result['key_actives'])} key ingredients")
        
        return {"ingredients_content": result}


class UsageProcessorAgent(AutonomousAgent):
    """Processes usage instructions into detailed content"""
    
    def __init__(self):
        super().__init__(
            agent_id="usage_processor",
            capabilities=[AgentCapability.PROCESS_CONTENT],
            dependencies=[AgentCapability.PARSE_DATA]
        )
        self.client = get_openai_client()
    
    def process(self, shared_state: Dict[str, Any]) -> Dict[str, Any]:
        """Process usage content"""
        parse_result = shared_state.get('parse_data')
        product = parse_result.get('product')
        
        prompt = f"""Create detailed usage instructions for this product:
Product: {product.name}
Basic Instructions: {product.usage_instructions}
Skin Types: {', '.join(product.skin_types)}

Provide:
1. Step-by-step application guide
2. Best time to use (AM/PM)
3. Tips for maximum effectiveness
4. What to pair it with
5. What to avoid using with it

Format as JSON:
{{
    "steps": ["step 1", "step 2", ...],
    "timing": "...",
    "tips": [...],
    "pair_with": [...],
    "avoid_with": [...]
}}"""
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a skincare routine expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        result = json.loads(response.choices[0].message.content)
        print(f"    → Processed {len(result['steps'])} usage steps")
        
        return {"usage_content": result}


class SafetyProcessorAgent(AutonomousAgent):
    """Processes safety information into detailed content"""
    
    def __init__(self):
        super().__init__(
            agent_id="safety_processor",
            capabilities=[AgentCapability.PROCESS_CONTENT],
            dependencies=[AgentCapability.PARSE_DATA]
        )
        self.client = get_openai_client()
    
    def process(self, shared_state: Dict[str, Any]) -> Dict[str, Any]:
        """Process safety content"""
        parse_result = shared_state.get('parse_data')
        product = parse_result.get('product')
        
        prompt = f"""Analyze safety information for this product:
Product: {product.name}
Side Effects: {product.side_effects}
Skin Types: {', '.join(product.skin_types)}

Provide:
1. Common side effects and how to manage them
2. Who should avoid this product
3. Patch test recommendations
4. Warning signs to watch for

Format as JSON:
{{
    "side_effects": [{{"effect": "...", "management": "..."}}],
    "contraindications": [...],
    "patch_test": "...",
    "warning_signs": [...]
}}"""
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a dermatology safety expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        result = json.loads(response.choices[0].message.content)
        print(f"    → Processed {len(result['side_effects'])} safety items")
        
        return {"safety_content": result}
