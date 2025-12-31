"""
Autonomous Template Filling Agents
Each agent fills a specific template type independently
"""
from typing import Dict, Any, List
from datetime import datetime
from orchestrator.autonomous_agent import AutonomousAgent
from orchestrator.agent_protocol import AgentCapability
from models.data_models import ProductModel, Question
from templates.template_schemas import TemplateRegistry, TemplateValidator
from config import MODEL_NAME, get_openai_client


class FAQTemplateAgent(AutonomousAgent):
    """Fills FAQ template with questions and answers"""
    
    def __init__(self):
        super().__init__(
            agent_id="faq_template_filler",
            capabilities=[AgentCapability.FILL_TEMPLATE],
            dependencies=[AgentCapability.PARSE_DATA, AgentCapability.GENERATE_QUESTIONS]
        )
        self.registry = TemplateRegistry()
        self.validator = TemplateValidator()
        self.client = get_openai_client()
    
    def process(self, shared_state: Dict[str, Any]) -> Dict[str, Any]:
        """Fill FAQ template"""
        parse_result = shared_state.get('parse_data')
        question_result = shared_state.get('generate_questions')
        
        product = parse_result.get('product')
        questions = question_result.get('questions')
        
        # Get template
        template = self.registry.get_template('faq')
        
        # Generate answers
        answered_questions = self._generate_answers(questions, product)
        
        # Fill template
        categories = list(set(q.category for q in answered_questions))
        
        template["product_name"] = product.name
        template["total_questions"] = len(answered_questions)
        template["categories"] = categories
        template["questions"] = [q.to_dict() for q in answered_questions]
        template["metadata"]["generated_at"] = datetime.now().isoformat()
        
        # Validate
        self.validator.validate('faq', template)
        
        print(f"    → Filled FAQ template with {len(answered_questions)} Q&A pairs")
        
        return {"faq_page": template}
    
    def _generate_answers(self, questions: List[Question], product: ProductModel) -> List[Question]:
        """Generate answers for questions using LLM"""
        
        for question in questions:
            prompt = f"""Answer this question about the product:

Product: {product.name}
Concentration: {product.concentration}
Ingredients: {', '.join(product.ingredients)}
Benefits: {', '.join(product.benefits)}
Usage: {product.usage_instructions}
Side Effects: {product.side_effects}
Price: {product.currency} {product.price}
Skin Types: {', '.join(product.skin_types)}

Question: {question.question}

Provide a clear, concise, and helpful answer (2-3 sentences):"""
            
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful skincare expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            question.answer = response.choices[0].message.content.strip()
        
        return questions


class ProductPageTemplateAgent(AutonomousAgent):
    """Fills product page template with detailed content"""
    
    def __init__(self):
        super().__init__(
            agent_id="product_page_template_filler",
            capabilities=[AgentCapability.FILL_TEMPLATE],
            dependencies=[AgentCapability.PARSE_DATA, AgentCapability.PROCESS_CONTENT]
        )
        self.registry = TemplateRegistry()
        self.validator = TemplateValidator()
        self.client = get_openai_client()
    
    def process(self, shared_state: Dict[str, Any]) -> Dict[str, Any]:
        """Fill product page template"""
        parse_result = shared_state.get('parse_data')
        product = parse_result.get('product')
        
        # Get processed content from content processors
        process_result = shared_state.get('process_content', {})
        benefits_content = process_result.get('benefits_content', {})
        ingredients_content = process_result.get('ingredients_content', {})
        usage_content = process_result.get('usage_content', {})
        safety_content = process_result.get('safety_content', {})
        
        # Get template
        template = self.registry.get_template('product')
        
        # Generate tagline and description
        tagline = self._generate_tagline(product)
        description = self._generate_description(product)
        
        # Fill template
        template["product"]["name"] = product.name
        template["product"]["tagline"] = tagline
        template["product"]["description"] = description
        template["product"]["concentration"] = product.concentration
        template["product"]["skin_types"] = product.skin_types
        
        # Price
        template["product"]["price"]["amount"] = product.price
        template["product"]["price"]["currency"] = product.currency
        template["product"]["price"]["display"] = f"{product.currency} {product.price}"
        
        # Key features
        template["product"]["key_features"] = product.benefits
        
        # Ingredients
        template["product"]["ingredients"]["key_actives"] = ingredients_content.get("key_actives", [])
        template["product"]["ingredients"]["synergy"] = ingredients_content.get("ingredient_synergy", "")
        template["product"]["ingredients"]["full_list"] = product.ingredients
        
        # Benefits
        template["product"]["benefits"]["primary"] = benefits_content.get("primary_benefit", "")
        template["product"]["benefits"]["detailed"] = benefits_content.get("detailed_benefits", [])
        template["product"]["benefits"]["timeline"] = benefits_content.get("timeline", "")
        template["product"]["benefits"]["concerns_addressed"] = benefits_content.get("concerns_addressed", [])
        
        # Usage
        template["product"]["usage"]["steps"] = usage_content.get("steps", [])
        template["product"]["usage"]["timing"] = usage_content.get("timing", "")
        template["product"]["usage"]["tips"] = usage_content.get("tips", [])
        template["product"]["usage"]["pair_with"] = usage_content.get("pair_with", [])
        template["product"]["usage"]["avoid_with"] = usage_content.get("avoid_with", [])
        
        # Safety
        template["product"]["safety"]["side_effects"] = safety_content.get("side_effects", [])
        template["product"]["safety"]["contraindications"] = safety_content.get("contraindications", [])
        template["product"]["safety"]["patch_test"] = safety_content.get("patch_test", "")
        template["product"]["safety"]["warning_signs"] = safety_content.get("warning_signs", [])
        
        template["metadata"]["generated_at"] = datetime.now().isoformat()
        
        # Validate
        self.validator.validate('product', template)
        
        print(f"    → Filled product page template for {product.name}")
        
        return {"product_page": template}
    
    def _generate_tagline(self, product: ProductModel) -> str:
        """Generate product tagline"""
        prompt = f"""Create a catchy, concise tagline (max 10 words) for this product:
Product: {product.name}
Benefits: {', '.join(product.benefits)}

Tagline:"""
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a marketing copywriter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=30
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_description(self, product: ProductModel) -> str:
        """Generate product description"""
        prompt = f"""Write a compelling product description (3-4 sentences) for:
Product: {product.name}
Concentration: {product.concentration}
Benefits: {', '.join(product.benefits)}
Skin Types: {', '.join(product.skin_types)}

Description:"""
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a product description writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        return response.choices[0].message.content.strip()


