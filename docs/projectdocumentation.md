# Project Documentation

## Problem Statement

Design and implement a modular agentic automation system that takes a small product dataset and automatically generates structured, machine-readable content pages.

### Core Challenge
Transform raw product data into multiple content formats (FAQ, Product Page, Comparison Page) through autonomous agent orchestration without external data sources or manual intervention.

### Key Requirements
- Multi-agent workflow with clear boundaries
- Automation graph/orchestration
- Reusable content logic blocks
- Template-based generation
- Structured JSON output
- System abstraction & modularity

---

## Solution Overview

### High-Level Architecture

This system implements a **DAG-based multi-agent orchestration** pattern where specialized agents collaborate to transform product data into structured content.

```
Input Data → DataParser → QuestionGenerator → ContentLogic → TemplateEngine → JSON Output
                ↓              ↓                  ↓              ↓
           Orchestrator (Coordinates all agents via DAG)
```

### Core Components

1. **Agents** - Autonomous units with single responsibilities
2. **Content Blocks** - Reusable transformation logic
3. **Templates** - Structured content definitions
4. **Orchestrator** - DAG-based workflow coordinator
5. **Data Models** - Type-safe data structures

---

## Scopes & Assumptions

### In Scope
✅ Parse single product data structure  
✅ Generate 15+ categorized questions automatically  
✅ Create 3 distinct page types (FAQ, Product, Comparison)  
✅ Implement custom template engine  
✅ Build reusable content logic blocks  
✅ Output machine-readable JSON  
✅ Agent-based modular architecture  
✅ DAG orchestration flow  

### Out of Scope
❌ External data fetching or web scraping  
❌ UI/Frontend implementation  
❌ Database persistence  
❌ Real-time user interaction  
❌ Multi-product batch processing (extensible for future)  
❌ Content quality scoring/validation beyond structure  

### Assumptions
- Product data follows the specified schema
- LLM API (OpenAI) is available and configured
- Single product processing per execution
- Fictional Product B for comparison is system-generated
- English language content only
- JSON output is the final deliverable (no HTML/CSS)

---

## System Design

### 1. Architecture Pattern: Multi-Agent DAG Orchestration

**Design Philosophy:**
- **Separation of Concerns**: Each agent has ONE clear responsibility
- **Composability**: Agents can be reused, replaced, or extended
- **Deterministic Flow**: DAG ensures predictable execution order
- **State Isolation**: No shared global state between agents

### 2. Agent Design

#### 2.1 DataParserAgent
**Responsibility:** Parse and validate raw product data

**Input:**
```python
{
    "product_name": str,
    "concentration": str,
    "skin_type": str,
    "key_ingredients": str,
    "benefits": str,
    "how_to_use": str,
    "side_effects": str,
    "price": str
}
```

**Output:**
```python
ProductModel(
    name: str,
    concentration: str,
    skin_types: List[str],
    ingredients: List[str],
    benefits: List[str],
    usage_instructions: str,
    side_effects: str,
    price: float,
    currency: str
)
```

**Logic:**
- Validates required fields
- Normalizes data types
- Splits comma-separated values into lists
- Extracts numeric price and currency

---

#### 2.2 QuestionGeneratorAgent
**Responsibility:** Generate categorized user questions from product data

**Input:** `ProductModel`

**Output:**
```python
List[Question(
    id: str,
    category: str,
    question: str,
    priority: int
)]
```

**Categories:**
1. **Informational** - What is this product?
2. **Safety** - Is it safe for my skin?
3. **Usage** - How do I use it?
4. **Purchase** - Where can I buy it?
5. **Comparison** - How does it compare?
6. **Ingredients** - What's inside?
7. **Benefits** - What results can I expect?

**Logic:**
- Uses LLM to generate contextual questions
- Ensures minimum 15 questions across categories
- Assigns priority based on user intent
- Validates question uniqueness

---

#### 2.3 ContentLogicAgent
**Responsibility:** Apply reusable content transformation blocks

**Content Blocks Implemented:**

1. **BenefitsBlock**
   - Expands benefit keywords into detailed descriptions
   - Maps benefits to skin concerns
   - Generates benefit-focused copy

2. **IngredientsBlock**
   - Explains ingredient functions
   - Highlights key active ingredients
   - Generates ingredient-focused copy

