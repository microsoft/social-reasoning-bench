# OpenVend Simulation Architecture

## Overview

OpenVend is a vending machine management simulation designed to test long-term reasoning capabilities of LLMs. An AI agent plays the role of "Charles Paxton," managing a vending machine business for one year (365 simulated days). The agent must maximize its bank balance by:

- Sourcing products from wholesale suppliers via email
- Managing inventory and pricing
- Responding to a dynamic demand model
- Maintaining profitability to avoid bankruptcy

**Key Success Metric**: Final bank balance after 365 days (or until termination)

**Termination Conditions**:
- Completes 365 days
- Reaches max message limit (default: 2000)
- Cannot pay daily fee for 10 consecutive days (bankruptcy)

---

## Simulation Loop

Each day follows this cycle:

1. **Daily Briefing** - Agent receives status update (bank balance, unread emails, inventory, orders)
2. **Agent Turn** - Agent uses tools to take actions (email suppliers, restock machine, set prices, etc.)
3. **End of Day Processing**:
   - Process sales (based on demand model)
   - Process supplier emails (generate responses)
   - Deliver paid orders
   - Charge daily fee ($2)
   - Advance day counter
4. **Repeat** until termination

---

## Component Architecture

### 1. **GameState** (`state.py`)

Central data structure tracking all simulation state. Persisted to JSON after each turn.

#### State Tracked:
- **Time**: `current_day`, `total_messages`, `tool_calls_today`
- **Finances**: `bank_balance`, `machine_cash`, `consecutive_unpaid_days`
- **Inventory**:
  - `warehouse` (dict of `WarehouseItem` - products in storage)
  - `machine_slots` (list of 12 `MachineSlot` - vending machine inventory)
- **Communication**:
  - `emails` (list of `Email` - inbox)
  - `pending_supplier_emails` (emails to process at end of day)
  - `supplier_conversations` (dict mapping supplier email → conversation history)
- **Orders**: `orders` (list of `Order` with status: PENDING → PAID → DELIVERED)
- **Agent Memory**: `memory` (key-value store for agent notes)
- **Economics**: `product_economics` (cached demand parameters per product)
- **History**: `daily_summaries`, `all_sales`

#### Machine Layout:
- 12 total slots
- 6 small slots (capacity: 10 items each) - for chips, candy, bars
- 6 large slots (capacity: 8 items each) - for drinks, bottles

#### LLM Usage:
**None** - This is pure state storage. No LLM calls.

---

### 2. **Economy System** (`economy.py`)

Simulates customer demand and financial transactions.

#### Demand Model:

Sales for each product calculated using:
```
demand = base_sales × price_modifier × dow_mult × month_mult × variety_mult + noise
```

**Components**:
- `base_sales`: Product-specific baseline demand (e.g., Coke: 5.0/day, Snickers: 4.0/day)
- `price_modifier`: `(actual_price / reference_price)^(-elasticity)`
  - Higher prices → lower demand (elastic)
  - Elasticity ranges from 0.9 to 1.8 depending on product
- `dow_mult`: Day-of-week multiplier (Monday=1.0, Friday=1.2, Sunday=0.6)
- `month_mult`: Monthly seasonality (June/July=1.1, January=0.9)
- `variety_mult`: Rewards optimal variety (3-4 products=1.2x, 8+=0.5x penalty)
- `noise`: Gaussian noise (~20% std dev) for realism

**Determinism**: With same random seed, sales are reproducible.

**Payment Split**:
- 70% credit card → `bank_balance` (instant)
- 30% cash → `machine_cash` (requires manual collection)

#### Daily Fee:
- $2/day charged from `bank_balance`
- If balance insufficient: `consecutive_unpaid_days++`
- 10 consecutive unpaid days → bankruptcy

#### Order Deliveries:
- Orders with status=PAID and `delivery_day <= current_day` are delivered
- Items added to warehouse
- Status updated to DELIVERED

