"""
QuestionGenerator Agent
Responsibility: Generate categorized user questions from product data
"""
from typing import Dict, Any, List
import os
from agents.base_agent import BaseAgent
from models.data_models import AgentResult, ProductModel, Question
import openai


class QuestionGeneratorAgent(BaseAgent):
    """
    Generates 15+ categorized questions using LLM
    Categories: Informational, Safety, Usage, Purchase, Comparison, Ingredients, Benefits
    """
    
    CATEGORIES = [
        "Informational",
        "Safety",
        "Usage",
        "Purchase",
        "Comparison",
        "Ingredients",
        "Benefits"
    ]
    
    def __init__(self):
        super().__init__("QuestionGeneratorAgent")
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def execute(self, context: Dict[str, Any]) -> AgentResult:
        """
        Generate questions from product data
        
        Args:
            context: Must contain 'product' (ProductModel)
            
        Returns:
            AgentResult with List[Question]
        """
        return self._wrap_execution(self._generate_questions, context)
    
    def _generate_questions(self, context: Dict[str, Any]) -> List[Question]:
        """Internal question generation logic"""
        product = context.get('product')
        
        if not isinstance(product, ProductModel):
            raise ValueError("Product must be ProductModel instance")
        
        # Generate questions using LLM
        prompt = self._build_prompt(product)
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert at generating user questions for skincare products."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        questions_text = response.choices[0].message.content
        questions = self._parse_questions(questions_text)
        
        print(f"✓ {self.agent_name}: Generated {len(questions)} questions")
        return questions
    
    def _build_prompt(self, product: ProductModel) -> str:
        """Build LLM prompt for question generation"""
        return f"""Generate exactly 15 user questions about this skincare product. 
Distribute them across these categories: {', '.join(self.CATEGORIES)}

Product Details:
- Name: {product.name}
- Concentration: {product.concentration}
- Skin Types: {', '.join(product.skin_types)}
- Key Ingredients: {', '.join(product.ingredients)}
- Benefits: {', '.join(product.benefits)}
- Usage: {product.usage_instructions}
- Side Effects: {product.side_effects}
- Price: {product.currency} {product.price}

Format each question as:
[CATEGORY] Question text here?

Ensure questions are:
1. Natural and conversational
2. Relevant to the product
3. Diverse across categories
4. Actionable for users

Generate exactly 15 questions now:"""
    
    def _parse_questions(self, questions_text: str) -> List[Question]:
        """Parse LLM response into Question objects"""
        questions = []
        lines = questions_text.strip().split('\n')
        
        question_id = 1
        for line in lines:
            line = line.strip()
            if not line or not '[' in line:
                continue
            
            # Extract category and question
            try:
                category_end = line.index(']')
                category = line[1:category_end].strip()
                question_text = line[category_end+1:].strip()
                
                if category in self.CATEGORIES and question_text:
                    questions.append(Question(
                        id=f"Q{question_id:03d}",
                        category=category,
                        question=question_text,
                        priority=self._calculate_priority(category)
                    ))
                    question_id += 1
            except:
                continue
        
        # Ensure we have at least 15 questions
        if len(questions) < 15:
            raise ValueError(f"Only generated {len(questions)} questions, need 15+")
        
        return questions[:15]  # Return exactly 15
    
    def _calculate_priority(self, category: str) -> int:
        """Calculate question priority based on category"""
        priority_map = {
            "Safety": 1,
            "Usage": 2,
            "Informational": 3,
            "Benefits": 4,
            "Ingredients": 5,
            "Purchase": 6,
            "Comparison": 7
        }
        return priority_map.get(category, 5)
