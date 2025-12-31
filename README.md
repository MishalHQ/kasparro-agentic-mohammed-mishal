# Kasparro Dynamic Multi-Agent System

🤖 **A true autonomous multi-agent system with dynamic coordination and message-based communication**

## 🎯 Overview

This project implements a **production-grade dynamic multi-agent system** where agents are truly autonomous, communicate via messages, and self-organize based on capabilities and dependencies. Unlike traditional hard-coded workflows, this system demonstrates genuine agent autonomy and dynamic coordination.

## ✨ Key Features

- ✅ **True Agent Autonomy** - Agents make independent decisions
- ✅ **Dynamic Coordination** - No hard-coded execution order
- ✅ **Message-Based Communication** - Agents communicate via message bus
- ✅ **Capability-Driven Execution** - Agents execute when dependencies are satisfied
- ✅ **Parallel Execution** - Multiple agents can run simultaneously
- ✅ **Flexible Architecture** - Easy to add/remove agents without code changes

## 🏗️ Architecture

### Dynamic Multi-Agent System

**Core Components:**
- **MessageBus**: Central communication hub for agent messages
- **AgentRegistry**: Tracks agent capabilities and dependencies
- **DynamicOrchestrator**: Coordinates agents without hard-coding
- **AutonomousAgent**: Base class for all independent agents

**Autonomous Agents:**
1. **DataParserAgent** - Parses raw product data
2. **QuestionGeneratorAgent** - Generates categorized questions
3. **BenefitsProcessorAgent** - Processes product benefits
4. **IngredientsProcessorAgent** - Analyzes ingredients
5. **UsageProcessorAgent** - Creates usage instructions
6. **SafetyProcessorAgent** - Processes safety information
7. **FAQTemplateAgent** - Fills FAQ template
8. **ProductPageTemplateAgent** - Fills product page template
9. **ComparisonTemplateAgent** - Fills comparison template

### How It Works

```
1. Agents register their capabilities and dependencies
2. Orchestrator finds agents with satisfied dependencies
3. Agents execute in natural order (discovered at runtime!)
4. Results are broadcast via message bus
5. Process repeats until all agents complete
```

**Example Execution Flow:**
```
Iteration 1: data_parser (no dependencies)
Iteration 2: question_generator, benefits_processor, ingredients_processor, 
             usage_processor, safety_processor (all need parse_data)
Iteration 3: faq_template_filler, product_page_template_filler, 
             comparison_template_filler (need various dependencies)
```

## 📦 Generated Outputs

The system autonomously generates:
1. **FAQ Page** (`output/faq.json`) - 15+ categorized Q&As with answers
2. **Product Page** (`output/product_page.json`) - Complete product details
3. **Comparison Page** (`output/comparison_page.json`) - Product comparison analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenRouter API key (FREE) or OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/MishalHQ/kasparro-agentic-mohammed-mishal.git
cd kasparro-agentic-mohammed-mishal

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API key to .env:
# OPENROUTER_API_KEY=sk-or-v1-... (FREE - get at https://openrouter.ai/keys)
# OR
# OPENAI_API_KEY=sk-... (PAID)
```

### Running the System

**Option 1: Dynamic Multi-Agent System (Recommended)**
```bash
python main_dynamic.py
```

This uses the new autonomous agents with dynamic orchestration.

**Option 2: Legacy System (For Comparison)**
```bash
python main.py
```

This uses the old hard-coded approach.

## 📁 Project Structure

```
kasparro-agentic-mohammed-mishal/
├── agents/
│   ├── autonomous/              # New autonomous agents
│   │   ├── data_parser_agent.py
│   │   ├── question_generator_agent.py
│   │   ├── content_processor_agents.py
│   │   └── template_filler_agents.py
│   └── [legacy agents]          # Old hard-coded agents
├── orchestrator/
│   ├── agent_protocol.py        # Message bus & communication
│   ├── autonomous_agent.py      # Base autonomous agent class
│   ├── dynamic_orchestrator.py  # Dynamic coordination
│   └── dag_orchestrator.py      # Legacy orchestrator
├── content_blocks/              # Reusable content logic
├── templates/                   # Template definitions
├── models/                      # Data models
├── output/                      # Generated JSON files
├── docs/
│   ├── DYNAMIC_ARCHITECTURE.md  # Architecture documentation
│   └── projectdocumentation.md  # Original documentation
├── tests/                       # Unit tests
├── main_dynamic.py              # New dynamic entry point
├── main.py                      # Legacy entry point
└── config.py                    # Configuration
```

## 📚 Documentation

- **[Dynamic Architecture](docs/DYNAMIC_ARCHITECTURE.md)** - Comprehensive guide to the new system
- **[Project Documentation](docs/projectdocumentation.md)** - Original design documentation
- **[Submission Checklist](SUBMISSION_CHECKLIST.md)** - Assignment requirements

## 🔑 Key Differences from Hard-Coded Approach

| Aspect | Hard-Coded (Old) | Dynamic (New) |
|--------|------------------|---------------|
| **Execution Order** | Fixed in code | Discovered at runtime |
| **Agent Addition** | Requires code changes | Just register new agent |
| **Parallelization** | Manual coordination | Automatic |
| **Dependencies** | Implicit in code | Explicit declarations |
| **Communication** | Direct function calls | Message bus |
| **Flexibility** | Rigid | Highly flexible |

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=agents --cov=orchestrator
```

## 🛠️ Technology Stack

- **Python 3.10+**
- **Agent Framework**: Custom autonomous agent implementation
- **LLM**: OpenRouter (NVIDIA Nemotron - FREE) or OpenAI GPT-4
- **Orchestration**: Dynamic message-based coordination
- **Communication**: Custom message bus protocol

## 🎓 Assignment Requirements Met

✅ **Clear separation of agent responsibilities**
- Each agent has specific capabilities
- No overlap in functionality

✅ **Dynamic agent interaction and coordination**
- Message-based communication
- No hard-coded calls between agents

✅ **Architecture supports agent autonomy**
- Agents check their own dependencies
- Agents decide when to execute
- Orchestrator doesn't dictate order

✅ **Not static control flow**
- Execution order emerges from dependencies
- Can add/remove agents dynamically
- Parallel execution where possible

## 🚀 Adding New Agents

To add a new agent:

1. **Create Agent Class**:
```python
from orchestrator.autonomous_agent import AutonomousAgent
from orchestrator.agent_protocol import AgentCapability

class MyNewAgent(AutonomousAgent):
    def __init__(self):
        super().__init__(
            agent_id="my_new_agent",
            capabilities=[AgentCapability.MY_CAPABILITY],
            dependencies=[AgentCapability.PARSE_DATA]
        )
    
    def process(self, shared_state):
        # Your logic here
        return {"my_result": result}
```

2. **Register in main_dynamic.py**:
```python
orchestrator.register_agent(MyNewAgent())
```

That's it! The orchestrator handles the rest.

## 📄 License

MIT License

## 👤 Author

**M A Mohammed Mishal**
- GitHub: [@MishalHQ](https://github.com/MishalHQ)
- Email: mohammedmishal2004@gmail.com

---

Built for **Kasparro Applied AI Engineer Challenge** 🚀

**Note**: This project demonstrates a true multi-agent system with autonomous agents, dynamic coordination, and message-based communication - not just hard-coded functions labeled as "agents".
