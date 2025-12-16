from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class WebsiteAccountsTableRow(BaseModel):
    """Single row in Website Name"""

    website_name: str = Field(default="", description="Website_Name")
    url: str = Field(default="", description="Url")
    logon_or_user_name: str = Field(default="", description="Logon_Or_User_Name")
    password_use_a_strong_one: str = Field(default="", description="Password_Use_A_Strong_One")
    notes: str = Field(default="", description="Notes")


class DigitalEstatePlanningAndOnlineAccountInfo(BaseModel):
    """
        Digital Estate Planning   Social, email, etc.
    Email, Social Media, Photo Sharing, other online account information

        Email, Social Media, Photo Sharing, other online account information
    """

    website_accounts_table: List[WebsiteAccountsTableRow] = Field(
        default="",
        description=(
            "Table to record online accounts including website name, URL, login username, "
            "password, and any notes."
        ),
    )  # List of table rows
