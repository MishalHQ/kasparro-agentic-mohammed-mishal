# System Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│                        ORCHESTRATOR LAYER                            │
│                     (DAG-Based Coordination)                         │
│                                                                       │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│                          AGENT LAYER                                 │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  DataParser  │  │  Question    │  │ ContentLogic │              │
│  │    Agent     │  │  Generator   │  │    Agent     │              │
│  │              │  │    Agent     │  │              │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
│  ┌──────────────────────────────────────────────────┐               │
│  │         TemplateEngine Agent                     │               │
│  │                                                   │               │
│  └──────────────────────────────────────────────────┘               │
│                                                                       │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      CONTENT BLOCKS LAYER                            │
│                   (Reusable Transformation Logic)                    │
│                                                                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │Benefits │  │Ingredi- │  │  Usage  │  │ Safety  │  │Compari- │  │
│  │  Block  │  │  ents   │  │  Block  │  │  Block  │  │  son    │  │
│  │         │  │  Block  │  │         │  │         │  │  Block  │  │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │
│                                                                       │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│                       TEMPLATE LAYER                                 │
│                   (Structured Schemas)                               │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │     FAQ      │  │   Product    │  │  Comparison  │              │
│  │   Template   │  │   Template   │  │   Template   │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA MODEL LAYER                              │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ ProductModel │  │   Question   │  │ ContentBlock │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Execution Flow (DAG)

```
                        START
                          │
                          ↓
                  ┌───────────────┐
                  │  Raw Product  │
                  │     Data      │
                  └───────────────┘
                          │
                          ↓
                  ┌───────────────┐
                  │  DataParser   │
                  │     Agent     │
                  └───────────────┘
                          │
                          ↓
                  ┌───────────────┐
                  │ ProductModel  │
                  └───────────────┘
                          │
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │Question │    │Content  │    │Content  │
    │Generator│    │Logic    │    │Logic    │
    │         │    │(Product)│    │(Compare)│
    └─────────┘    └─────────┘    └─────────┘
          │               │               │
          ↓               ↓               ↓
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │Content  │    │Template │    │Template │
    │Logic    │    │Engine   │    │Engine   │
    │(FAQ)    │    │(Product)│    │(Compare)│
    └─────────┘    └─────────┘    └─────────┘
          │               │               │
          ↓               ↓               ↓
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │Template │    │product_ │    │compari- │
    │Engine   │    │page.json│    │son_page │
    │(FAQ)    │    │         │    │.json    │
    └─────────┘    └─────────┘    └─────────┘
          │
          ↓
    ┌─────────┐
    │faq.json │
    └─────────┘
          │
          ↓
        END
```

## Agent Interaction Sequence

```
User/System
    │
    │ 1. Provide Product Data
    ↓
Orchestrator
    │
    │ 2. Initialize Context
    ↓
DataParserAgent
    │
    │ 3. Parse & Validate
    ↓
ProductModel ────────────────────────────────┐
    │                                        │
    │ 4. Generate Questions                  │ 5. Process Content
    ↓                                        ↓
QuestionGeneratorAgent              ContentLogicAgent
    │                                        │
    │ (Uses LLM)                            │ (Applies Blocks)
    ↓                                        ↓
Questions List                      Processed Content
    │                                        │
    │ 6. Fill FAQ Template                   │ 7. Fill Product/Comparison
    ↓                                        ↓
TemplateEngineAgent ←────────────────────────┘
    │
    │ 8. Validate & Generate
    ↓
JSON Output Files
    │
    │ 9. Save to Disk
    ↓
output/
├── faq.json
├── product_page.json
└── comparison_page.json
```

## Content Block Processing

```
ProductModel
    │
    ├──→ BenefitsBlock ──→ {primary_benefit, detailed_benefits, timeline}
    │
    ├──→ IngredientsBlock ──→ {key_actives, synergy, combinations}
    │
    ├──→ UsageBlock ──→ {steps, timing, tips, pair_with, avoid_with}
    │
    ├──→ SafetyBlock ──→ {side_effects, contraindications, warnings}
    │
    └──→ ComparisonBlock ──→ {differences, similarities, recommendation}
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT LAYER                               │
│                                                               │
│  Raw Product Data (Dict)                                     │
│  {                                                            │
│    "product_name": "GlowBoost Vitamin C Serum",             │
│    "concentration": "10% Vitamin C",                         │
│    "skin_type": "Oily, Combination",                        │
│    ...                                                        │
│  }                                                            │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ↓ Parse & Validate
┌─────────────────────────────────────────────────────────────┐
│                  STRUCTURED DATA LAYER                       │
│                                                               │
│  ProductModel (Dataclass)                                    │
│  - name: str                                                 │
│  - concentration: str                                        │
│  - skin_types: List[str]                                    │
│  - ingredients: List[str]                                   │
│  - benefits: List[str]                                      │
│  - price: float                                             │
│  ...                                                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ↓ Transform & Enrich
┌─────────────────────────────────────────────────────────────┐
│                 PROCESSED CONTENT LAYER                      │
│                                                               │
│  Questions: List[Question]                                   │
│  Content Blocks: Dict[str, Any]                             │
│  - benefits: {...}                                           │
│  - ingredients: {...}                                        │
│  - usage: {...}                                              │
│  - safety: {...}                                             │
│  - comparison: {...}                                         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ↓ Fill Templates
┌─────────────────────────────────────────────────────────────┐
│                   OUTPUT LAYER                               │
│                                                               │
│  JSON Files (Machine-Readable)                              │
│  - faq.json                                                  │
│  - product_page.json                                         │
│  - comparison_page.json                                      │
└─────────────────────────────────────────────────────────────┘
```

## Key Design Patterns

### 1. Strategy Pattern (Content Blocks)
```
ContentBlockInterface
    ↑
    ├── BenefitsBlock
    ├── IngredientsBlock
    ├── UsageBlock
    ├── SafetyBlock
    └── ComparisonBlock
```

### 2. Template Method Pattern (Base Agent)
```
BaseAgent
    ↑
    ├── DataParserAgent
    ├── QuestionGeneratorAgent
    ├── ContentLogicAgent
    └── TemplateEngineAgent
```

### 3. Registry Pattern (Templates)
```
TemplateRegistry
    ├── get_faq_template()
    ├── get_product_page_template()
    └── get_comparison_template()
```

### 4. State Pattern (Execution State)
```
ExecutionState
    ├── context: Dict
    ├── completed_agents: List
    ├── errors: List
    └── methods: update(), get_context(), add_error()
```

## Error Handling Flow

```
Agent Execution
    │
    ├─→ Success ──→ Update State ──→ Continue
    │
    └─→ Failure ──→ Log Error ──→ Raise Exception ──→ Stop
```

## Scalability Considerations

```
Current: Single Product Processing
    │
    ↓ Future Extension
    │
    ├─→ Batch Processing (Multiple Products)
    │
    ├─→ Parallel Agent Execution (Threading/Async)
    │
    ├─→ Caching Layer (Redis/Memcached)
    │
    ├─→ Queue System (Celery/RabbitMQ)
    │
    └─→ API Layer (FastAPI/Flask)
```

---

**Legend:**
- `│` : Sequential flow
- `├─→` : Branch/Fork
- `↓` : Data transformation
- `┌─┐` : Component boundary