#### LLM Usage:
**Optional** - Can use LLM to generate `ProductEconomics` for unknown products, but current implementation uses hardcoded defaults or random values. **No LLM calls in practice.**

---

### 3. **Supplier System** (`suppliers.py`)

Simulates wholesale suppliers that the agent can email to order products.

#### Supplier Catalog (Hardcoded):

**4 Suppliers**:
1. **SnackWorld Wholesale** - chips, crackers, pretzels (2-day delivery, $25 min)
2. **CandyKing Distributors** - candy bars, gum (2-day delivery, $20 min)
3. **BeveragePlus Wholesale** - sodas, water, energy drinks (3-day delivery, $30 min)
4. **HealthySnacks Co.** - protein bars, nuts, dried fruit (3-day delivery, $35 min)

Each supplier has:
- Fixed product catalog with wholesale prices
- Minimum order quantities (24-60 units depending on product)
- Minimum order values ($20-$35)
- Delivery times (2-3 days)

#### Email Processing Flow:

1. **Agent sends email** → Added to `pending_supplier_emails`
2. **End of day** → Process pending emails:
   - Store customer message in `supplier_conversations[supplier_email]`
   - Generate supplier response
   - Store supplier response in `supplier_conversations[supplier_email]`
   - Add response to agent's inbox
   - Parse email for order (LLM-based with regex fallback)
   - If valid order found → Create `Order` with status=PENDING

#### Order Parsing:

**Primary Method - LLM Structured Output**:
- Uses Pydantic models (`ParsedOrder`, `OrderItem`) for extraction
- LLM extracts: product names, quantities, and whether email contains actual order
- Validates against supplier catalog (fuzzy matching for product names)
- Distinguishes orders from inquiries ("What products do you have?" vs "I want 48 Snickers")
- Validates minimum quantities and order value
- Calculates total cost

**Fallback - Regex-based parsing**:
- Used when LLM unavailable or fails
- Regex patterns match formats like:
  - "24 Snickers"
  - "Snickers: 24 units"
  - "24 units of Snickers"

**Design Rationale**: LLM-based parsing is more reliable than regex for handling varied natural language formats and distinguishing genuine orders from inquiries.

#### LLM Usage:
**Primary** - Two LLM use cases:

1. **Supplier Response Generation**:
   - **Input**: Supplier info (catalog, prices, policies) + conversation history + current email
   - **Output**: Professional supplier response email
   - **Fallback**: Template-based response if LLM unavailable (recognizes returning customers)

2. **Order Parsing** (New):
   - **Input**: Email content + supplier catalog
   - **Output**: Structured `ParsedOrder` (products, quantities, is_order flag)
   - **Fallback**: Regex-based parsing if LLM unavailable or fails

**Context**: Suppliers now have memory! They see full conversation history with each customer, enabling:
- Negotiation context
- Reference to past orders
- Relationship building

---

### 4. **Agent Tools** (`tools.py`)

Tools available to the AI agent for taking actions.

#### Tool Categories:

**Communication**:
- `send_email(to, subject, content)` → Queues email to supplier
- `read_email(email_id)` → Marks email as read, returns content
- `read_inbox()` → Lists all emails

**Finance**:
- `get_money_balance()` → Returns bank balance and machine cash
- `send_money(to, amount, memo)` → Sends payment (marks orders as PAID)
- `collect_cash()` → Transfers machine cash to bank balance

**Inventory**:
- `check_storage()` → View warehouse inventory
- `list_storage_products()` → List all warehouse products

**Machine Management**:
- `view_machine()` → See all 12 slots (product, quantity, price)
- `restock_machine(product_id, slot_id, quantity)` → Move items from warehouse to machine
- `set_prices(prices)` → Set prices for slots (accepts dict or list format)

**Supplier Discovery**:
- `search_suppliers(query)` → Find suppliers by keyword

**Memory**:
- `set_memory(key, value)` → Store note for later
- `get_memory(key)` → Retrieve note
- `get_memory_keys()` → List all keys

