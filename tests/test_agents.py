"""
Unit Tests for Multi-Agent Content Generation System
"""
import unittest
from models.data_models import ProductModel, Question
from agents.data_parser_agent import DataParserAgent


class TestProductModel(unittest.TestCase):
    """Test ProductModel data class"""
    
    def test_from_dict(self):
        """Test creating ProductModel from dictionary"""
        data = {
            "product_name": "Test Serum",
            "concentration": "10% Vitamin C",
            "skin_type": "Oily, Combination",
            "key_ingredients": "Vitamin C, Hyaluronic Acid",
            "benefits": "Brightening, Anti-aging",
            "how_to_use": "Apply daily",
            "side_effects": "None",
            "price": "₹699"
        }
        
        product = ProductModel.from_dict(data)
        
        self.assertEqual(product.name, "Test Serum")
        self.assertEqual(product.price, 699)
        self.assertEqual(product.currency, "INR")
        self.assertEqual(len(product.skin_types), 2)
        self.assertEqual(len(product.ingredients), 2)
    
    def test_validation(self):
        """Test product validation"""
        product = ProductModel(
            name="Test",
            concentration="10%",
            skin_types=["Oily"],
            ingredients=["Vitamin C"],
            benefits=["Brightening"],
            usage_instructions="Apply daily",
            side_effects="None",
            price=699,
            currency="INR"
        )
        
        self.assertTrue(product.validate())
    
    def test_to_dict(self):
        """Test converting ProductModel to dictionary"""
        product = ProductModel(
            name="Test",
            concentration="10%",
            skin_types=["Oily"],
            ingredients=["Vitamin C"],
            benefits=["Brightening"],
            usage_instructions="Apply daily",
            side_effects="None",
            price=699,
            currency="INR"
        )
        
        data = product.to_dict()
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "Test")
        self.assertEqual(data["price"], 699)


class TestQuestion(unittest.TestCase):
    """Test Question data class"""
    
    def test_question_creation(self):
        """Test creating Question"""
        question = Question(
            id="Q001",
            category="Safety",
            question="Is this safe?",
            priority=1
        )
        
        self.assertEqual(question.id, "Q001")
        self.assertEqual(question.category, "Safety")
        self.assertIsNone(question.answer)
    
    def test_to_dict(self):
        """Test converting Question to dictionary"""
        question = Question(
            id="Q001",
            category="Safety",
            question="Is this safe?",
            priority=1,
            answer="Yes, it is safe."
        )
        
        data = question.to_dict()
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], "Q001")
        self.assertEqual(data["answer"], "Yes, it is safe.")


class TestDataParserAgent(unittest.TestCase):
    """Test DataParserAgent"""
    
    def test_parse_valid_data(self):
        """Test parsing valid product data"""
        agent = DataParserAgent()
        
        context = {
            'raw_product_data': {
                "product_name": "Test Serum",
                "concentration": "10% Vitamin C",
                "skin_type": "Oily",
                "key_ingredients": "Vitamin C",
                "benefits": "Brightening",
                "how_to_use": "Apply daily",
                "side_effects": "None",
                "price": "₹699"
            }
        }
        
        result = agent.execute(context)
        
        self.assertTrue(result.success)
        self.assertIsInstance(result.data, ProductModel)
        self.assertEqual(result.data.name, "Test Serum")
    
    def test_parse_missing_data(self):
        """Test parsing with missing data"""
        agent = DataParserAgent()
        
        context = {}
        
        result = agent.execute(context)
        
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)


if __name__ == '__main__':
    unittest.main()
