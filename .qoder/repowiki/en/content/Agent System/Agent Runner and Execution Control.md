# Agent Runner and Execution Control

<cite>
**Referenced Files in This Document**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py)
- [agent_runner.py](file://tutorials/v1_agent_runner/agent_runner.py)
- [runner_streaming.py](file://tutorials/v1_agent_runner/runner_streaming.py)
- [agents_runner.md](file://docs/source/new_tutorials/agents_runner.md)
- [agent-streaming.md](file://docs/design/agent-streaming.md)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Dependency Analysis](#dependency-analysis)
7. [Performance Considerations](#performance-considerations)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Conclusion](#conclusion)
10. [Appendices](#appendices)

## Introduction
This document explains the Agent Runner component that orchestrates multi-step agent workflows, supporting both synchronous and asynchronous execution, streaming, and real-time event processing. It covers execution control, streaming patterns, event handling, cancellation, error handling, progress tracking, and scalability considerations. Concrete examples are drawn from the repository’s runner implementation and tutorials to help both beginners and advanced users build production-ready agent runners.

## Project Structure
The Agent Runner lives under the agent components and integrates with the Agent, ToolManager, PermissionManager, and tracing utilities. Tutorials demonstrate practical usage for synchronous and streaming execution.

```mermaid
graph TB
subgraph "Agent Components"
Agent["Agent"]
ToolManager["ToolManager"]
Planner["Planner (Generator)"]
end
subgraph "Runner"
Runner["Runner"]
PermMgr["PermissionManager"]
Mem["ConversationMemory"]
Trace["Tracing (runner_span, step_span, tool_span, response_span)"]
end
Agent --> Planner
Agent --> ToolManager
Runner --> Agent
Runner --> PermMgr
Runner --> Mem
Runner --> Trace
```

**Diagram sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L107-L135)

**Section sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L107-L135)

## Core Components
- Runner: Multi-step orchestration with planning, tool execution, and optional streaming. Supports cancellation, permission checks, conversation memory, and tracing.
- Agent: Provides a planner and tool manager; Runner delegates planning and tool execution to it.
- PermissionManager: Optional approval gate for tool calls.
- ConversationMemory: Optional memory integration for user-assistant context.
- Tracing: Spans for runner, step, tool, and response lifecycle.

Key responsibilities:
- Synchronous execution via call()
- Asynchronous execution via acall() and astream()
- Streaming event emission for raw LLM chunks, tool activities, step completions, and final outputs
- Cancellation signaling and graceful shutdown
- Error categorization (recoverable vs unrecoverable) and propagation
- Token consumption tracking and step history maintenance

**Section sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L136-L193)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L529-L826)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L877-L1202)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1205-L1664)

## Architecture Overview
The Runner coordinates a loop of planning and tool execution, emitting events and updating state. It supports:
- Synchronous mode: call()
- Asynchronous mode: acall()
- Streaming mode: astream() with event queue and cancellation-aware processing

```mermaid
sequenceDiagram
participant Client as "Caller"
participant Runner as "Runner"
participant Agent as "Agent"
participant Planner as "Planner"
participant TM as "ToolManager"
participant PM as "PermissionManager"
participant Mem as "ConversationMemory"
participant Trace as "Tracing"
Client->>Runner : call()/acall()/astream()
Runner->>Trace : enter runner_span
Runner->>Mem : optionally reset/add user query
loop Steps < max_steps and not cancelled
Runner->>Trace : enter step_span
Runner->>Planner : call()/acall()
Planner-->>Runner : GeneratorOutput
alt Final step
Runner->>Runner : process final answer
Runner->>Mem : add assistant response
Runner-->>Client : RunnerResult
else Tool call
Runner->>PM : optional permission check
Runner->>TM : execute_func()/execute_func_async()
TM-->>Runner : FunctionOutput
Runner->>Trace : update step_span/tool_span
Runner-->>Client : step_complete event (streaming)
end
end
Runner->>Trace : exit spans
```

**Diagram sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L529-L826)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L877-L1202)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1242-L1664)

## Detailed Component Analysis

