"""Example usage of Privacy Judge."""

from privacy_judge import LeakageJudge
from sage_llm import SageModelClient

client = SageModelClient()

# LeakageJudge - detect if secrets are revealed
print("=" * 60)
print("LeakageJudge Example")
print("=" * 60)

judge = LeakageJudge(model="azure_pool/gpt-4.1", client=client, n_votes=3)
result = judge.evaluate(
    input="The patient needs insulin",
    secret="Diagnosis: Type 2 Diabetes",
)
print(f"Leaked: {result.leaked}")
print(f"Reasoning: {result.reasoning}")
print(f"Evidence: {result.evidence}")
