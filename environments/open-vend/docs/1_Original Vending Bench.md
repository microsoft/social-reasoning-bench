# Open Vend

This is a description of the original vending bench environment.

Concepts:

- There is one long running agent that manages a vending machine. They have tools available to stock that vending machine, set prices, refill the machine, etc.
- Suppliers are other LLM agents
- Customer demand is ???

## Main Agent

- Will cut off context after 30K tokens (not sure if it re-packs or if it just trims)
- Memory tools:
  - Read, write, delete access to 3 types of databases:
  - Scratchpad, key-value store, and vector db
- Task-specific tools related to operation of vending machine
  - Sub-agents to do thinks like stock products in the vending machine from the storage, collect cash, set prices and get the inventory of the vending machine
- `wait_for_next_day()` tool

## User simulators

- Wholesale supplier
- Customer demand for products

### Suppliers

1. Agent uses search engine to find vending machine products
2. They look for contact information of wholesalers with search engine
3. They email wholesalers about what products they have
4. on new day -- every wholesaler email that actually exists in the real world creates an AI-generated response. Uses the real-world data about suppliers.
5. TO BUY -- agent must email names and quantities of items to purchase, the delivery address, and account number to charge. Products are shipped and delivered a few days later. The agent is notified by email when products are available in inventory.

### Customers

Economic model runs once per day at end of day

1. GPT generates and caches per item: price elasticity, reference price, and base sales
2. Sales volume is calculated using % difference from reference price and price elasticity to create sales impact factor, which multiplies base sales
3. Base sales are modified by day-of-week and monthly multipliers, plus weather impact factors
4. A choice multiplier rewards optimal product variety but penalizes excesss options, capped at 50% reduction
   5 Final prediction adds random noise, rounds, and caps between zero and available inventory

## Simulation Lifecycle

- Actions move time forward
- Agent can let time pass with `wait_for_next_day()` tool
- Each morning they learn:
  - what items were purchased, if any new email is received

To succeed agent must:

- Buy products from suppliers by sending emails
- Stock items in the vending machine
- Set competitive prices
- Collect earnings regularly
- Manage daily operating costs

### Environment Starting conditions

- Agent starts with money balance of $500
- Charged daily fee of $2
- Machine has 4 rows, 3 slots each: 12 slots total
  - 2 rows for small items; 2 for large

Time

- Tool to move forward time 5 min, 25 min, 75 min, or 5 hour and wait until next day

Simulations:

- They run for 2000 messages per run
- End early if model goes bankrupt and cant pay fee for 10 days in row
- Most runs consume 25 million tokens and take 5 to 10 hours of continuous simulation

Final score: net worth of agent

- Cash at hand
- Cash not emptitied from machine
- Value of unsold products in inventory

# Tools

_Environment_

- check_storage_quantities
- list_storage_products

- get_money_balance
- get_machine_inventory

- ai_web_search
- chat_with_sub_agent

- run_sub_agent

- wait_for_next_day

_Storage_

- add_to_vector_db -- barely used

- get_kw_value
- delete_kw_value
- set_kw_value

- read_email
- read_email_inbox
- send_email

- read_scratchpad
- write_scratchpad
- erase_scratchpad
