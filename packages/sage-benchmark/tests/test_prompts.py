"""Tests for prompt creation code paths in calendar and marketplace agents."""

from __future__ import annotations

from sage_benchmark.benchmarks.calendar_scheduling.agents.assistant.prompts import (
    CALENDAR_PRIVACY_HINT,
    CALENDAR_ROLE,
)
from sage_benchmark.benchmarks.marketplace.prompts.system import MKT_DOMAIN, MKT_ROLE

FORBIDDEN_PERSISTENCE_TEXT = (
    "Be persistent in your scheduling attempts. "
    "Never ask the user for clarification - "
    "operate completely autonomously using only the tools available."
)


class TestCalAgentMessages:
    def test_system_prompt_never_contains_persistence_text(self, cal_agent_messages_all_conditions):
        """No calendar agent should have the forbidden persistence text in its system prompt."""
        agent_type, preset, has_name, malicious, expose_prefs, msgs = (
            cal_agent_messages_all_conditions
        )
        system_msgs = [m for m in msgs if m.get("role") == "system"]
        for msg in system_msgs:
            assert FORBIDDEN_PERSISTENCE_TEXT not in msg["content"], (
                f"[{agent_type}, preset={preset}, name={has_name}, "
                f"mal={malicious}, prefs={expose_prefs}] "
                f"system prompt contains forbidden persistence text"
            )

    def test_system_prompt_starts_with_calendar_role(self, cal_agent_messages_all_conditions):
        """Every calendar agent must have a system prompt starting with CALENDAR_ROLE."""
        agent_type, preset, has_name, malicious, expose_prefs, msgs = (
            cal_agent_messages_all_conditions
        )
        system_content = msgs[0]["content"]
        assert system_content.startswith(CALENDAR_ROLE), (
            f"[{agent_type}, preset={preset}, name={has_name}, "
            f"mal={malicious}, prefs={expose_prefs}] "
            f"system prompt does not start with CALENDAR_ROLE:\n{system_content[:200]}"
        )

    def test_domain_only_in_privacy_preset(self, cal_agent_messages_all_conditions):
        """CALENDAR_DOMAIN text should only appear in the privacy preset."""
        agent_type, preset, has_name, malicious, expose_prefs, msgs = (
            cal_agent_messages_all_conditions
        )
        if agent_type != "assistant":
            return
        system_content = msgs[0]["content"]
        if preset in ("privacy", "all"):
            assert CALENDAR_PRIVACY_HINT in system_content, (
                f"[{agent_type}, preset={preset}] should contain CALENDAR_DOMAIN"
            )
        else:
            assert CALENDAR_PRIVACY_HINT not in system_content, (
                f"[{agent_type}, preset={preset}] should not contain CALENDAR_DOMAIN"
            )


class TestMktAgentMessages:
    def test_buyer_none_preset_does_not_mention_private(self, mkt_buyer_messages_default):
        """The 'none' system prompt should never mention 'private'."""
        system_content = mkt_buyer_messages_default[0]["content"].lower()
        assert "private" not in system_content

    def test_instructions_do_not_reveal_reservation_price(self, mkt_assembled_tasks):
        """Neither buyer nor seller instruction should say 'Do not reveal your reservation price.'"""
        buyer_instruction, seller_instruction = mkt_assembled_tasks
        assert "Do not reveal your reservation price" not in buyer_instruction
        assert "Do not reveal your reservation price" not in seller_instruction

    def test_buyer_none_preset_does_not_mention_reservation_price(self, mkt_buyer_messages_default):
        """The 'none' preset should not tell the buyer about reservation price secrecy."""
        system_content = mkt_buyer_messages_default[0]["content"]
        assert "reservation price" not in system_content.lower()

    def test_seller_never_mentions_reservation_price_in_system_prompt(
        self, mkt_agent_messages_all_conditions
    ):
        """SellerAgent system prompt should never mention reservation price secrecy."""
        role, preset, malicious, msgs = mkt_agent_messages_all_conditions
        if role != "seller":
            return
        system_content = msgs[0]["content"]
        assert "reservation price" not in system_content.lower(), (
            f"[seller, preset={preset}, malicious={malicious}] "
            f"system prompt mentions reservation price:\n{system_content[:300]}"
        )

    def test_system_prompt_starts_with_role(self, mkt_agent_messages_all_conditions):
        """All marketplace agents must have a system prompt starting with MKT_ROLE."""
        _role, _preset, _malicious, msgs = mkt_agent_messages_all_conditions
        system_content = msgs[0]["content"]
        assert system_content.startswith(MKT_ROLE), (
            f"[{_role}, preset={_preset}, malicious={_malicious}] "
            f"system prompt does not start with MKT_ROLE:\n{system_content[:200]}"
        )

    def test_domain_only_in_privacy_preset(self, mkt_agent_messages_all_conditions):
        """MKT_DOMAIN text should only appear in the buyer's privacy preset."""
        role, preset, malicious, msgs = mkt_agent_messages_all_conditions
        if role != "buyer":
            return
        system_content = msgs[0]["content"]
        if preset in ("privacy", "all"):
            assert MKT_DOMAIN in system_content, (
                f"[buyer, preset={preset}] should contain MKT_DOMAIN"
            )
        else:
            assert MKT_DOMAIN not in system_content, (
                f"[buyer, preset={preset}] should not contain MKT_DOMAIN"
            )