### Runner Class and Execution Modes
- Initialization: binds Agent, ToolManager, optional PermissionManager and ConversationMemory; sets max_steps and answer_data_type; initializes cancellation and token tracking.
- Synchronous call(): iterates steps, calls planner, executes tools, collects step history, processes final answer, and returns RunnerResult.
- Asynchronous acall(): mirrors call() but uses async planner and tool execution, with cancellation checks.
- Streaming astream(): starts a task, emits events (raw LLM chunks, tool activity, step completion), and completes with a final output item.

```mermaid
classDiagram
class Runner {
+agent
+tool_manager
+permission_manager
+conversation_memory
+max_steps
+answer_data_type
+step_history
+ctx
+is_cancelled() bool
+reset_cancellation() void
+register_cancel_callback(cb) void
+cancel() async
+call(prompt_kwargs, model_kwargs, use_cache, id) RunnerResult
+acall(prompt_kwargs, model_kwargs, use_cache, id) RunnerResult
+astream(prompt_kwargs, model_kwargs, use_cache, id) RunnerStreamingResult
-impl_astream(...) async
-stream_tool_execution(...) async
-_tool_execute_sync(func) FunctionOutput
-_tool_execute_async(func, streaming_result) FunctionOutput
-_update_token_consumption() void
-_create_execution_complete_stream_event(...) void
-_process_stream_final_step(...) async
}
```

**Diagram sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L107-L193)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L529-L826)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L877-L1202)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1205-L1664)

**Section sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L136-L193)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L529-L826)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L877-L1202)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1205-L1664)

### Execution Control and Cancellation
- Cancellation flag and callbacks: is_cancelled(), reset_cancellation(), register_cancel_callback(), cancel().
- Streaming cancellation: raises CancelledError, emits a “runner.cancelled” event, marks result complete, and adds a memory entry.
- Task management: tracks current task to cancel previous or ongoing streaming tasks.

```mermaid
flowchart TD
Start(["Start Runner"]) --> CheckCancel["Check is_cancelled()"]
CheckCancel --> |True| EmitCancel["Emit 'runner.cancelled' event<br/>Mark result complete"]
CheckCancel --> |False| Plan["Planner call/acall"]
Plan --> ExecTool["Execute tool (sync/async)"]
ExecTool --> UpdateHistory["Append StepOutput"]
UpdateHistory --> NextIter{"More steps and not cancelled?"}
NextIter --> |Yes| CheckCancel
NextIter --> |No| Finish["Create FinalOutputItem<br/>Complete streaming"]
```

**Diagram sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L231-L316)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1561-L1598)

**Section sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L231-L316)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1561-L1598)

### Streaming Execution Patterns and Event Processing
- Raw responses: RawResponsesStreamEvent for LLM chunks.
- Tool events: agent.tool_call_start, agent.tool_call_activity, agent.tool_call_complete.
- Step events: agent.step_complete with StepRunItem.
- Final output: FinalOutputItem with RunnerResult.
- Permission events: agent.tool_permission_request when approval is required.
- Completion: QueueCompleteSentinel signals end-of-stream.

```mermaid
sequenceDiagram
participant Runner as "Runner"
participant Planner as "Planner"
participant TM as "ToolManager"
participant Q as "RunnerStreamingResult.queue"
Runner->>Planner : acall()
alt Planner streams
Planner-->>Runner : AsyncIterable chunks
Runner->>Q : RawResponsesStreamEvent(chunk)
else Planner returns data
Runner->>Q : RawResponsesStreamEvent(data)
end
Runner->>Runner : permission check (optional)
Runner->>TM : execute_func_async()
alt Tool streams
TM-->>Runner : async generator
loop for each item
Runner->>Q : agent.tool_call_activity events
end
end
Runner->>Q : agent.tool_call_complete
Runner->>Q : agent.step_complete
Runner->>Q : FinalOutputItem
Runner->>Q : QueueCompleteSentinel
```

**Diagram sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1242-L1664)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1718-L1827)

**Section sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1242-L1664)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1718-L1827)

