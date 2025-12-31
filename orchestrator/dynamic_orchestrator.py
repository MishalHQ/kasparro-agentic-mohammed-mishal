"""
Dynamic Multi-Agent Orchestrator
Coordinates autonomous agents through message-based communication
No hard-coded workflows - agents self-organize based on capabilities
"""
from typing import Dict, Any, List, Set
import time
from orchestrator.agent_protocol import (
    MessageBus, AgentRegistry, AgentCapability, Message, MessageType
)
from orchestrator.autonomous_agent import AutonomousAgent


class DynamicOrchestrator:
    """
    Dynamic orchestrator that coordinates autonomous agents
    
    Key features:
    1. No hard-coded execution order
    2. Agents execute when dependencies are satisfied
    3. Parallel execution where possible
    4. Event-driven coordination
    """
    
    def __init__(self):
        self.message_bus = MessageBus()
        self.registry = AgentRegistry()
        self.agents: Dict[str, AutonomousAgent] = {}
        self.shared_state: Dict[str, Any] = {}
        self.execution_log: List[Dict[str, Any]] = []
    
    def register_agent(self, agent: AutonomousAgent):
        """Register an autonomous agent"""
        agent.register(self.message_bus)
        self.registry.register(agent.get_registration())
        self.agents[agent.agent_id] = agent
        print(f"  → {agent.agent_id} registered")
    
    def execute(self, initial_state: Dict[str, Any], max_iterations: int = 20) -> Dict[str, Any]:
        """
        Execute multi-agent workflow dynamically
        
        Args:
            initial_state: Initial shared state
            max_iterations: Maximum iterations to prevent infinite loops
            
        Returns:
            Final shared state with all results
        """
        print("\n" + "="*70)
        print("🤖 DYNAMIC MULTI-AGENT ORCHESTRATION")
        print("="*70)
        
        # Initialize shared state
        self.shared_state = initial_state.copy()
        
        # Track execution
        executed_agents: Set[str] = set()
        iteration = 0
        
        print(f"\n📊 Registered Agents: {len(self.agents)}")
        for agent_id, agent in self.agents.items():
            caps = [c.value for c in agent.capabilities]
            deps = [d.value for d in agent.dependencies]
            print(f"  • {agent_id}")
            print(f"    Capabilities: {caps}")
            print(f"    Dependencies: {deps}")
        
        print("\n" + "-"*70)
        print("🚀 Starting Dynamic Execution")
        print("-"*70 + "\n")
        
        while iteration < max_iterations:
            iteration += 1
            executed_this_round = []
            
            # Find agents that can execute
            ready_agents = self._find_ready_agents(executed_agents)
            
            if not ready_agents:
                # No more agents can execute
                break
            
            print(f"🔄 Iteration {iteration}: {len(ready_agents)} agent(s) ready")
            
            # Execute ready agents (simulated parallel execution)
            for agent_id in ready_agents:
                agent = self.agents[agent_id]
                
                try:
                    print(f"  ⚡ Executing {agent_id}...")
                    start_time = time.time()
                    
                    result = agent.execute(self.shared_state)
                    
                    execution_time = time.time() - start_time
                    
                    if result:
                        # Update shared state with results
                        # IMPORTANT: Merge results instead of overwriting
                        for capability in agent.capabilities:
                            cap_key = capability.value
                            
                            # If capability key doesn't exist, create it
                            if cap_key not in self.shared_state:
                                self.shared_state[cap_key] = {}
                            
                            # Merge the result into existing capability data
                            if isinstance(self.shared_state[cap_key], dict) and isinstance(result, dict):
                                self.shared_state[cap_key].update(result)
                            else:
                                # If not dict, just store it
                                self.shared_state[cap_key] = result
                        
                        executed_agents.add(agent_id)
                        executed_this_round.append(agent_id)
                        
                        # Log execution
                        self.execution_log.append({
                            "iteration": iteration,
                            "agent": agent_id,
                            "capabilities": [c.value for c in agent.capabilities],
                            "execution_time": execution_time,
                            "success": True
                        })
                        
                        print(f"    ✓ {agent_id} completed in {execution_time:.2f}s")
                    
                except Exception as e:
                    print(f"    ✗ {agent_id} failed: {str(e)}")
                    self.execution_log.append({
                        "iteration": iteration,
                        "agent": agent_id,
                        "error": str(e),
                        "success": False
                    })
                    raise
            
            if not executed_this_round:
                # No progress made
                break
            
            print()
        
        # Check if all agents executed
        not_executed = set(self.agents.keys()) - executed_agents
        
        print("-"*70)
        print("📊 Execution Summary")
        print("-"*70)
        print(f"  Total Iterations: {iteration}")
        print(f"  Agents Executed: {len(executed_agents)}/{len(self.agents)}")
        print(f"  Execution Order: {' → '.join([log['agent'] for log in self.execution_log if log['success']])}")
        
        if not_executed:
            print(f"  ⚠️  Not Executed: {', '.join(not_executed)}")
            print(f"     (Dependencies not satisfied)")
        
        print("\n" + "="*70)
        print("✅ ORCHESTRATION COMPLETE")
        print("="*70 + "\n")
        
        return self.shared_state
    
    def _find_ready_agents(self, executed: Set[str]) -> List[str]:
        """
        Find agents that are ready to execute
        
        Args:
            executed: Set of already executed agent IDs
            
        Returns:
            List of agent IDs ready to execute
        """
        ready = []
        
        for agent_id, agent in self.agents.items():
            # Skip if already executed
            if agent_id in executed:
                continue
            
            # Check if dependencies are satisfied
            if agent.can_execute(self.shared_state):
                ready.append(agent_id)
        
        return ready
    
    def get_execution_graph(self) -> Dict[str, Any]:
        """Get execution graph for visualization"""
        return {
            "agents": {
                agent_id: {
                    "capabilities": [c.value for c in agent.capabilities],
                    "dependencies": [d.value for d in agent.dependencies]
                }
                for agent_id, agent in self.agents.items()
            },
            "execution_log": self.execution_log,
            "message_history": [msg.to_dict() for msg in self.message_bus.get_history()]
        }
    
    def visualize_execution(self):
        """Print execution visualization"""
        print("\n" + "="*70)
        print("📈 EXECUTION VISUALIZATION")
        print("="*70 + "\n")
        
        for i, log in enumerate(self.execution_log, 1):
            if log['success']:
                print(f"{i}. {log['agent']} ({log['execution_time']:.2f}s)")
                print(f"   Capabilities: {', '.join(log['capabilities'])}")
            else:
                print(f"{i}. {log['agent']} ✗ FAILED")
                print(f"   Error: {log['error']}")
            print()
