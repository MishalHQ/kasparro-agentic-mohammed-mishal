"""
TemplateEngine Agent
Responsibility: Fill templates with processed content
"""
from typing import Dict, Any, List
from datetime import datetime
import os
from agents.base_agent import BaseAgent
from models.data_models import AgentResult, ProductModel, Question
from templates.template_schemas import TemplateRegistry, TemplateValidator
import openai


class TemplateEngineAgent(BaseAgent):
    """
    Fills templates with processed data
    Supports FAQ, Product Page, and Comparison templates
    """
    
    def __init__(self):
        super().__init__("TemplateEngineAgent")
        self.registry = TemplateRegistry()
        self.validator = TemplateValidator()
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def execute(self, context: Dict[str, Any]) -> AgentResult:
        """
        Fill template with data
        
        Args:
            context: Must contain 'template_type' and relevant data
            
        Returns:
            AgentResult with filled template
        """
        return self._wrap_execution(self._fill_template, context)
    
    def _fill_template(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fill template based on type"""
        template_type = context.get('template_type')
        
        if not template_type:
            raise ValueError("No template_type specified")
        
        # Get empty template
        template = self.registry.get_template(template_type)
        
        # Fill based on type
        if template_type == "faq":
            filled = self._fill_faq_template(template, context)
        elif template_type == "product":
            filled = self._fill_product_template(template, context)
        elif template_type == "comparison":
            filled = self._fill_comparison_template(template, context)
        else:
            raise ValueError(f"Unknown template type: {template_type}")
        
        # Validate
        self.validator.validate(template_type, filled)
        
        print(f"✓ {self.agent_name}: Filled {template_type} template")
        return filled
    
    def _fill_faq_template(self, template: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Fill FAQ template"""
        product = context.get('product')
        questions = context.get('questions', [])
        
        if not isinstance(product, ProductModel):
            raise ValueError("Product must be ProductModel")
        
        if not questions:
            raise ValueError("No questions provided")
        
        # Generate answers for questions
        answered_questions = self._generate_answers(questions, product)
        
        # Get unique categories
        categories = list(set(q.category for q in answered_questions))
        
        template["product_name"] = product.name
        template["total_questions"] = len(answered_questions)
        template["categories"] = categories
        template["questions"] = [q.to_dict() for q in answered_questions]
        template["metadata"]["generated_at"] = datetime.now().isoformat()
        
        return template
    
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
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful skincare expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            question.answer = response.choices[0].message.content.strip()
        
        return questions
    
    def _fill_product_template(self, template: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Fill product page template"""
        product = context.get('product')
        content_data = context.get('content_data', {})
        
        if not isinstance(product, ProductModel):
            raise ValueError("Product must be ProductModel")
        
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
        
        # Key features (from benefits)
        template["product"]["key_features"] = product.benefits
        
        # Ingredients
        if "ingredients" in content_data:
            ing_data = content_data["ingredients"]
            template["product"]["ingredients"]["key_actives"] = ing_data.get("key_actives", [])
            template["product"]["ingredients"]["synergy"] = ing_data.get("ingredient_synergy", "")
        template["product"]["ingredients"]["full_list"] = product.ingredients
        
        # Benefits
        if "benefits" in content_data:
            ben_data = content_data["benefits"]
            template["product"]["benefits"]["primary"] = ben_data.get("primary_benefit", "")
            template["product"]["benefits"]["detailed"] = ben_data.get("detailed_benefits", [])
            template["product"]["benefits"]["timeline"] = ben_data.get("timeline", "")
            template["product"]["benefits"]["concerns_addressed"] = ben_data.get("concerns_addressed", [])
        
        # Usage
        if "usage" in content_data:
            usage_data = content_data["usage"]
            template["product"]["usage"]["steps"] = usage_data.get("steps", [])
            template["product"]["usage"]["timing"] = usage_data.get("timing", "")
            template["product"]["usage"]["tips"] = usage_data.get("tips", [])
            template["product"]["usage"]["pair_with"] = usage_data.get("pair_with", [])
            template["product"]["usage"]["avoid_with"] = usage_data.get("avoid_with", [])
        
        # Safety
        if "safety" in content_data:
            safety_data = content_data["safety"]
            template["product"]["safety"]["side_effects"] = safety_data.get("side_effects", [])
            template["product"]["safety"]["contraindications"] = safety_data.get("contraindications", [])
            template["product"]["safety"]["patch_test"] = safety_data.get("patch_test", "")
            template["product"]["safety"]["warning_signs"] = safety_data.get("warning_signs", [])
        
        template["metadata"]["generated_at"] = datetime.now().isoformat()
        
        return template
    
    def _generate_tagline(self, product: ProductModel) -> str:
        """Generate product tagline"""
        prompt = f"""Create a catchy, concise tagline (max 10 words) for this product:
Product: {product.name}
Benefits: {', '.join(product.benefits)}

Tagline:"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
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
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a product description writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        return response.choices[0].message.content.strip()
    
    def _fill_comparison_template(self, template: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Fill comparison template"""
        product = context.get('product')
        content_data = context.get('content_data', {})
        
        if not isinstance(product, ProductModel):
            raise ValueError("Product must be ProductModel")
        
        if "comparison" not in content_data:
            raise ValueError("No comparison data provided")
        
        comp_data = content_data["comparison"]
        product_b_data = comp_data.get("product_b_data", {})
        
        # Product A
        template["products"][0]["name"] = product.name
        template["products"][0]["concentration"] = product.concentration
        template["products"][0]["price"] = f"{product.currency} {product.price}"
        template["products"][0]["ingredients"] = product.ingredients
        template["products"][0]["benefits"] = product.benefits
        template["products"][0]["skin_types"] = product.skin_types
        template["products"][0]["strengths"] = comp_data.get("product_a", {}).get("strengths", [])
        template["products"][0]["weaknesses"] = comp_data.get("product_a", {}).get("weaknesses", [])
        
        # Product B
        template["products"][1]["name"] = product_b_data.get("name", "")
        template["products"][1]["concentration"] = product_b_data.get("concentration", "")
        template["products"][1]["price"] = f"{product_b_data.get('currency', 'INR')} {product_b_data.get('price', 0)}"
        template["products"][1]["ingredients"] = product_b_data.get("ingredients", [])
        template["products"][1]["benefits"] = product_b_data.get("benefits", [])
        template["products"][1]["skin_types"] = product_b_data.get("skin_types", [])
        template["products"][1]["strengths"] = comp_data.get("product_b", {}).get("strengths", [])
        template["products"][1]["weaknesses"] = comp_data.get("product_b", {}).get("weaknesses", [])
        
        # Comparison matrix
        template["comparison_matrix"]["key_differences"] = comp_data.get("key_differences", [])
        template["comparison_matrix"]["similarities"] = comp_data.get("similarities", [])
        template["comparison_matrix"]["best_for"] = comp_data.get("best_for", {})
        template["comparison_matrix"]["price_value"] = comp_data.get("price_value", "")
        
        template["recommendation"] = comp_data.get("recommendation", "")
        template["metadata"]["generated_at"] = datetime.now().isoformat()
        
        return template
