"""
Main Entry Point
Runs the complete multi-agent content generation system
"""
import os
import sys
from dotenv import load_dotenv
from orchestrator.dag_orchestrator import DAGOrchestrator


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
        from config import USE_OPENROUTER, API_KEY
        
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
        
        # Show which API is being used
        api_name = "OpenRouter (FREE)" if USE_OPENROUTER else "OpenAI (PAID)"
        print(f"\n🔑 Using API: {api_name}")
        
    except Exception as e:
        print(f"❌ ERROR: Failed to load configuration: {e}")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🤖 KASPARRO MULTI-AGENT CONTENT GENERATION SYSTEM")
    print("="*60)
    print("\n📦 Input Product:")
    print(f"  • {PRODUCT_DATA['product_name']}")
    print(f"  • {PRODUCT_DATA['concentration']}")
    print(f"  • Price: {PRODUCT_DATA['price']}")
    print()
    
    try:
        # Initialize orchestrator
        orchestrator = DAGOrchestrator()
        
        # Execute workflow
        outputs = orchestrator.execute(PRODUCT_DATA)
        
        # Save outputs
        print("\n💾 Saving outputs...")
        orchestrator.save_outputs(outputs)
        
        print("\n" + "="*60)
        print("✅ SUCCESS! All pages generated successfully")
        print("="*60)
        print("\n📁 Output files:")
        print("  • output/faq.json")
        print("  • output/product_page.json")
        print("  • output/comparison_page.json")
        print("\n🎉 System execution complete!\n")
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ ERROR OCCURRED")
        print("="*60)
        print(f"\n{str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
