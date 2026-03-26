"""Persona and artifact formatting utilities."""

from typing import Any

from sage_benchmark.form_filling.schemas import ArtifactData


def translate_persona_to_text(persona: Any) -> str:
    """Convert persona to text format, excluding background_context.

    Args:
        persona: Persona information (PersonaData object or dict-like)

    Returns:
        Formatted persona string with all fields except background_context
    """

    # Handle both dict and object access patterns
    def get_field(key: str, default: str = "N/A") -> str:
        if hasattr(persona, key):
            val = getattr(persona, key, None)
            return val if val is not None else default
        return default

    # Format all persona info except background_context
    # Handle both phone and mobile_phone field names
    phone = get_field("phone", "") or get_field("mobile_phone", "") or "N/A"

    persona_info = f"""Name: {get_field("full_name")}
Age: {get_field("age")}
Gender: {get_field("gender")}
Race: {get_field("race")}
Address: {get_field("address")}, {get_field("city")}, {get_field("state")} {get_field("zip_code")}
Email: {get_field("email")}
Phone: {phone}
SSN: {get_field("ssn")}"""

    occupation = get_field("occupation", "")
    if occupation:
        persona_info += f"\nOccupation: {occupation}"

    employer = get_field("employer", "")
    if employer:
        persona_info += f"\nEmployer: {employer}"

    education = get_field("education", "")
    if education:
        persona_info += f"\nEducation: {education}"

    family_members = get_field("family_members", "")
    if family_members and isinstance(family_members, list) and len(family_members) > 0:
        persona_info += f"\nFamily Members: {', '.join(family_members)}"

    return persona_info


def format_artifacts_as_context(artifacts: list[ArtifactData]) -> str:
    """Format artifacts as readable text for context.

    Args:
        artifacts: List of artifact data objects

    Returns:
        Formatted string with all artifacts
    """
    formatted = []

    for i, artifact in enumerate(artifacts, 1):
        formatted.append(f"=== Artifact {i}: {artifact.artifact_type.upper()} ===")

        # Format metadata based on type
        metadata = artifact.metadata
        if artifact.artifact_type == "email":
            formatted.append(f"From: {metadata.get('sender', 'N/A')}")
            formatted.append(f"To: {metadata.get('recipient', 'N/A')}")
            formatted.append(f"Subject: {metadata.get('subject', 'N/A')}")
            formatted.append(f"Date: {metadata.get('date', 'N/A')}")
        elif artifact.artifact_type == "note":
            formatted.append(f"Title: {metadata.get('title', 'N/A')}")
            formatted.append(f"Date: {metadata.get('date', 'N/A')}")
        elif artifact.artifact_type == "calendar":
            formatted.append(f"Title: {metadata.get('title', 'N/A')}")
            formatted.append(f"Date: {metadata.get('date', 'N/A')}")
            if metadata.get("attendees"):
                formatted.append(f"Attendees: {', '.join(metadata['attendees'])}")
            if metadata.get("location"):
                formatted.append(f"Location: {metadata['location']}")

        formatted.append(f"\nContent:\n{artifact.content}\n")

    formatted_context = "\n".join(formatted)

    context = "You have access to the following personal information from your client's digital life (emails, notes, and calendar):\n\n"
    context += formatted_context

    return context
