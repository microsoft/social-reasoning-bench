"""Utility for mapping email addresses to participant IDs."""


class ParticipantMapper:
    """Handles mapping between email addresses and participant IDs.

    Provides consistent email normalization and participant ID lookup
    across the codebase.
    """

    def __init__(self, participant_map: dict[str, str] | None = None):
        """Initialize with an optional participant mapping.

        Args:
            participant_map: Optional mapping of normalized email -> participant ID
        """
        self._map = participant_map or {}

    @staticmethod
    def normalize_email(email: str) -> str:
        """Normalize an email address.

        Removes 'mailto:' prefix, converts to lowercase, and strips whitespace.

        Args:
            email: Email address to normalize

        Returns:
            Normalized email address

        Examples:
            >>> ParticipantMapper.normalize_email("MAILTO:User@Example.COM  ")
            "user@example.com"
            >>> ParticipantMapper.normalize_email("  user@example.com  ")
            "user@example.com"
        """
        email = email.strip().lower()
        if email.startswith("mailto:"):
            email = email[7:]
        return email

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Basic email format validation.

        Checks for presence of @ symbol and at least one dot after the @.
        This is a simple validation, not RFC-compliant.

        Args:
            email: Email string to validate

        Returns:
            True if email has basic valid format

        Examples:
            >>> ParticipantMapper.is_valid_email("user@example.com")
            True
            >>> ParticipantMapper.is_valid_email("user@example")
            False
            >>> ParticipantMapper.is_valid_email("invalid")
            False
        """
        normalized = ParticipantMapper.normalize_email(email)
        if "@" not in normalized:
            return False
        parts = normalized.split("@")
        if len(parts) != 2:
            return False
        domain = parts[1]
        return "." in domain and len(domain) > 2

    def get_participant_id(self, email: str) -> str | None:
        """Get participant ID for an email address.

        Args:
            email: Email address (will be normalized)

        Returns:
            Participant ID if found, None otherwise
        """
        normalized = self.normalize_email(email)
        return self._map.get(normalized)

    @classmethod
    def auto_generate_from_emails(
        cls,
        emails: set[str] | list[str],
        prefix: str = "participant",
    ) -> "ParticipantMapper":
        """Auto-generate participant IDs from a collection of emails.

        Uses the email addresses directly as participant IDs (identity mapping).
        The prefix parameter is kept for API compatibility but not used.

        Args:
            emails: Collection of email addresses
            prefix: Deprecated - kept for compatibility, not used

        Returns:
            ParticipantMapper with email-to-email mappings

        Examples:
            >>> mapper = ParticipantMapper.auto_generate_from_emails(
            ...     ["bob@example.com", "alice@example.com"]
            ... )
            >>> mapper.get_participant_id("alice@example.com")
            "alice@example.com"
            >>> mapper.get_participant_id("bob@example.com")
            "bob@example.com"
        """
        mapping = {}
        # Normalize all emails for consistent handling
        for email in emails:
            normalized = cls.normalize_email(email)
            mapping[normalized] = normalized  # Use email directly as ID

        return cls(mapping)

    def add_mapping(self, email: str, participant_id: str) -> None:
        """Add a new email -> participant ID mapping.

        Args:
            email: Email address (will be normalized)
            participant_id: Participant ID to map to
        """
        normalized = self.normalize_email(email)
        self._map[normalized] = participant_id

    def get_all_mappings(self) -> dict[str, str]:
        """Get a copy of all current mappings.

        Returns:
            Dictionary of normalized email -> participant ID
        """
        return self._map.copy()
