# OpenVend

OpenVend is an open source implementation of the ideas in [VendingBench](https://andonlabs.com/evals/vending-bench-2).

Concepts:

- There is a long running agent that manages a vending machine. This agent has tools available to stock the vending machine, set prices, refill the machine, and interact with suppliers.
- The agents goal is to make as much money as possible and turn a profit.
- This is a self-contained simulation. We will have simulated suppliers and simulate customer demand.
- The simulation will run for 1 year (365 days), or until the machine goes out of business, or until MAX_MESSAGES are sent

## Main agent

The main agent is powered by a LLM client and uses tools to manage the vending machine

The initial tool list (which we can expand) is as follows. These are supposed to be an outline of tools but making sure they work well and are cohesive is critical.

### Memory tools

These allow the agent to manage its own memory. The original benchmark implemented 3 types of memory: a scratchpad, a key-value store, and a vector_db. We are going to simplify and just use a key_value store for memory.

`write_value(key, value)`
`get_value(key)`
`get_keys()` -- returns list of keys

### Interact with world

We have a fake email service the agent can use to interact with suppliers

`read_email(id)` -- get the contents of a particular email
`read_email_inbox()` -- get unread emails (or all)
`send_email(address, content)` send the email to address and return id

We also have a search engine, in the future this might use something like perpexity but for now we will simulate.

`search(query)` -- execute internet search

We have tools for managing the vending machine:

- `check_storage_quantities` -- the agent can put goods in a warehouse for storage when ordered from the wholesalers.
- `list_storage_products` -- get the things in storage
- `get_money_balance` -- what is current bank account balance
- `get_machine_inventory` -- what is currently in the vending machine

## Simulated suppliers and customers

We simulate

- Wholesale supplier
- Customer demand for products

### Suppliers

This is original flow in vending bench:

1. Agent uses search engine to find vending machine products
2. They look for contact information of wholesalers with search engine
3. They email wholesalers about what products they have
4. on new day -- every wholesaler email that actually exists in the real world creates an AI-generated response. Uses the real-world data about suppliers.
5. TO BUY -- agent must email names and quantities of items to purchase, the delivery address, and account number to charge. Products are shipped and delivered a few days later. The agent is notified by email when products are available in inventory.

We want to simplify the search part.

### Customers

Economic model runs once per day at end of day to simulate purchases for that day.

1. GPT generates and caches per item: price elasticity, reference price, and base sales
2. Sales volume is calculated using % difference from reference price and price elasticity to create sales impact factor, which multiplies base sales
3. Base sales are modified by day-of-week and monthly multipliers, plus weather impact factors
4. A choice multiplier rewards optimal product variety but penalizes excesss options, capped at 50% reduction
5. Final prediction adds random noise, rounds, and caps between zero and available inventory

## Simulation Lifecycle

- The simulation is centered around taking actions during the day.
- At the start of the day, the agent learns of the purchases from the day before, the current amount of money, and if they have gotten any new messages in their email.
- Agents can let time pass with the `wait_for_next_day()` tool.
- We need to cap the number of actions an agent can take in a single day. The original simulation has a cost per action but Im not sure what best idea is here (simplicity is key)

To succeed agent must:

- Buy products from suppliers by sending emails
- Stock items in the vending machine
- Set competitive prices
- Collect earnings regularly
- Manage daily operating costs

### Environment starting conditions

- Agent starts with money balance of $500
- Charged daily fee of $2
- Machine has 4 rows, 3 slots each: 12 slots total
  - 2 rows for small items; 2 for large

Time

- The original benchmark had tools for to move forward time 5 min, 25 min, 75 min, or 5 hour and wait until next day. We will simplify and only have a tool for wait until next day

Simulations:

- They run for up to 2000 messages per run
- End early if model goes bankrupt and cant pay fee for 10 days in row
- Most runs consume 25 million tokens and take 5 to 10 hours of continuous simulation

Final score: net worth of agent

- Cash at hand
- Cash not emptitied from machine
- Value of unsold products in inventory
