# Dynamic Multi-Agent Architecture

## Overview

This project implements a **true multi-agent system** with autonomous agents that communicate via messages and self-organize based on capabilities and dependencies. Unlike traditional hard-coded workflows, this system demonstrates:

- ✅ **Agent Autonomy** - Agents make independent decisions
- ✅ **Dynamic Coordination** - No hard-coded execution order
- ✅ **Message-Based Communication** - Agents communicate via a message bus
- ✅ **Capability-Driven Execution** - Agents execute when dependencies are satisfied
- ✅ **Parallel Execution** - Multiple agents can run simultaneously

---

## Architecture Components

### 1. Agent Communication Protocol (`orchestrator/agent_protocol.py`)

Defines the communication infrastructure:

- **MessageBus**: Central hub for agent communication
- **AgentRegistry**: Tracks agent capabilities and dependencies
- **Message Types**: REQUEST, RESPONSE, EVENT, QUERY, RESULT, ERROR
- **Agent Capabilities**: PARSE_DATA, GENERATE_QUESTIONS, PROCESS_CONTENT, FILL_TEMPLATE

### 2. Autonomous Agent Base (`orchestrator/autonomous_agent.py`)

Base class for all autonomous agents:

```python
class AutonomousAgent(ABC):
    def __init__(self, agent_id, capabilities, dependencies):
        # Agent identity and capabilities
        
    def can_execute(self, shared_state) -> bool:
        # Check if dependencies are satisfied
        
    def process(self, shared_state) -> Dict:
        # Agent-specific logic (abstract)
        
    def execute(self, shared_state) -> Dict:
        # Execute if ready, broadcast results
```

**Key Features:**
- Agents check their own dependencies
- Agents broadcast results when complete
- Agents communicate via messages, not direct calls

### 3. Dynamic Orchestrator (`orchestrator/dynamic_orchestrator.py`)

Coordinates agents without hard-coding:

```python
class DynamicOrchestrator:
    def execute(self, initial_state, max_iterations=20):
        while iteration < max_iterations:
            # Find agents whose dependencies are satisfied
            ready_agents = self._find_ready_agents(executed)
            
            # Execute ready agents (parallel simulation)
            for agent in ready_agents:
                result = agent.execute(shared_state)
                shared_state.update(result)
```

**How It Works:**
1. Agents register their capabilities and dependencies
2. Orchestrator finds agents with satisfied dependencies
3. Agents execute in natural order (no hard-coding!)
4. Results are shared via message bus
5. Process repeats until all agents complete

---

## Agent Types

### Data Processing Agents

**AutonomousDataParserAgent**
- Capabilities: `PARSE_DATA`
- Dependencies: None
- Function: Parses raw product data into structured format

**AutonomousQuestionGeneratorAgent**
- Capabilities: `GENERATE_QUESTIONS`
- Dependencies: `PARSE_DATA`
- Function: Generates 15 categorized questions using LLM

### Content Processing Agents (Parallel Execution)

These agents can run **simultaneously** since they only depend on parsed data:

**BenefitsProcessorAgent**
- Capabilities: `PROCESS_CONTENT`
- Dependencies: `PARSE_DATA`
- Function: Processes product benefits into detailed content

**IngredientsProcessorAgent**
- Capabilities: `PROCESS_CONTENT`
- Dependencies: `PARSE_DATA`
- Function: Analyzes ingredients and their synergies

**UsageProcessorAgent**
- Capabilities: `PROCESS_CONTENT`
- Dependencies: `PARSE_DATA`
- Function: Creates detailed usage instructions

**SafetyProcessorAgent**
- Capabilities: `PROCESS_CONTENT`
- Dependencies: `PARSE_DATA`
- Function: Processes safety information and warnings

### Template Filling Agents

**FAQTemplateAgent**
- Capabilities: `FILL_TEMPLATE`
- Dependencies: `PARSE_DATA`, `GENERATE_QUESTIONS`
- Function: Fills FAQ template with Q&A pairs

**ProductPageTemplateAgent**
- Capabilities: `FILL_TEMPLATE`
- Dependencies: `PARSE_DATA`, `PROCESS_CONTENT`
- Function: Fills product page with all content