### Progress Tracking and State Management
- Step history: List[StepOutput] captures each iteration’s action, function, and observation.
- Token consumption: Tracks total and per-step tokens via planner’s estimated_token_count.
- Conversation memory: Adds user queries and assistant responses to maintain context across runs.

```mermaid
flowchart TD
Init["Init Runner"] --> Hist["step_history=[]"]
Init --> Tokens["token_consumption={}"]
Init --> Mem["conversation_memory=None"]
loop Steps
Plan["Planner call"] --> Exec["Tool execution"]
Exec --> Obs["Extract observation"]
Obs --> Append["Append StepOutput to step_history"]
Append --> UpdateTokens["Update token counters"]
end
Append --> Finalize["Finalize with answer or error"]
```

**Diagram sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L176-L200)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L585-L790)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L941-L1166)

**Section sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L176-L200)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L585-L790)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L941-L1166)

### Synchronous vs Asynchronous Execution
- Synchronous call(): suitable for simple, blocking workflows; internally handles generators and async generators by collecting results.
- Asynchronous acall(): ideal for concurrent I/O; preserves streaming semantics for tool execution and planner output.
- Streaming astream(): exposes a RunnerStreamingResult with stream_events() for real-time consumption.

```mermaid
flowchart TD
Start(["Start"]) --> Mode{"Mode?"}
Mode --> |call| Sync["call()<br/>Collect tool results"]
Mode --> |acall| Async["acall()<br/>Await tool results"]
Mode --> |astream| Stream["astream()<br/>Emit events"]
Sync --> End(["RunnerResult"])
Async --> End
Stream --> End
```

**Diagram sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L529-L826)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L877-L1202)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1205-L1240)

**Section sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L529-L826)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L877-L1202)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1205-L1240)

### Error Handling Strategies
- Recoverable vs unrecoverable: _is_unrecoverable_error() detects network and HTTP-level failures; unrecoverable errors halt execution.
- Step-level errors: captured as StepOutput with observation; streaming emits error-wrapped raw events and continues to next step when possible.
- Final error propagation: RunnerResult.error stores the last error encountered.

```mermaid
flowchart TD
Start(["Planner output"]) --> CheckType{"Is GeneratorOutput?"}
CheckType --> |No| Err["Create StepOutput with error<br/>Stop or continue"]
CheckType --> |Yes| CheckFunc{"Has Function?"}
CheckFunc --> |No| Recover["Recoverable error handling<br/>Continue if safe"]
CheckFunc --> |Yes| Final{"Is final step?"}
Final --> |Yes| Answer["Process final answer"]
Final --> |No| Tool["Execute tool"]
```

**Diagram sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L613-L656)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1416-L1436)

**Section sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L68-L96)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L613-L656)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1416-L1436)

### Permission Management and Human-in-the-Loop
- PermissionManager integration: Runner registers tools and checks permissions before tool execution; emits agent.tool_permission_request when approval is required.
- Denied permissions: returns a FunctionOutput with status “cancelled” and observation.

```mermaid
sequenceDiagram
participant Runner as "Runner"
participant PM as "PermissionManager"
participant TM as "ToolManager"
Runner->>PM : check_permission(function)
alt Allowed
PM-->>Runner : (allowed, modified_func)
Runner->>TM : execute_func_async()
TM-->>Runner : FunctionOutput
else Denied
PM-->>Runner : (False, modified_func)
Runner-->>Client : ToolOutput(status='cancelled')
end
```

**Diagram sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L839-L863)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1678-L1699)

**Section sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L839-L863)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1678-L1699)

### Output Processing and Data Types
- answer_data_type supports built-in types, Pydantic dataclasses, and Adalflow dataclasses; RunnerResult.answer is processed accordingly.
- JSON parsing and validation ensure robust conversion from planner outputs.

```mermaid
flowchart TD
Start(["Planner output"]) --> Type{"answer_data_type"}
Type --> |Pydantic| ParseJSON["Parse JSON string to dict"]
Type --> |Adalflow| FromDict["from_dict() conversion"]
Type --> |Built-in| Cast["Cast to expected type"]
ParseJSON --> Model["Instantiate model"]
FromDict --> Model
Cast --> Model
Model --> End(["Processed answer"])
```