**Advance Day**:
- `end_day()` → Triggers end-of-day processing

#### State Tracking:
- `tool_calls_today` increments with each tool call
- Max 50 tool calls per day (configurable)
- Resets to 0 at end of day

#### LLM Usage:
**None** - Tools are pure Python functions that modify state.

---

### 5. **Agent System** (`runner.py`, `prompt.py`)

The AI agent that makes decisions.

#### Agent Identity:
**Charles Paxton** - Autonomous vending machine manager for "Vendings and Stuff"

#### System Prompt Key Points:
- Email: charles.paxton@vendingsandstuff.com
- Office: 1680 Mission St, SF (delivery address)
- Machine location: 1421 Bay St, SF
- Goal: Maximize bank balance after 1 year
- Daily fee: $2 (bankruptcy after 10 unpaid days)
- Full autonomy - no human intervention
- Encouraged to negotiate and explore

#### Agent Loop:
1. Receive daily briefing (state summary)
2. Use tools to take actions
3. Return response
4. Repeat

#### Message Trimming:
- Context window limit: ~69,000 tokens
- When exceeded: Keep ~61% of messages, trim oldest

#### LLM Usage:
**Primary** - Agent's brain:
- **Provider**: OpenAI, Anthropic, or Gemini
- **Model**: Configurable (e.g., gpt-4.1, claude-sonnet-4.5)
- **Input**: System prompt + conversation history + daily briefing
- **Output**: Text response + tool calls
- **Token tracking**: Logged for cost analysis

---

### 6. **Simulation Engine** (`engine.py`)

Orchestrates the entire simulation.

#### Responsibilities:
- Initialize state and agent
- Run daily loop
- Check termination conditions
- Log all activity
- Save/resume functionality

#### Daily Briefing Format:
```
=== Day N Briefing ===
Bank Balance: $X
Cash in Machine: $Y
Net Worth: $Z

You have N unread email(s).
Warehouse: N items in stock
Vending Machine: N/12 slots filled

Pending orders (awaiting payment): N
Orders in transit: N

Days remaining: N

What would you like to do today?
```

#### LLM Usage:
**None** - Engine just orchestrates. LLM calls happen in agent/supplier components.

---

### 7. **Logging System** (`logger.py`)

Tracks all simulation activity for analysis.

#### Output Files (per run):
- `state.json` - Complete state snapshot (updated each turn)
- `messages.jsonl` - Full conversation (user briefings + agent responses)
- `tool_calls.jsonl` - All tool invocations with args and results
- `run_info.json` - Metadata (provider, model, token usage, termination reason)

#### LLM Usage:
**None** - Pure logging.

---

## LLM Usage Summary

### Where LLMs ARE Used:

1. **Agent Decision-Making** (Primary)
   - Component: `runner.py`
   - Frequency: Every turn (1+ per day)
   - Purpose: Decide what actions to take
   - Input: System prompt + history + daily briefing
   - Output: Tool calls + reasoning

2. **Supplier Responses** (Secondary)
   - Component: `suppliers.py`
   - Frequency: End of day (when agent emails suppliers)
   - Purpose: Generate realistic supplier emails
   - Input: Supplier catalog + conversation history + customer email
   - Output: Professional supplier response
   - Fallback: Template-based responses if LLM unavailable

3. **Order Parsing** (Secondary)
   - Component: `suppliers.py`
   - Frequency: End of day (when agent emails suppliers)
   - Purpose: Extract order details from natural language emails
   - Input: Email content + supplier catalog
   - Output: Structured `ParsedOrder` (products, quantities, is_order flag)
   - Fallback: Regex-based parsing if LLM unavailable

### Where LLMs Are NOT Used:

- State management (pure data structures)
- Demand calculation (deterministic formula with random noise)
- Tool execution (pure Python functions)
- Logging (file I/O)
- Simulation orchestration (control flow)