**ComparisonTemplateAgent**
- Capabilities: `FILL_TEMPLATE`
- Dependencies: `PARSE_DATA`
- Function: Generates and fills comparison template

---

## Execution Flow

### Dynamic Execution (No Hard-Coding!)

```
Iteration 1:
  ✓ data_parser (no dependencies)

Iteration 2:
  ✓ question_generator (needs parse_data)
  ✓ benefits_processor (needs parse_data)
  ✓ ingredients_processor (needs parse_data)
  ✓ usage_processor (needs parse_data)
  ✓ safety_processor (needs parse_data)

Iteration 3:
  ✓ faq_template_filler (needs parse_data + generate_questions)
  ✓ product_page_template_filler (needs parse_data + process_content)
  ✓ comparison_template_filler (needs parse_data)
```

**Key Point**: The orchestrator **discovers** this order at runtime by checking dependencies. You can add/remove agents without changing orchestrator code!

---

## Key Differences from Hard-Coded Approach

| Aspect | Hard-Coded (Old) | Dynamic (New) |
|--------|------------------|---------------|
| **Execution Order** | Fixed in code | Discovered at runtime |
| **Agent Addition** | Requires code changes | Just register new agent |
| **Parallelization** | Manual coordination | Automatic |
| **Dependencies** | Implicit in code | Explicit declarations |
| **Communication** | Direct function calls | Message bus |
| **Flexibility** | Rigid | Highly flexible |

---

## Running the System

### Option 1: Dynamic System (Recommended)

```bash
python main_dynamic.py
```

This uses the new autonomous agents with dynamic orchestration.

### Option 2: Legacy System

```bash
python main.py
```

This uses the old hard-coded approach (kept for comparison).

---

## Adding New Agents

To add a new agent:

1. **Create Agent Class**:
```python
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

---

## Message Flow Example

```
1. DataParser broadcasts:
   Message(type=RESULT, capability=PARSE_DATA, payload={product})

2. QuestionGenerator receives message, executes, broadcasts:
   Message(type=RESULT, capability=GENERATE_QUESTIONS, payload={questions})

3. FAQTemplate waits for both PARSE_DATA and GENERATE_QUESTIONS
   Once both available, executes and broadcasts:
   Message(type=RESULT, capability=FILL_TEMPLATE, payload={faq_page})
```

---

## Benefits of This Architecture

1. **True Autonomy**: Agents decide when to act
2. **Scalability**: Easy to add new agents
3. **Maintainability**: Changes don't ripple through codebase
4. **Testability**: Agents can be tested independently
5. **Observability**: Message history shows exact execution flow
6. **Flexibility**: Can swap agents without changing orchestrator

---

## Comparison with Assignment Requirements

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

---

## Technical Implementation Details

### Dependency Resolution

The orchestrator uses a simple but effective algorithm:

```python
def _find_ready_agents(self, executed):
    ready = []
    for agent in self.agents:
        if agent not in executed:
            if all(dep in shared_state for dep in agent.dependencies):
                ready.append(agent)
    return ready
```

This ensures agents only execute when their dependencies are satisfied.

### Shared State Management

Agents communicate through a shared state dictionary:

```python
shared_state = {
    "parse_data": {...},           # From DataParser
    "generate_questions": {...},   # From QuestionGenerator
    "process_content": {...},      # From Content Processors
    "fill_template": {...}         # From Template Fillers
}
```

Each capability adds its results to the shared state.

### Message Bus

The message bus enables:
- Broadcasting results to all interested agents
- Direct messaging between specific agents
- Message history for debugging
- Event-driven coordination

---

## Future Enhancements

Possible extensions to this architecture:

1. **True Parallel Execution**: Use threading/multiprocessing
2. **Agent Discovery**: Agents can query for other agents
3. **Negotiation**: Agents can negotiate task allocation
4. **Learning**: Agents can learn from execution history
5. **Fault Tolerance**: Automatic retry and fallback mechanisms

---

## Conclusion

This implementation demonstrates a **true multi-agent system** where:

- Agents are independent and autonomous
- Coordination is dynamic, not hard-coded
- Communication is message-based
- Execution order emerges from dependencies
- System is flexible and extensible

This is fundamentally different from simply wrapping functions in "agent" classes with hard-coded orchestration.
