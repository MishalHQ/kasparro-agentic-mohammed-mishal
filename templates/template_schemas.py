"""
Template Definitions
Structured schemas for FAQ, Product Page, and Comparison Page
"""
from typing import Dict, Any, List
from datetime import datetime


class TemplateRegistry:
    """
    Registry of all template schemas
    """
    
    @staticmethod
    def get_faq_template() -> Dict[str, Any]:
        """FAQ page template schema"""
        return {
            "page_type": "faq",
            "product_name": None,
            "total_questions": 0,
            "categories": [],
            "questions": [],
            "metadata": {
                "generated_at": None,
                "version": "1.0"
            }
        }
    
    @staticmethod
    def get_product_page_template() -> Dict[str, Any]:
        """Product page template schema"""
        return {
            "page_type": "product",
            "product": {
                "name": None,
                "tagline": None,
                "description": None,
                "price": {
                    "amount": None,
                    "currency": None,
                    "display": None
                },
                "concentration": None,
                "skin_types": [],
                "key_features": [],
                "ingredients": {
                    "key_actives": [],
                    "full_list": [],
                    "synergy": None
                },
                "benefits": {
                    "primary": None,
                    "detailed": [],
                    "timeline": None,
                    "concerns_addressed": []
                },
                "usage": {
                    "steps": [],
                    "timing": None,
                    "tips": [],
                    "pair_with": [],
                    "avoid_with": []
                },
                "safety": {
                    "side_effects": [],
                    "contraindications": [],
                    "patch_test": None,
                    "warning_signs": []
                }
            },
            "metadata": {
                "generated_at": None,
                "version": "1.0"
            }
        }
    
    @staticmethod
    def get_comparison_template() -> Dict[str, Any]:
        """Comparison page template schema"""
        return {
            "page_type": "comparison",
            "products": [
                {
                    "name": None,
                    "concentration": None,
                    "price": None,
                    "ingredients": [],
                    "benefits": [],
                    "skin_types": [],
                    "strengths": [],
                    "weaknesses": []
                },
                {
                    "name": None,
                    "concentration": None,
                    "price": None,
                    "ingredients": [],
                    "benefits": [],
                    "skin_types": [],
                    "strengths": [],
                    "weaknesses": []
                }
            ],
            "comparison_matrix": {
                "key_differences": [],
                "similarities": [],
                "best_for": {
                    "product_a": [],
                    "product_b": []
                },
                "price_value": None
            },
            "recommendation": None,
            "metadata": {
                "generated_at": None,
                "version": "1.0"
            }
        }
    
    @staticmethod
    def get_template(template_type: str) -> Dict[str, Any]:
        """Get template by type"""
        templates = {
            "faq": TemplateRegistry.get_faq_template(),
            "product": TemplateRegistry.get_product_page_template(),
            "comparison": TemplateRegistry.get_comparison_template()
        }
        
        if template_type not in templates:
            raise ValueError(f"Unknown template type: {template_type}")
        
        return templates[template_type]


class TemplateValidator:
    """
    Validates filled templates against schemas
    """
    
    @staticmethod
    def validate_faq(data: Dict[str, Any]) -> bool:
        """Validate FAQ template"""
        required_fields = ["page_type", "product_name", "questions"]
        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(data["questions"], list) or len(data["questions"]) == 0:
            raise ValueError("Questions must be a non-empty list")
        
        return True
    
    @staticmethod
    def validate_product(data: Dict[str, Any]) -> bool:
        """Validate product page template"""
        if "product" not in data:
            raise ValueError("Missing product field")
        
        product = data["product"]
        required_fields = ["name", "price", "ingredients", "benefits", "usage"]
        for field in required_fields:
            if field not in product or product[field] is None:
                raise ValueError(f"Missing required product field: {field}")
        
        return True
    
    @staticmethod
    def validate_comparison(data: Dict[str, Any]) -> bool:
        """Validate comparison template"""
        if "products" not in data or len(data["products"]) != 2:
            raise ValueError("Comparison must have exactly 2 products")
        
        if "comparison_matrix" not in data:
            raise ValueError("Missing comparison_matrix")
        
        return True
    
    @staticmethod
    def validate(template_type: str, data: Dict[str, Any]) -> bool:
        """Validate template by type"""
        validators = {
            "faq": TemplateValidator.validate_faq,
            "product": TemplateValidator.validate_product,
            "comparison": TemplateValidator.validate_comparison
        }
        
        if template_type not in validators:
            raise ValueError(f"Unknown template type: {template_type}")
        
        return validators[template_type](data)
