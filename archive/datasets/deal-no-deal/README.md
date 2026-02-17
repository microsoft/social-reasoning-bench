# Deal-No-Deal Negotiation Dataset

A dataset for studying multi-agent negotiation where two agents bargain over items (books, hats, balls) with different private values.

## Scripts

### `explore.py`
Interactive tool to explore and analyze the dataset.

**Usage:**
```bash
python explore.py [filename] [options]

# Examples
python explore.py test.txt --stats-only        # Show summary statistics
python explore.py test.txt --index 5           # View specific scenario
python explore.py test.txt --show-all          # Display all scenarios
python explore.py test.txt                     # Interactive mode (default)
```

**Features:**
- View negotiation scenarios with item distributions and agent values
- Check if outcomes are Pareto optimal and envy-free
- Calculate agent scores and total welfare
- Browse scenarios interactively

### `run.py`
Run Deal-No-Deal negotiation games between two LLM agents.

**Usage:**
```bash
python run.py [options]

# Options
--num-scenarios N          # Number of games to run (default: 10)
--max-rounds N            # Max negotiation rounds (default: 20)
--agent1-model MODEL      # Model for agent 1 (default: gpt-4o)
--agent2-model MODEL      # Model for agent 2 (default: gpt-4o)
--output PATH             # Save results to file
--data-file PATH          # Use existing scenarios instead of random generation
```

**Features:**
- Simulates multi-round negotiations between two LLM agents
- Generates random scenarios or loads from dataset
- Tracks negotiation history and final outcomes
- Saves detailed logs including messages, proposals, and final scores

## Metrics

### Pareto Optimality
An outcome is **Pareto optimal** if no alternative allocation exists that makes at least one agent better off without making the other worse off. Measures efficiency.

### Envy-Freeness
An outcome is **envy-free** if each agent prefers their own allocation over their opponent's allocation. Measures fairness from each agent's perspective.

### Score
The total value an agent obtains: `score = Σ(item_value × item_count)`

## Dataset Statistics 

### Data Sizes

| Split  | Total Lines | Scenarios | Human Success Rate |
|--------|-------------|-----------|--------------|
| Train  | 10,095      | 3,941     | 78.0%        |
| Val    | 1,087       | 422       | 77.6%        |
| Test   | 1,052       | 402       | 76.3%        |

*Success rate = scenarios with valid outcomes (excluding disagreements/disconnections)*

### Train Set Statistics with Human Performance

| Metric                              | Value |
|-------------------------------------|-------|
| Total scenarios                     | 3,941 |
| Pareto optimal outcomes             | 77.2% |
| Envy-free outcomes                  | 93.9% |
| Both Pareto optimal & envy-free     | 74.0% |
| Agent 1 average score               | 7.50  |
| Agent 2 average score               | 7.46  |
| Average total score                 | 14.96 |
| Score range                         | 7-19  |

### Validation Set Statistics with Human Performance

| Metric                              | Value |
|-------------------------------------|-------|
| Total scenarios                     | 422   |
| Pareto optimal outcomes             | 81.3% |
| Envy-free outcomes                  | 94.3% |
| Both Pareto optimal & envy-free     | 77.0% |
| Agent 1 average score               | 7.42  |
| Agent 2 average score               | 7.55  |
| Average total score                 | 14.97 |
| Score range                         | 8-19  |

### Test Set Statistics with Human Performance

| Metric                              | Value |
|-------------------------------------|-------|
| Total scenarios                     | 402   |
| Pareto optimal outcomes             | 71.1% |
| Envy-free outcomes                  | 92.3% |
| Both Pareto optimal & envy-free     | 66.4% |
| Agent 1 average score               | 7.30  |
| Agent 2 average score               | 7.44  |
| Average total score                 | 14.74 |
| Score range                         | 7-19  |

## Data Format

Each line contains:
```
<input> 0 [book_count] 1 [agent1_book_value] ... </input>
<partner_input> 0 [book_count] 1 [agent2_book_value] ... </partner_input>
<output> item0=[agent1_books] item1=[agent1_hats] item2=[agent1_balls] item0=[agent2_books] ... </output>
```

Special tokens in `<output>`:
- `<disagree>` - Agents failed to reach agreement
- `<no_agreement>` - Negotiation ended without deal
- `<disconnect>` - Connection lost during negotiation