3. **UsageBlock**
   - Formats usage instructions
   - Adds contextual tips
   - Generates step-by-step guides

4. **SafetyBlock**
   - Processes side effects
   - Generates safety warnings
   - Creates precaution lists

5. **ComparisonBlock**
   - Compares two products
   - Highlights differences
   - Generates comparison tables

**Input:** `ProductModel` + `block_type`

**Output:** `Dict[str, Any]` (processed content)

---

#### 2.4 TemplateEngineAgent
**Responsibility:** Fill templates with processed content

**Templates Defined:**

**FAQ Template:**
```python
{
    "page_type": "faq",
    "product_name": str,
    "total_questions": int,
    "categories": List[str],
    "questions": List[{
        "id": str,
        "category": str,
        "question": str,
        "answer": str,
        "priority": int
    }],
    "metadata": {...}
}
```

**Product Page Template:**
```python
{
    "page_type": "product",
    "product": {
        "name": str,
        "tagline": str,
        "description": str,
        "price": {...},
        "key_features": [...],
        "ingredients": {...},
        "benefits": {...},
        "usage": {...},
        "safety": {...}
    },
    "metadata": {...}
}
```

**Comparison Page Template:**
```python
{
    "page_type": "comparison",
    "products": [
        {"name": str, "details": {...}},
        {"name": str, "details": {...}}
    ],
    "comparison_matrix": {...},
    "recommendation": str,
    "metadata": {...}
}
```

**Input:** `template_type` + `processed_data`

**Output:** Filled template as JSON

---

#### 2.5 OrchestratorAgent
**Responsibility:** Coordinate entire workflow via DAG

**DAG Structure:**
```
START
  ↓
DataParser
  ↓
  ├─→ QuestionGenerator → ContentLogic (FAQ) → TemplateEngine (FAQ) → faq.json
  ├─→ ContentLogic (Product) → TemplateEngine (Product) → product_page.json
  └─→ ContentLogic (Comparison) → TemplateEngine (Comparison) → comparison_page.json
  ↓
END
```

**Execution Flow:**
1. Parse product data
2. Fork into 3 parallel branches
3. Each branch processes independently
4. Collect all outputs
5. Write JSON files

**State Management:**
- Maintains execution context
- Tracks agent completion status
- Handles errors gracefully
- Logs execution trace

---

### 3. Data Models

**ProductModel:**
```python
@dataclass
class ProductModel:
    name: str
    concentration: str
    skin_types: List[str]
    ingredients: List[str]
    benefits: List[str]
    usage_instructions: str
    side_effects: str
    price: float
    currency: str
    
    def to_dict(self) -> Dict[str, Any]: ...
    def validate(self) -> bool: ...
```

**Question:**
```python
@dataclass
class Question:
    id: str
    category: str
    question: str
    priority: int
    answer: Optional[str] = None
```

**ContentBlock:**
```python
@dataclass
class ContentBlock:
    block_type: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    metadata: Dict[str, Any]
```

---

### 4. Content Logic Blocks (Reusable)

**Design Pattern:** Strategy Pattern

Each block implements:
```python
class ContentBlockInterface:
    def process(self, product: ProductModel) -> Dict[str, Any]:
        raise NotImplementedError
```

**Example: BenefitsBlock**
```python
class BenefitsBlock(ContentBlockInterface):
    def process(self, product: ProductModel) -> Dict[str, Any]:
        return {
            "primary_benefits": self._extract_primary(product.benefits),
            "detailed_benefits": self._expand_benefits(product.benefits),
            "benefit_timeline": self._generate_timeline(product.benefits),
            "skin_concerns_addressed": self._map_to_concerns(product.benefits)
        }
```

**Reusability:**
- Blocks are independent and composable
- Can be used across different templates
- Easy to test in isolation
- Extensible for new content types

---

### 5. Template Engine Design

**Architecture:**

```python
class TemplateEngine:
    def __init__(self):
        self.templates = self._load_templates()
        self.validators = self._load_validators()
    
    def fill_template(self, template_type: str, data: Dict) -> Dict:
        template = self.templates[template_type]
        filled = self._recursive_fill(template, data)
        self._validate_output(filled, template_type)
        return filled
```

