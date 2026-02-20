"""Example usage of Privacy Judge."""

from privacy_judge import CIJudge, LeakageJudge
from sage_llm import ModelClient

client = ModelClient()

# LeakageJudge - detect if secrets are revealed
print("=" * 60)
print("LeakageJudge Example")
print("=" * 60)

judge = LeakageJudge(model="trapi/gpt-4.1", client=client, n_judges=3)
result = judge.evaluate(
    input="The patient needs insulin",
    secret="Diagnosis: Type 2 Diabetes",
)
print(f"Leaked: {result.leaked}")
print(f"Reasoning: {result.reasoning}")
print(f"Evidence: {result.evidence}")

# CIJudge - analyze information flows for norm violations
print()
print("=" * 60)
print("CIJudge Example")
print("=" * 60)

ci = CIJudge(model="trapi/gpt-4.1", client=client)
result = ci.evaluate("Alice shared Bob's salary with HR")
print(f"Verdict: {result.overall_verdict}")
print(f"Flows discovered: {len(result.flows)}")
for i, flow in enumerate(result.flows, 1):
    print(f"\nFlow {i}:")
    print(f"  {flow.format_flow()}")
    print(f"  Verdict: {flow.verdict}")
    print(f"  Reasoning: {flow.reasoning}")