class ComparisonTemplateAgent(AutonomousAgent):
    """Fills comparison template with product comparison"""
    
    def __init__(self):
        super().__init__(
            agent_id="comparison_template_filler",
            capabilities=[AgentCapability.FILL_TEMPLATE],
            dependencies=[AgentCapability.PARSE_DATA]
        )
        self.registry = TemplateRegistry()
        self.validator = TemplateValidator()
        self.client = get_openai_client()
    
    def process(self, shared_state: Dict[str, Any]) -> Dict[str, Any]:
        """Fill comparison template"""
        parse_result = shared_state.get('parse_data')
        product = parse_result.get('product')
        
        # Generate comparison data
        comparison_data = self._generate_comparison(product)
        
        # Get template
        template = self.registry.get_template('comparison')
        
        # Fill template
        product_b_data = comparison_data.get('product_b_data', {})
        
        # Product A
        template["products"][0]["name"] = product.name
        template["products"][0]["concentration"] = product.concentration
        template["products"][0]["price"] = f"{product.currency} {product.price}"
        template["products"][0]["ingredients"] = product.ingredients
        template["products"][0]["benefits"] = product.benefits
        template["products"][0]["skin_types"] = product.skin_types
        template["products"][0]["strengths"] = comparison_data.get("product_a", {}).get("strengths", [])
        template["products"][0]["weaknesses"] = comparison_data.get("product_a", {}).get("weaknesses", [])
        
        # Product B
        template["products"][1]["name"] = product_b_data.get("name", "")
        template["products"][1]["concentration"] = product_b_data.get("concentration", "")
        template["products"][1]["price"] = f"{product_b_data.get('currency', 'INR')} {product_b_data.get('price', 0)}"
        template["products"][1]["ingredients"] = product_b_data.get("ingredients", [])
        template["products"][1]["benefits"] = product_b_data.get("benefits", [])
        template["products"][1]["skin_types"] = product_b_data.get("skin_types", [])
        template["products"][1]["strengths"] = comparison_data.get("product_b", {}).get("strengths", [])
        template["products"][1]["weaknesses"] = comparison_data.get("product_b", {}).get("weaknesses", [])
        
        # Comparison matrix
        template["comparison_matrix"]["key_differences"] = comparison_data.get("key_differences", [])
        template["comparison_matrix"]["similarities"] = comparison_data.get("similarities", [])
        template["comparison_matrix"]["best_for"] = comparison_data.get("best_for", {})
        template["comparison_matrix"]["price_value"] = comparison_data.get("price_value", "")
        
        template["recommendation"] = comparison_data.get("recommendation", "")
        template["metadata"]["generated_at"] = datetime.now().isoformat()
        
        # Validate
        self.validator.validate('comparison', template)
        
        print(f"    → Filled comparison template: {product.name} vs {product_b_data.get('name', 'Unknown')}")
        
        return {"comparison_page": template}
    
    def _generate_comparison(self, product: ProductModel) -> Dict[str, Any]:
        """Generate comparison with fictional Product B"""
        import json
        
        # First generate Product B
        prompt_b = f"""Create a fictional competing product to compare with:
Product A: {product.name}
- Concentration: {product.concentration}
- Price: {product.currency} {product.price}

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
        
        response_b = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a product developer. Respond only with valid JSON."},
                {"role": "user", "content": prompt_b}
            ],
            temperature=0.7
        )
        
        product_b = json.loads(response_b.choices[0].message.content)
        
        # Now generate comparison
        prompt_comp = f"""Compare these two skincare products:

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
        
        response_comp = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a product comparison expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt_comp}
            ],
            temperature=0.5
        )
        
        comparison = json.loads(response_comp.choices[0].message.content)
        comparison['product_b_data'] = product_b
        
        return comparison