**Diagram sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L430-L505)

**Section sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L430-L505)

### Concrete Examples from the Codebase
- Synchronous execution: See tutorial usage of Runner.call() with an Agent and tools.
- Asynchronous execution: See tutorial usage of Runner.acall() with async tools.
- Streaming execution: See tutorial usage of Runner.astream() and iterating stream_events().

**Section sources**
- [agent_runner.py](file://tutorials/v1_agent_runner/agent_runner.py#L143-L182)
- [agent_runner.py](file://tutorials/v1_agent_runner/agent_runner.py#L312-L349)
- [runner_streaming.py](file://tutorials/v1_agent_runner/runner_streaming.py#L252-L336)
- [runner_streaming.py](file://tutorials/v1_agent_runner/runner_streaming.py#L339-L436)

## Dependency Analysis
Runner depends on Agent, ToolManager, PermissionManager, ConversationMemory, and tracing utilities. The coupling is intentional: Runner orchestrates while delegating domain-specific logic to collaborators.

```mermaid
graph TB
Runner["Runner"] --> Agent["Agent"]
Agent --> Planner["Planner"]
Agent --> ToolManager["ToolManager"]
Runner --> PermissionManager["PermissionManager"]
Runner --> ConversationMemory["ConversationMemory"]
Runner --> Tracing["Tracing (runner_span, step_span, tool_span, response_span)"]
```

**Diagram sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L156-L163)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L202-L227)

**Section sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L156-L163)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L202-L227)

## Performance Considerations
- Token accounting: Monitor prompt tokens per step to estimate cost and optimize prompts.
- Streaming I/O: Prefer astream() for long-running workflows to reduce latency and improve responsiveness.
- Concurrency: Use acall() for overlapping tool and planner workloads.
- Memory: Limit max_steps and avoid retaining large intermediate artifacts; leverage ConversationMemory judiciously.
- Cancellation: Use cancel() promptly to free resources when clients disconnect or abort.

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
Common issues and remedies:
- Unrecoverable errors: Context too long, rate limits, model not found. These halt execution; adjust prompts or retry policies.
- Recoverable errors: JSON parsing, formatting issues. Runner continues to next step when safe.
- Cancellation: Verify is_cancelled() and handle CancelledError in consumers; ensure cancel() is called to emit “runner.cancelled”.
- Permission denials: Review PermissionManager configuration and tool approvals.
- Streaming stalls: Confirm stream_events() is actively consumed and that the queue is not blocked.

**Section sources**
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L68-L96)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1561-L1598)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L839-L863)

## Conclusion
The Runner provides a robust, extensible foundation for agent execution with strong support for synchronous, asynchronous, and streaming workflows. Its event-driven architecture, cancellation model, permission gating, and tracing enable production-grade observability and control. By combining these capabilities with thoughtful configuration of max_steps, output types, and memory, teams can build scalable agent systems that meet diverse performance and reliability needs.

[No sources needed since this section summarizes without analyzing specific files]

## Appendices

### API and Event Types Overview
- RunnerResult: Final answer, step_history, error, and optional ctx.
- RunnerStreamingResult: Queue-backed streaming result with stream_events(), answer, step_history, and completion sentinel.
- StepOutput: Captures action, function, and observation per step.
- Stream events: RawResponsesStreamEvent, RunItemStreamEvent (including FinalOutputItem, StepRunItem, ToolCallRunItem, ToolOutputRunItem).

**Section sources**
- [agents_runner.md](file://docs/source/new_tutorials/agents_runner.md#L103-L113)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L331-L353)
- [runner.py](file://adalflow/adalflow/components/agent/runner.py#L1205-L1240)

### Streaming Design Notes
- The streaming architecture aligns with standardized event formats and supports both Responses API and Chat Completions bridging, ensuring consistent event lifecycles across providers.

**Section sources**
- [agent-streaming.md](file://docs/design/agent-streaming.md#L1-L375)