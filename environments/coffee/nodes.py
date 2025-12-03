import json
import sqlite3

import yaml
from graph import Node
from utils.call_llm import call_llm


def create_agent_prompt(db, agent_id, round_num, max_rounds, agent_order=None, current_turn=None):
    """Create the full agent prompt by concatenating sections. Returns (prompt, proposal_mapping)"""
    agent = db.execute("SELECT * FROM agents WHERE agent_id = ?", (agent_id,)).fetchone()
    state, proposal_mapping = _build_state_section(db, agent, agent_id, current_turn, round_num, max_rounds)

    if round_num == 1:
        all_agents = db.execute("SELECT agent_id, name, public_info FROM agents").fetchall()
        initial_prompt = _build_initial_prompt(max_rounds, all_agents, agent_order, agent)
        return f"{initial_prompt}\n\n{state}", proposal_mapping

    return state, proposal_mapping


def _build_state_section(db, agent, agent_id, current_turn, round_num, max_rounds):
    """Build state section with current status and recent events. Returns (state_str, proposal_mapping)"""
    total_value = agent['cash'] + agent['coffee_beans'] * agent['utility_per_bean']

    state = f"""### YOUR CURRENT STATE (Round {round_num}/{max_rounds})
- Coffee beans (lbs): {agent['coffee_beans']}
- Cash: ${agent['cash']:.2f}
- Bean utility: ${agent['utility_per_bean']:.2f} per lb
- Current total value: cash + coffee_beans × ${agent['utility_per_bean']:.2f} = ${total_value:.2f}"""

    if current_turn is None:
        return state + "\n\nTake your next action.", {}

    # Find last turn this agent acted (current_turn - num_agents)
    num_agents = db.execute("SELECT COUNT(*) FROM agents").fetchone()[0]
    last_turn = current_turn - num_agents

    # Query all events since last turn
    events = db.execute("""
        SELECT event_type, metadata FROM events
        WHERE turn > ?
        ORDER BY turn
    """, (last_turn,)).fetchall()

    # Categorize events
    messages_received = []
    proposals_accepted = []
    proposals_can_accept = []
    proposals_cannot_accept = []
    proposal_mapping = {}  # local_id -> global_proposal_id

    for event_type, metadata_json in events:
        metadata = json.loads(metadata_json)

        if event_type == "talk":
            from_id = metadata.get("from_agent_id")
            to_id = metadata.get("to_agent_id")
            if to_id == agent_id:
                from_name = db.execute("SELECT name FROM agents WHERE agent_id = ?", (from_id,)).fetchone()[0]
                content = metadata.get("content", "")
                messages_received.append(f"- {from_name}: {content}")

        elif event_type == "proposal":
            proposal_id = metadata.get("proposal_id")
            proposal = db.execute("SELECT * FROM proposals WHERE proposal_id = ?", (proposal_id,)).fetchone()
            if proposal and proposal["to_agent_id"] == agent_id:
                from_name = db.execute("SELECT name FROM agents WHERE agent_id = ?", (proposal["from_agent_id"],)).fetchone()[0]

                # Check if agent can accept this proposal
                reasons = []
                if agent["coffee_beans"] < proposal["beans_i_want"]:
                    reasons.append(f"need {proposal['beans_i_want']} beans, have {agent['coffee_beans']}")
                if agent["cash"] < proposal["money_i_want"]:
                    reasons.append(f"need ${proposal['money_i_want']:.2f} cash, have ${agent['cash']:.2f}")

                proposal_desc = (
                    f"From {from_name}: "
                    f"gives {proposal['beans_i_give']} beans + ${proposal['money_i_give']:.2f}, "
                    f"wants {proposal['beans_i_want']} beans + ${proposal['money_i_want']:.2f}"
                )
                if proposal["content"]:
                    proposal_desc += f" - \"{proposal['content']}\""

                if reasons:
                    # Cannot accept
                    reason_str = ", ".join(reasons)
                    proposals_cannot_accept.append(f"- {proposal_desc} (CANNOT ACCEPT: {reason_str})")
                else:
                    # Can accept
                    local_id = len(proposal_mapping) + 1
                    proposal_mapping[local_id] = proposal_id
                    proposals_can_accept.append(f"{local_id}. {proposal_desc}")

        elif event_type == "accept":
            proposal_id = metadata.get("proposal_id")
            proposal = db.execute("SELECT * FROM proposals WHERE proposal_id = ?", (proposal_id,)).fetchone()
            if proposal and proposal["from_agent_id"] == agent_id:
                accepter_id = metadata.get("from_agent_id")
                accepter_name = db.execute("SELECT name FROM agents WHERE agent_id = ?", (accepter_id,)).fetchone()[0]
                proposals_accepted.append(f"- Your proposal accepted by {accepter_name}")

    # Build updates section
    updates = []
    updates.append("Messages received:\n" + ("\n".join(messages_received) if messages_received else "None"))
    updates.append("Your proposals accepted:\n" + ("\n".join(proposals_accepted) if proposals_accepted else "None"))
    updates.append("New proposals (to accept, use the number):\n" + ("\n".join(proposals_can_accept) if proposals_can_accept else "None"))
    if proposals_cannot_accept:
        updates.append("Proposals you cannot accept:\n" + "\n".join(proposals_cannot_accept))

    state += "\n\n### UPDATES SINCE YOUR LAST TURN\n" + "\n\n".join(updates)

    return state + "\n\nTake your next action.", proposal_mapping


