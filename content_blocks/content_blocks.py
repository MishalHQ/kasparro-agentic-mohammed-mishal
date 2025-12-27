"""
Content Logic Blocks - Reusable transformation logic
Each block implements a specific content transformation strategy
"""
from typing import Dict, Any, List
from models.data_models import ProductModel
import os
import openai


class ContentBlockInterface:
    """Base interface for all content blocks"""
    
    def process(self, product: ProductModel, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError


class BenefitsBlock(ContentBlockInterface):
    """
    Transforms benefit keywords into detailed descriptions
    Maps benefits to skin concerns
    """
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def process(self, product: ProductModel, **kwargs) -> Dict[str, Any]:
        """Process benefits into structured content"""
        
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
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a skincare expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        import json
        return json.loads(response.choices[0].message.content)


class IngredientsBlock(ContentBlockInterface):
    """
    Explains ingredient functions and highlights key actives
    """
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def process(self, product: ProductModel, **kwargs) -> Dict[str, Any]:
        """Process ingredients into structured content"""
        
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
    "key_actives": [{{name": "...", "function": "...", "concentration": "..."}}],
    "ingredient_synergy": "...",
    "notable_combinations": [...]
}}"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a cosmetic chemist. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        import json
        return json.loads(response.choices[0].message.content)


class UsageBlock(ContentBlockInterface):
    """
    Formats usage instructions with contextual tips
    """
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def process(self, product: ProductModel, **kwargs) -> Dict[str, Any]:
        """Process usage instructions into structured content"""
        
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
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a skincare routine expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        import json
        return json.loads(response.choices[0].message.content)


class SafetyBlock(ContentBlockInterface):
    """
    Processes side effects and generates safety information
    """
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def process(self, product: ProductModel, **kwargs) -> Dict[str, Any]:
        """Process safety information"""
        
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
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a dermatology safety expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        import json
        return json.loads(response.choices[0].message.content)


class ComparisonBlock(ContentBlockInterface):
    """
    Compares two products and highlights differences
    """
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def process(self, product: ProductModel, **kwargs) -> Dict[str, Any]:
        """Compare two products"""
        product_b = kwargs.get('product_b')
        
        if not product_b:
            # Generate fictional Product B
            product_b = self._generate_product_b(product)
        
        prompt = f"""Compare these two skincare products:

Product A: {product.name}
- Concentration: {product.concentration}
- Ingredients: {', '.join(product.ingredients)}
- Benefits: {', '.join(product.benefits)}
- Price: {product.currency} {product.price}
- Skin Types: {', '.join(product.skin_types)}

Product B: {product_b['name']}
- Concentration: {product_b['concentration']}
- Ingredients: {', '.join(product_b['ingredients'])}
- Benefits: {', '.join(product_b['benefits'])}
- Price: {product_b['currency']} {product_b['price']}
- Skin Types: {', '.join(product_b['skin_types'])}

Provide:
1. Key differences
2. Similarities
3. Which is better for specific concerns
4. Price-value comparison
5. Recommendation

Format as JSON:
{{
    "product_a": {{"name": "...", "strengths": [...], "weaknesses": [...]}},
    "product_b": {{"name": "...", "strengths": [...], "weaknesses": [...]}},
    "key_differences": [...],
    "similarities": [...],
    "best_for": {{"product_a": [...], "product_b": [...]}},
    "price_value": "...",
    "recommendation": "..."
}}"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a product comparison expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        result['product_b_data'] = product_b
        return result
    
    def _generate_product_b(self, product_a: ProductModel) -> Dict[str, Any]:
        """Generate fictional Product B for comparison"""
        
        prompt = f"""Create a fictional competing product to compare with:
Product A: {product_a.name}
- Concentration: {product_a.concentration}
- Price: {product_a.currency} {product_a.price}

Create Product B with:
- Similar category but different formulation
- Different concentration
- Different price point
- Different ingredient mix
- Realistic product name

Format as JSON:
{{
    "name": "...",
    "concentration": "...",
    "ingredients": [...],
    "benefits": [...],
    "price": number,
    "currency": "INR",
    "skin_types": [...]
}}"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a product developer. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        import json
        return json.loads(response.choices[0].message.content)


# Registry of all content blocks
CONTENT_BLOCKS = {
    "benefits": BenefitsBlock(),
    "ingredients": IngredientsBlock(),
    "usage": UsageBlock(),
    "safety": SafetyBlock(),
    "comparison": ComparisonBlock()
}
