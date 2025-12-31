"""
Main Entry Point - Dynamic Multi-Agent System
Demonstrates true agent autonomy with dynamic coordination
"""
import os
import sys
import json
from dotenv import load_dotenv

# Import dynamic orchestrator
from orchestrator.dynamic_orchestrator import DynamicOrchestrator

# Import autonomous agents
from agents.autonomous.data_parser_agent import AutonomousDataParserAgent
from agents.autonomous.question_generator_agent import AutonomousQuestionGeneratorAgent
from agents.autonomous.content_processor_agents import (
    BenefitsProcessorAgent,
    IngredientsProcessorAgent,
    UsageProcessorAgent,
    SafetyProcessorAgent
)
from agents.autonomous.template_filler_agents import (
    FAQTemplateAgent,
    ProductPageTemplateAgent,
    ComparisonTemplateAgent
)


# Product data (as specified in assignment)
PRODUCT_DATA = {
    "product_name": "GlowBoost Vitamin C Serum",
    "concentration": "10% Vitamin C",
    "skin_type": "Oily, Combination",
    "key_ingredients": "Vitamin C, Hyaluronic Acid",
    "benefits": "Brightening, Fades dark spots",
    "how_to_use": "Apply 2–3 drops in the morning before sunscreen",
    "side_effects": "Mild tingling for sensitive skin",
    "price": "₹699"
}


def main():
    """Main execution function"""
    
    # Load environment variables
    load_dotenv()
    
    # Import config to check which API is being used
    try:
        from config import USE_OPENROUTER, API_KEY, MODEL_NAME
        
        # Validate API key exists
        if not API_KEY:
            if USE_OPENROUTER:
                print("❌ ERROR: OPENROUTER_API_KEY not found in environment")
                print("Please create a .env file with your OpenRouter API key")
                print("Get a FREE key at: https://openrouter.ai/keys")
                print("Example: OPENROUTER_API_KEY=sk-or-v1-...")
            else:
                print("❌ ERROR: OPENAI_API_KEY not found in environment")
                print("Please create a .env file with your OpenAI API key")
                print("Example: OPENAI_API_KEY=sk-...")
            sys.exit(1)
        
        # Show configuration
        api_name = "OpenRouter (FREE)" if USE_OPENROUTER else "OpenAI (PAID)"
        print(f"\n🔑 API: {api_name}")
        print(f"🤖 Model: {MODEL_NAME}")
        
    except Exception as e:
        print(f"❌ ERROR: Failed to load configuration: {e}")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("🚀 KASPARRO DYNAMIC MULTI-AGENT SYSTEM")
    print("="*70)
    print("\n📦 Input Product:")
    print(f"  • {PRODUCT_DATA['product_name']}")
    print(f"  • {PRODUCT_DATA['concentration']}")
    print(f"  • Price: {PRODUCT_DATA['price']}")
    print()
    
    try:
        # Create dynamic orchestrator
        orchestrator = DynamicOrchestrator()
        
        print("\n" + "="*70)
        print("📋 REGISTERING AUTONOMOUS AGENTS")
        print("="*70 + "\n")
        
        # Register all autonomous agents
        # Note: Order doesn't matter - orchestrator figures it out!
        orchestrator.register_agent(AutonomousDataParserAgent())
        orchestrator.register_agent(AutonomousQuestionGeneratorAgent())
        orchestrator.register_agent(BenefitsProcessorAgent())
        orchestrator.register_agent(IngredientsProcessorAgent())
        orchestrator.register_agent(UsageProcessorAgent())
        orchestrator.register_agent(SafetyProcessorAgent())
        orchestrator.register_agent(FAQTemplateAgent())
        orchestrator.register_agent(ProductPageTemplateAgent())
        orchestrator.register_agent(ComparisonTemplateAgent())
        
        # Execute workflow dynamically
        # Agents will self-organize based on dependencies
        initial_state = {"raw_product_data": PRODUCT_DATA}
        final_state = orchestrator.execute(initial_state)
        
        # Extract outputs
        outputs = {}
        
        # Get FAQ page
        if 'fill_template' in final_state:
            template_result = final_state['fill_template']
            if 'faq_page' in template_result:
                outputs['faq'] = template_result['faq_page']
            if 'product_page' in template_result:
                outputs['product_page'] = template_result['product_page']
            if 'comparison_page' in template_result:
                outputs['comparison_page'] = template_result['comparison_page']
        
        # Save outputs
        print("\n" + "="*70)
        print("💾 SAVING OUTPUTS")
        print("="*70 + "\n")
        
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        for page_type, data in outputs.items():
            filename = f"{page_type}.json"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"  ✓ Saved: {filepath}")
        
        # Visualize execution
        orchestrator.visualize_execution()
        
        print("\n" + "="*70)
        print("✅ SUCCESS! Dynamic Multi-Agent System Complete")
        print("="*70)
        print("\n📁 Output files:")
        print("  • output/faq.json")
        print("  • output/product_page.json")
        print("  • output/comparison_page.json")
        print("\n🎉 All pages generated successfully!\n")
        
    except Exception as e:
        print("\n" + "="*70)
        print("❌ ERROR OCCURRED")
        print("="*70)
        print(f"\n{str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