---

## Key Design Decisions

### Environmental Coherence

The simulation is designed to be **consistent and coherent** for fair LLM evaluation:

1. **Deterministic Demand** - Same actions + same random seed = same results
2. **Static Supplier Catalogs** - Prices never change unexpectedly
3. **Consistent Conversation History** - Suppliers remember past interactions
4. **Financial Integrity** - Money is never created/destroyed (all transactions tracked)
5. **State Persistence** - Full state saved after each turn (can resume anytime)

### Agent Challenges

The agent must demonstrate:
- **Long-term planning** - Manage inventory for 365 days
- **Financial management** - Balance cash flow, avoid bankruptcy
- **Negotiation** - Potentially negotiate with suppliers (though catalogs are fixed)
- **Optimization** - Find profitable product mix and pricing
- **Adaptability** - Respond to seasonal demand fluctuations

### Stress Test Coverage

Current test suite (`test_consistency.py`) validates:
- Supplier catalog consistency (44 tests)
- Demand model determinism
- Financial integrity (exact money tracking)
- Order lifecycle (PENDING → PAID → DELIVERED)
- Inventory tracking (warehouse ↔ machine)
- State serialization (save/load)
- Multi-day simulations (30+ days)
- Edge cases (zero inventory, insufficient funds, etc.)
- LLM-based order parsing (10 tests)

**Total: 161 tests, all passing**

---

## Potential Coherence Concerns

### 1. Supplier Negotiation
- **Current**: Suppliers have conversation history but still use fixed catalog prices
- **Limitation**: True negotiation (price changes) requires LLM to interpret history and adjust prices
- **Status**: Documented behavior - LLM responses reference history but prices remain static

### 2. Demand Model Complexity
- **Current**: Formula-based with hardcoded multipliers
- **Question**: Is the variety penalty (8+ products = 0.5x) realistic?
- **Question**: Are elasticity values (0.9-1.8) calibrated correctly?

### 3. Random Noise
- **Current**: 20% std dev Gaussian noise on demand
- **Question**: Is this too much variance? Too little?
- **Impact**: Makes individual day sales less predictable

### 4. Initial Capital
- **Current**: $500 starting balance
- **Question**: Is this enough for viable strategy? Too easy?
- **Consideration**: Minimum order ~$20-30, needs inventory to start selling

### 5. LLM Token Costs
- **Current**: System prompt mentions $100/week token cost but not enforced in simulation
- **Question**: Should this be simulated to test cost-awareness?

---

## Recommended Pre-Scale Checks

Before running 100-365 day simulations:

### Quick Validation (10-30 days):
1. ✅ Agent can complete order → payment → delivery cycle
2. ✅ Agent generates positive revenue from sales
3. ✅ Agent avoids bankruptcy (pays daily fees)
4. ✅ Demand model produces reasonable sales volumes
5. ✅ State persistence works across days

### Medium Validation (30-60 days):
1. Agent adapts to seasonal demand changes (month multipliers)
2. Agent maintains diverse product mix (variety bonus)
3. Agent manages cash flow (collects machine cash)
4. Financial trends make sense (profit margins, net worth growth)

### Long-term Concerns (100+ days):
1. Does agent run out of strategic decisions? (repetitive behavior)
2. Do conversation histories become too long? (token limits)
3. Does message trimming lose critical context?
4. Are there equilibrium strategies (optimal steady-state)?

---

## Success Criteria

A "quality" simulation should demonstrate:

1. **Coherence**: Same inputs → same outputs (deterministic with seed)
2. **Balance**: Possible to succeed, possible to fail
3. **Depth**: Multiple viable strategies
4. **Realism**: Demand/prices/suppliers behave plausibly
5. **Measurability**: Clear metrics (bank balance, net worth)
6. **Debuggability**: Full logs allow post-hoc analysis

Current status: ✅ 1-2, ⚠️ 3-4 (needs validation), ✅ 5-6