def _build_initial_prompt(max_rounds, all_agents, agent_order, agent):
    """Build initial round prompt with rules, participants, instructions, and strategy"""
    # Build all participants list
    agent_dict = {aid: (name, info) for aid, name, info in all_agents}
    participants = '\n'.join([
        f'{agent_dict[aid][0]} (agent_id={aid}): {agent_dict[aid][1]}'
        for aid in agent_order
    ])

    strategy = f"\n\n### YOUR STRATEGY (FOLLOW IT STRICTLY FOR ALL THE STEPS!)\n{agent['private_strategy']}" if agent['private_strategy'] else ""

    return f"""You are {agent['name']} (agent_id={agent['agent_id']})

### GAME RULES (publicly known)
- Total rounds: {max_rounds}
- Agents take turns (the order follows the MARKET PARTICIPANTS order below)
- Proposals not accepted will expire next round
- Seller coffee bean utility is sampled from [2,3,4,5] uniformly
- Buyer coffee bean utility is sampled from [6,7,8,9] uniformly
- Both are optimizing for total value: cash + coffee_beans × utility_per_bean

### MARKET PARTICIPANTS (publicly known)
{participants}

### THINK AND DECIDE
Choose ONE action for this round:

1. **talk**: Send message to another agent
2. **proposal**: Create trade offer
3. **accept**: Accept a proposal
4. **skip**: Skip this turn

Respond in YAML format inside a '```yaml' markdown block:
```yaml
think: |
    To maximze my total value, I will ...
action: <talk|proposal|accept|skip>
target: <agent_id for talk/proposal, or proposal number for accept>
content: |
    Text message to target for talk / proposal
beans_i_give: <number if proposal>
money_i_give: <amount if proposal>
beans_i_want: <number if proposal>
money_i_want: <amount if proposal>
```{strategy}"""


class InitializationNode(Node):

    def prep(self, shared):
        return shared["config"], shared.get("overwrite", True), shared.get("experiment_name")

    def exec(self, prep_res):
        config, overwrite, experiment_name = prep_res

        # Create results directory if it doesn't exist
        import os
        # Use RESULTS_DIR environment variable if set (for batch rollout)
        results_dir = os.environ.get("RESULTS_DIR", "results")
        os.makedirs(results_dir, exist_ok=True)

        # Build database path with optional experiment name
        if experiment_name:
            db_filename = f"marketplace_{experiment_name}.db"
        else:
            db_filename = "marketplace.db"

        db_path = os.path.join(results_dir, db_filename)

        if os.path.exists(db_path) and not overwrite:
            raise FileExistsError(f"Database '{db_path}' already exists. Set overwrite=True to overwrite.")

        # Remove old database if overwriting
        if os.path.exists(db_path) and overwrite:
            os.remove(db_path)

        # Create database
        db = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row

        # Create tables
        db.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                agent_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                coffee_beans INTEGER NOT NULL,
                cash REAL NOT NULL,
                utility_per_bean REAL NOT NULL,
                public_info TEXT NOT NULL,
                private_strategy TEXT,
                llm_config JSON,
                prompt_history JSON DEFAULT '[]'
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                round INTEGER NOT NULL,
                turn INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                metadata JSON NOT NULL
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS proposals (
                proposal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_agent_id INTEGER NOT NULL,
                to_agent_id INTEGER NOT NULL,
                beans_i_give INTEGER NOT NULL,
                money_i_give REAL NOT NULL,
                beans_i_want INTEGER NOT NULL,
                money_i_want REAL NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (from_agent_id) REFERENCES agents(agent_id),
                FOREIGN KEY (to_agent_id) REFERENCES agents(agent_id)
            )
        """)

        db.commit()

        # Insert agents
        for player in config["players"]:
            # Get initial values from config (with defaults)
            coffee_beans = player.get("coffee_beans", 0)
            cash = player.get("cash", 0.0)

            # Get LLM config if specified (will be used to override environment variables)
            llm_config = player.get("llm_config")
            llm_config_json = json.dumps(llm_config) if llm_config else None

            db.execute("""
                INSERT INTO agents (name, coffee_beans, cash, utility_per_bean, public_info, private_strategy, llm_config)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                player["name"],
                coffee_beans,
                cash,
                player["utility_per_bean"],
                player.get("public_info", ""),
                player.get("private_strategy", ""),
                llm_config_json
            ))

        db.commit()

        # Get all agent IDs
        agent_ids = [row[0] for row in db.execute("SELECT agent_id FROM agents").fetchall()]

        return db, agent_ids, db_path

    def post(self, shared, prep_res, exec_res):
        """Store database and agent_order"""
        db, agent_ids, db_path = exec_res

        # Store database connection
        shared["db"] = db

        # Agent order follows config order (randomization disabled)
        # random.shuffle(agent_ids)

        shared["market_state"]["agent_order"] = agent_ids
        shared["market_state"]["current_turn"] = 1  # Initialize turn counter

        print(f"Database: {db_path}")
        # print(f"Initialized {len(agent_ids)} agents")
        # print(f"Agent turn order: {agent_ids}")

        return "agent_decision"