**Features:**
- Schema-based validation
- Recursive field filling
- Default value handling
- Type checking
- Missing field detection

---

### 6. Orchestration Flow

**Implementation: DAG Executor**

```python
class DAGOrchestrator:
    def __init__(self):
        self.graph = self._build_dag()
        self.state = ExecutionState()
    
    def execute(self, input_data: Dict) -> Dict[str, Any]:
        # Topological sort for execution order
        execution_order = self._topological_sort(self.graph)
        
        for node in execution_order:
            agent = self._get_agent(node)
            result = agent.execute(self.state.get_context())
            self.state.update(node, result)
        
        return self.state.get_outputs()
```

**Benefits:**
- Parallel execution where possible
- Dependency resolution
- Error isolation
- Execution tracing

---

### 7. System Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR                             │
│                   (DAG Coordinator)                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    ┌───────────────┐
                    │ DataParser    │
                    │ Agent         │
                    └───────────────┘
                            ↓
                    [ProductModel]
                            ↓
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Question      │   │ ContentLogic  │   │ ContentLogic  │
│ Generator     │   │ Agent         │   │ Agent         │
│ Agent         │   │ (Product)     │   │ (Comparison)  │
└───────────────┘   └───────────────┘   └───────────────┘
        ↓                   ↓                   ↓
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ ContentLogic  │   │ TemplateEngine│   │ TemplateEngine│
│ Agent (FAQ)   │   │ Agent         │   │ Agent         │
└───────────────┘   └───────────────┘   └───────────────┘
        ↓                   ↓                   ↓
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ TemplateEngine│   │ product_page  │   │ comparison    │
│ Agent         │   │ .json         │   │ _page.json    │
└───────────────┘   └───────────────┘   └───────────────┘
        ↓
┌───────────────┐
│ faq.json      │
└───────────────┘
```

---

### 8. Key Design Decisions

**1. Why DAG over Sequential Pipeline?**
- Enables parallel execution (FAQ, Product, Comparison can run simultaneously)
- Clear dependency visualization
- Easy to extend with new branches
- Better error isolation

**2. Why Custom Template Engine vs Jinja2?**
- Full control over validation logic
- Type-safe template definitions
- Better integration with data models
- No external template syntax to learn

**3. Why Content Blocks over Monolithic Functions?**
- Reusability across templates
- Easier testing
- Single Responsibility Principle
- Composable logic

**4. Why Dataclasses over Dicts?**
- Type safety
- IDE autocomplete
- Validation at instantiation
- Clear contracts

---

### 9. Extensibility

**Adding New Page Types:**
1. Define template schema in `templates/`
2. Create content blocks if needed
3. Add branch to DAG
4. Register in orchestrator

**Adding New Content Blocks:**
1. Implement `ContentBlockInterface`
2. Add to `content_blocks/` directory
3. Register in `ContentLogicAgent`

**Adding New Agents:**
1. Inherit from `BaseAgent`
2. Implement `execute()` method
3. Add to DAG graph
4. Define dependencies

---

### 10. Testing Strategy

**Unit Tests:**
- Each agent tested in isolation
- Content blocks tested independently
- Template validation tests
- Data model validation tests

**Integration Tests:**
- End-to-end workflow tests
- DAG execution tests
- Output JSON validation

**Test Coverage Target:** >80%

---

### 11. Performance Considerations

**Optimization Strategies:**
- Parallel agent execution where possible
- LLM call batching
- Response caching for repeated queries
- Lazy loading of templates

**Expected Performance:**
- Single product processing: <30 seconds
- Majority of time: LLM API calls
- Local processing: <2 seconds

---

### 12. Error Handling

**Strategy:**
- Graceful degradation
- Detailed error logging
- Retry logic for LLM calls
- Validation at each stage

**Error Types:**
- Data validation errors
- LLM API errors
- Template filling errors
- File I/O errors

---

## Conclusion

This system demonstrates production-grade multi-agent architecture with:
- ✅ Clear separation of concerns
- ✅ Modular, testable components
- ✅ Extensible design
- ✅ Type-safe implementations
- ✅ Comprehensive documentation

The architecture is designed to scale from single-product processing to batch operations with minimal modifications.

---

**Author:** M A Mohammed Mishal  
**Date:** December 2025  
**Challenge:** Kasparro Applied AI Engineer Assignment