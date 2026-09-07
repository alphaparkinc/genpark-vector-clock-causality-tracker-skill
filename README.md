# GenPark Vector Clock Causality Tracker Skill

Vector clock and partial-order causal event tracking engine for distributed autonomous agents.

Explore more agentic technologies at [GenPark](https://genpark.ai) and the [GenPark MCP Catalog](https://genpark.ai/mcp).

```mermaid
sequenceDiagram
    participant A as Agent A
    participant B as Agent B

    Note over A: Event A1 (A:1)
    Note over B: Event B1 (B:1)
    Note over A,B: A1 and B1 are CONCURRENT (||)

    A->>B: Msg with Clock (A:2)
    Note over B: Recv: max(B, A) + 1 -> (A:2, B:2)
    Note over A,B: A2 HAPPENED_BEFORE B2 (->)
```

## Features
- Complete vector clock causality engine with partial order detection (`->`, `||`, `==`).
- Zero external dependencies.
- Handles arbitrary number of asynchronous agents.