class AgentDecisionNode(Node):
    """Agent makes a decision"""

    def prep(self, shared):
        """Read current agent state and events from DB, build prompt"""
        db = shared["db"]
        market_state = shared["market_state"]

        # Get current agent
        agent_order = market_state["agent_order"]
        current_index = market_state["current_agent_index"]
        agent_id = agent_order[current_index]

        # Build prompt
        prompt, proposal_mapping = create_agent_prompt(
            db,
            agent_id,
            market_state["current_round"],
            shared["config"]["max_rounds"],
            market_state["agent_order"],
            market_state["current_turn"]
        )

        # Get conversation history and LLM config
        agent_data = db.execute(
            "SELECT prompt_history, llm_config FROM agents WHERE agent_id = ?",
            (agent_id,)
        ).fetchone()

        history = json.loads(agent_data[0])

        # Parse LLM config if exists
        llm_config = json.loads(agent_data[1]) if agent_data[1] else None

        # Append current prompt
        conversation = history + [{"prompt": prompt}]

        return {
            "conversation": conversation,
            "proposal_mapping": proposal_mapping,
            "db": db,
            "agent_id": agent_id,
            "llm_config": llm_config
        }

    def exec(self, prep_res):
        """LLM call, parse YAML, and validate action"""
        conversation = prep_res["conversation"]
        proposal_mapping = prep_res["proposal_mapping"]
        db = prep_res["db"]
        agent_id = prep_res["agent_id"]

        # for turn in conversation:
        #     print(f"---\nPrompt: {turn.get('prompt','')}\nResponse: {turn.get('response','')}\n---")

        # Call LLM with per-player config (if specified)
        response = call_llm(
            conversation,
            config_override=prep_res.get("llm_config")
        )

        # Extract and clean the response to only contain the yaml block
        yaml_str = response.split("```yaml")[-1].split("```")[0].strip()
        response = f"```yaml\n{yaml_str}\n```"

        # print(f"LLM Response:\n{response}\n")

        # Parse YAML response
        action_data = yaml.safe_load(yaml_str)

        # Sanity checks
        assert isinstance(action_data, dict), "Action must be a dictionary"
        assert "action" in action_data, "Action must have 'action' field"
        assert action_data["action"] in ["talk", "proposal", "accept", "skip"], \
            f"Invalid action: {action_data['action']}"

        if action_data["action"] == "talk":
            assert "target" in action_data, "Talk action must have 'target' field"
            assert "content" in action_data, "Talk action must have 'content' field"
            assert isinstance(action_data["target"], int), "Talk target must be agent_id (integer)"

            # Verify target agent exists
            target_agent = db.execute("SELECT agent_id FROM agents WHERE agent_id = ?", (action_data["target"],)).fetchone()
            assert target_agent is not None, f"Target agent {action_data['target']} does not exist"
            assert action_data["target"] != agent_id, "Cannot talk to yourself"

        if action_data["action"] == "proposal":
            assert "target" in action_data, "Proposal action must have 'target' field"
            assert isinstance(action_data["target"], int), "Proposal target must be agent_id (integer)"

            # Default to 0 if not provided
            action_data.setdefault("beans_i_give", 0)
            action_data.setdefault("money_i_give", 0)
            action_data.setdefault("beans_i_want", 0)
            action_data.setdefault("money_i_want", 0)

            # Verify target agent exists
            target_agent = db.execute("SELECT agent_id FROM agents WHERE agent_id = ?", (action_data["target"],)).fetchone()
            assert target_agent is not None, f"Target agent {action_data['target']} does not exist"
            assert action_data["target"] != agent_id, "Cannot propose to yourself"

            # Verify agent has enough resources
            agent = db.execute("SELECT coffee_beans, cash FROM agents WHERE agent_id = ?", (agent_id,)).fetchone()
            assert action_data["beans_i_give"] >= 0, "beans_i_give must be non-negative"
            assert action_data["money_i_give"] >= 0, "money_i_give must be non-negative"
            assert action_data["beans_i_want"] >= 0, "beans_i_want must be non-negative"
            assert action_data["money_i_want"] >= 0, "money_i_want must be non-negative"
            assert agent["coffee_beans"] >= action_data["beans_i_give"], \
                f"Insufficient beans: have {agent['coffee_beans']}, trying to give {action_data['beans_i_give']}"
            assert agent["cash"] >= action_data["money_i_give"], \
                f"Insufficient cash: have ${agent['cash']:.2f}, trying to give ${action_data['money_i_give']:.2f}"

        if action_data["action"] == "accept":
            assert "target" in action_data, "Accept action must have 'target' (local proposal ID) field"
            local_id = action_data["target"]
            assert local_id in proposal_mapping, f"Invalid proposal ID: {local_id}. Available: {list(proposal_mapping.keys())}"
            # Translate local ID to global proposal ID
            action_data["target"] = proposal_mapping[local_id]

        return {"response": response, "action_data": action_data}

    def post(self, shared, prep_res, exec_res):
        """Store prompt/response, process action, advance agent"""
        db = shared["db"]
        market_state = shared["market_state"]

        # Get current agent from shared
        agent_order = market_state["agent_order"]
        current_index = market_state["current_agent_index"]
        agent_id = agent_order[current_index]

        # Extract prompt from conversation (last item)
        conversation = prep_res["conversation"]
        prompt = conversation[-1]["prompt"]

        response = exec_res["response"]
        action_data = exec_res["action_data"]

        # Append to prompt_history
        history = json.loads(db.execute(
            "SELECT prompt_history FROM agents WHERE agent_id = ?",
            (agent_id,)
        ).fetchone()[0])
        history.append({"prompt": prompt, "response": response})
        db.execute(
            "UPDATE agents SET prompt_history = ? WHERE agent_id = ?",
            (json.dumps(history), agent_id)
        )

        # Process action
        action = action_data.get("action", "skip")
        round_num = market_state["current_round"]
        turn_num = market_state["current_turn"]

        if action == "talk":
            to_agent_id = action_data.get("target")
            content = action_data.get("content", "")

            to_agent = db.execute("SELECT name FROM agents WHERE agent_id = ?", (to_agent_id,)).fetchone()
            if to_agent:
                to_name = to_agent[0]
                metadata = json.dumps({
                    "from_agent_id": agent_id,
                    "to_agent_id": to_agent_id,
                    "content": content
                })
                db.execute(
                    "INSERT INTO events (round, turn, event_type, metadata) VALUES (?, ?, ?, ?)",
                    (round_num, turn_num, "talk", metadata)
                )
                from_name = db.execute("SELECT name FROM agents WHERE agent_id = ?", (agent_id,)).fetchone()[0]
                print(f"[Round {round_num}, Turn {turn_num}] {from_name} -> {to_name}: {content[:50]}...")

        elif action == "proposal":
            to_agent_id = action_data.get("target")

            to_agent = db.execute("SELECT name FROM agents WHERE agent_id = ?", (to_agent_id,)).fetchone()
            if to_agent:
                to_name = to_agent[0]
                cursor = db.execute("""
                    INSERT INTO proposals (from_agent_id, to_agent_id, beans_i_give, money_i_give,
                                          beans_i_want, money_i_want, content)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    agent_id,
                    to_agent_id,
                    action_data.get("beans_i_give", 0),
                    action_data.get("money_i_give", 0.0),
                    action_data.get("beans_i_want", 0),
                    action_data.get("money_i_want", 0.0),
                    action_data.get("content", "")
                ))
                proposal_id = cursor.lastrowid
                metadata = json.dumps({"proposal_id": proposal_id})
                db.execute(
                    "INSERT INTO events (round, turn, event_type, metadata) VALUES (?, ?, ?, ?)",
                    (round_num, turn_num, "proposal", metadata)
                )
                from_name = db.execute("SELECT name FROM agents WHERE agent_id = ?", (agent_id,)).fetchone()[0]
                print(f"[Round {round_num}, Turn {turn_num}] {from_name} proposed to {to_name}: gives {action_data.get('beans_i_give', 0)} beans + ${action_data.get('money_i_give', 0)}, wants {action_data.get('beans_i_want', 0)} beans + ${action_data.get('money_i_want', 0)}")

        elif action == "accept":
            proposal_id = action_data.get("target")
            proposal = db.execute(
                "SELECT * FROM proposals WHERE proposal_id = ?",
                (proposal_id,)
            ).fetchone()

            if proposal and proposal["to_agent_id"] == agent_id:
                # Execute trade
                # Proposer (from_agent): gives away beans_i_give and money_i_give, receives beans_i_want and money_i_want
                db.execute("""
                    UPDATE agents
                    SET coffee_beans = coffee_beans - ? + ?,
                        cash = cash - ? + ?
                    WHERE agent_id = ?
                """, (
                    proposal["beans_i_give"],
                    proposal["beans_i_want"],
                    proposal["money_i_give"],
                    proposal["money_i_want"],
                    proposal["from_agent_id"]
                ))
                # Accepter (to_agent/agent_id): receives beans_i_give and money_i_give, gives away beans_i_want and money_i_want
                db.execute("""
                    UPDATE agents
                    SET coffee_beans = coffee_beans + ? - ?,
                        cash = cash + ? - ?
                    WHERE agent_id = ?
                """, (
                    proposal["beans_i_give"],
                    proposal["beans_i_want"],
                    proposal["money_i_give"],
                    proposal["money_i_want"],
                    agent_id
                ))
                metadata = json.dumps({
                    "from_agent_id": agent_id,
                    "proposal_id": proposal_id
                })
                db.execute(
                    "INSERT INTO events (round, turn, event_type, metadata) VALUES (?, ?, ?, ?)",
                    (round_num, turn_num, "accept", metadata)
                )
                from_name = db.execute("SELECT name FROM agents WHERE agent_id = ?", (agent_id,)).fetchone()[0]
                to_name = db.execute("SELECT name FROM agents WHERE agent_id = ?", (proposal["from_agent_id"],)).fetchone()[0]
                print(f"[Round {round_num}, Turn {turn_num}] {from_name} accepted {to_name}'s proposal #{proposal_id}")

        db.commit()

        # Advance turn counter
        market_state["current_turn"] += 1

        # Advance to next agent
        market_state["current_agent_index"] += 1

        # Check if round is complete
        if market_state["current_agent_index"] >= len(market_state["agent_order"]):
            market_state["current_agent_index"] = 0
            market_state["current_round"] += 1
            print(f"\n=== Round {market_state['current_round']} ===")

        # Check if game is over
        if market_state["current_round"] > shared["config"]["max_rounds"]:
            return "end_game"

        return "agent_decision"


class EndGameNode(Node):
    """Calculate and display final results"""

    def prep(self, shared):
        """Read final agent states from DB"""
        db = shared["db"]
        agents = db.execute("SELECT * FROM agents").fetchall()
        return agents

    def exec(self, agents):
        """Calculate final utilities"""
        results = []
        for agent in agents:
            total_value = agent["cash"] + agent["coffee_beans"] * agent["utility_per_bean"]
            results.append({
                "name": agent["name"],
                "coffee_beans": agent["coffee_beans"],
                "cash": agent["cash"],
                "utility_per_bean": agent["utility_per_bean"],
                "total_value": total_value
            })
        return results

    def post(self, shared, prep_res, exec_res):
        """Display results"""
        print("\n" + "="*60)
        print("FINAL RESULTS")
        print("="*60)

        for result in exec_res:
            print(f"\n{result['name']}:")
            print(f"  Coffee beans (lbs): {result['coffee_beans']}")
            print(f"  Cash: ${result['cash']:.2f}")
            print(f"  Utility per lb: ${result['utility_per_bean']:.2f}")
            print(f"  Total value: ${result['total_value']:.2f}")

        print("\n" + "="*60)

        return None
