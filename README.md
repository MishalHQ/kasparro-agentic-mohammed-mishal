# Kasparro Multi-Agent Content Generation System

🤖 **A modular agentic automation system for structured content generation**

## 🎯 Overview

This project implements a production-grade multi-agent system that transforms product data into structured, machine-readable content pages through autonomous agent orchestration.

## 🏗️ System Architecture

**Agent-Based Design:**
- **DataParserAgent**: Parses and validates product data
- **QuestionGeneratorAgent**: Generates categorized user questions
- **ContentLogicAgent**: Applies reusable content transformation blocks
- **TemplateEngineAgent**: Fills templates with processed data
- **OrchestratorAgent**: Coordinates the entire workflow via DAG

**Key Features:**
- ✅ Modular agent boundaries with single responsibilities
- ✅ DAG-based orchestration flow
- ✅ Reusable content logic blocks
- ✅ Custom template engine
- ✅ Machine-readable JSON output
- ✅ Zero external data dependencies

## 📦 Generated Outputs

The system autonomously generates:
1. **FAQ Page** (`output/faq.json`) - 15+ categorized Q&As
2. **Product Page** (`output/product_page.json`) - Complete product details
3. **Comparison Page** (`output/comparison_page.json`) - Product comparison analysis

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/MishalHQ/kasparro-agentic-mohammed-mishal.git
cd kasparro-agentic-mohammed-mishal

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your OpenAI API key to .env

# Run the system
python main.py
```

## 📁 Project Structure

```
kasparro-agentic-mohammed-mishal/
├── agents/              # Individual agent implementations
├── content_blocks/      # Reusable content logic blocks
├── templates/           # Template definitions
├── orchestrator/        # Workflow orchestration
├── models/              # Data models
├── output/              # Generated JSON files
├── docs/                # Documentation
├── tests/               # Unit tests
└── main.py              # Entry point
```

## 📚 Documentation

Complete system design and architecture documentation: [docs/projectdocumentation.md](docs/projectdocumentation.md)

## 🧪 Testing

```bash
pytest tests/
```

## 🛠️ Technology Stack

- **Python 3.10+**
- **Agent Framework**: Custom implementation
- **LLM**: OpenAI GPT-4
- **Orchestration**: DAG-based state machine

## 📄 License

MIT License

## 👤 Author

**M A Mohammed Mishal**
- GitHub: [@MishalHQ](https://github.com/MishalHQ)
- Email: mohammedmishal2004@gmail.com

---

Built for **Kasparro Applied AI Engineer Challenge** 🚀
