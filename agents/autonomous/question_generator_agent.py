"""
Autonomous Question Generator Agent
Generates user questions from product data using LLM
"""
from typing import Dict, Any, List
from orchestrator.autonomous_agent import AutonomousAgent
from orchestrator.agent_protocol import AgentCapability
from models.data_models import ProductModel, Question
from config import MODEL_NAME, get_openai_client


class AutonomousQuestionGeneratorAgent(AutonomousAgent):
    """
    Autonomous agent that generates questions
    
    Capabilities: GENERATE_QUESTIONS
    Dependencies: PARSE_DATA (needs product data)
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
        super().__init__(
            agent_id="question_generator",
            capabilities=[AgentCapability.GENERATE_QUESTIONS],
            dependencies=[AgentCapability.PARSE_DATA]
        )
        self.client = get_openai_client()
    
    def process(self, shared_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate questions from product data
        
        Args:
            shared_state: Must contain 'parse_data' with product
            
        Returns:
            Dict with 'questions' key containing List[Question]
        """
        parse_result = shared_state.get('parse_data')
        
        if not parse_result:
            raise ValueError("No parse_data found in shared state")
        
        product = parse_result.get('product')
        
        if not isinstance(product, ProductModel):
            raise ValueError("Product must be ProductModel instance")
        
        # Generate questions
        questions = self._generate_questions(product)
        
        print(f"    → Generated {len(questions)} questions")
        print(f"    → Categories: {len(set(q.category for q in questions))}")
        
        return {"questions": questions}
    
    def _generate_questions(self, product: ProductModel) -> List[Question]:
        """Generate questions using LLM"""
        
        prompt = f"""Generate exactly 15 user questions about this skincare product. 
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
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert at generating user questions for skincare products."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        questions_text = response.choices[0].message.content
        questions = self._parse_questions(questions_text)
        
        return questions
    
    def _parse_questions(self, questions_text: str) -> List[Question]:
        """Parse LLM response into Question objects"""
        questions = []
        lines = questions_text.strip().split('\n')
        
        question_id = 1
        for line in lines:
            line = line.strip()
            if not line or not '[' in line:
                continue
            
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
        
        if len(questions) < 15:
            raise ValueError(f"Only generated {len(questions)} questions, need 15+")
        
        return questions[:15]
    
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
