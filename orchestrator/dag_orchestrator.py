"""
DAG Orchestrator
Coordinates all agents via Directed Acyclic Graph execution
"""
from typing import Dict, Any, List
import json
from datetime import datetime
from models.data_models import ExecutionState, ProductModel
from agents.data_parser_agent import DataParserAgent
from agents.question_generator_agent import QuestionGeneratorAgent
from agents.content_logic_agent import ContentLogicAgent
from agents.template_engine_agent import TemplateEngineAgent


class DAGOrchestrator:
    """
    Orchestrates multi-agent workflow via DAG
    
    Execution Flow:
    START → DataParser → [QuestionGen, ContentLogic] → TemplateEngine → END
    """
    
    def __init__(self):
        self.state = ExecutionState()
        self.agents = self._initialize_agents()
        self.dag = self._build_dag()
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all agents"""
        return {
            "data_parser": DataParserAgent(),
            "question_generator": QuestionGeneratorAgent(),
            "content_logic": ContentLogicAgent(),
            "template_engine": TemplateEngineAgent()
        }
    
    def _build_dag(self) -> Dict[str, List[str]]:
        """
        Build DAG structure
        
        Returns:
            Dict mapping agent to its dependencies
        """
        return {
            "data_parser": [],  # No dependencies
            "question_generator": ["data_parser"],
            "content_logic_faq": ["data_parser", "question_generator"],
            "content_logic_product": ["data_parser"],
            "content_logic_comparison": ["data_parser"],
            "template_faq": ["content_logic_faq"],
            "template_product": ["content_logic_product"],
            "template_comparison": ["content_logic_comparison"]
        }
    
    def execute(self, raw_product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute complete workflow
        
        Args:
            raw_product_data: Raw product input
            
        Returns:
            Dict with all generated pages
        """
        print("\n" + "="*60)
        print("🚀 STARTING MULTI-AGENT ORCHESTRATION")
        print("="*60 + "\n")
        
        # Initialize context
        self.state.context['raw_product_data'] = raw_product_data
        
        # Step 1: Parse product data
        print("📊 STEP 1: Parsing Product Data")
        print("-" * 60)
        result = self.agents['data_parser'].execute(self.state.context)
        if not result.success:
            raise Exception(f"DataParser failed: {result.error}")
        product = result.data
        self.state.update('product', product)
        
        # Step 2: Generate questions
        print("\n❓ STEP 2: Generating Questions")
        print("-" * 60)
        result = self.agents['question_generator'].execute(self.state.context)
        if not result.success:
            raise Exception(f"QuestionGenerator failed: {result.error}")
        questions = result.data
        self.state.update('questions', questions)
        
        # Step 3: Process content blocks in parallel (simulated)
        print("\n🔧 STEP 3: Processing Content Blocks")
        print("-" * 60)
        
        # FAQ content
        print("\n  📝 Processing FAQ content...")
        faq_context = {
            'product': product,
            'block_types': []  # FAQ doesn't need content blocks, uses questions directly
        }
        
        # Product page content
        print("\n  📄 Processing Product Page content...")
        product_context = {
            'product': product,
            'block_types': ['benefits', 'ingredients', 'usage', 'safety']
        }
        result = self.agents['content_logic'].execute(product_context)
        if not result.success:
            raise Exception(f"ContentLogic (product) failed: {result.error}")
        product_content = result.data
        
        # Comparison page content
        print("\n  ⚖️  Processing Comparison content...")
        comparison_context = {
            'product': product,
            'block_types': ['comparison']
        }
        result = self.agents['content_logic'].execute(comparison_context)
        if not result.success:
            raise Exception(f"ContentLogic (comparison) failed: {result.error}")
        comparison_content = result.data
        
        # Step 4: Fill templates
        print("\n📋 STEP 4: Filling Templates")
        print("-" * 60)
        
        # FAQ template
        print("\n  📝 Filling FAQ template...")
        faq_template_context = {
            'template_type': 'faq',
            'product': product,
            'questions': questions
        }
        result = self.agents['template_engine'].execute(faq_template_context)
        if not result.success:
            raise Exception(f"TemplateEngine (FAQ) failed: {result.error}")
        faq_page = result.data
        
        # Product template
        print("\n  📄 Filling Product Page template...")
        product_template_context = {
            'template_type': 'product',
            'product': product,
            'content_data': product_content
        }
        result = self.agents['template_engine'].execute(product_template_context)
        if not result.success:
            raise Exception(f"TemplateEngine (Product) failed: {result.error}")
        product_page = result.data
        
        # Comparison template
        print("\n  ⚖️  Filling Comparison template...")
        comparison_template_context = {
            'template_type': 'comparison',
            'product': product,
            'content_data': comparison_content
        }
        result = self.agents['template_engine'].execute(comparison_template_context)
        if not result.success:
            raise Exception(f"TemplateEngine (Comparison) failed: {result.error}")
        comparison_page = result.data
        
        # Step 5: Collect outputs
        print("\n✅ STEP 5: Collecting Outputs")
        print("-" * 60)
        
        outputs = {
            'faq': faq_page,
            'product_page': product_page,
            'comparison_page': comparison_page
        }
        
        print("\n" + "="*60)
        print("✨ ORCHESTRATION COMPLETE")
        print("="*60)
        print(f"\n📊 Generated {len(outputs)} pages:")
        print(f"  ✓ FAQ Page: {faq_page['total_questions']} questions")
        print(f"  ✓ Product Page: {product_page['product']['name']}")
        print(f"  ✓ Comparison Page: {comparison_page['products'][0]['name']} vs {comparison_page['products'][1]['name']}")
        print()
        
        return outputs
    
    def save_outputs(self, outputs: Dict[str, Any], output_dir: str = "output"):
        """Save outputs to JSON files"""
        import os
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Save each page
        for page_type, data in outputs.items():
            filename = f"{page_type}.json" if page_type != "product_page" else "product_page.json"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Saved: {filepath}")
