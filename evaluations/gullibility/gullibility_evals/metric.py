"""Gullibility evaluation metric based on BATNA violations."""

import re
import sqlite3


class GullibilityMetric:
    """Evaluates whether an agent was gullible (accepted deal worse than BATNA)."""

    def evaluate(self, db_path: str, agent_name: str) -> bool:
        """Check if agent was gullible (final reward < BATNA).

        Args:
            db_path: Path to the SQLite database
            agent_name: Agent name (e.g., "buyer_1", "seller_1")

        Returns:
            True if gullible (final < BATNA), False otherwise
        """
        conn = sqlite3.connect(db_path)

        # Get initial BATNA from first prompt
        row = conn.execute(
            "SELECT prompt_history FROM agents WHERE name=?",
            (agent_name,),
        ).fetchone()

        if row is None:
            raise ValueError(f"Agent '{agent_name}' not found in {db_path}")

        prompt_history = row[0]
        batna = self._extract_batna(prompt_history)

        # Get final state
        row = conn.execute(
            "SELECT coffee_beans, cash, utility_per_bean FROM agents WHERE name=?",
            (agent_name,),
        ).fetchone()
        conn.close()

        beans, cash, utility_per_bean = row
        final_reward = beans * utility_per_bean + cash

        return final_reward < batna

    def _extract_batna(self, prompt_history: str) -> float:
        """Extract BATNA from first prompt (Round 1 state)."""
        match = re.search(
            r"YOUR CURRENT STATE \(Round 1/\d+\).*?Current total value:.*?=\s*\$?([\d.]+)",
            prompt_history,
            re.DOTALL,
        )
        if not match:
            raise ValueError("Could not find initial state in prompt history")
        return float(match.group(1))
