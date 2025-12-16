from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CompanyRow(BaseModel):
    """Single row in Company"""

    company: str = Field(default="", description="Company")
    account_type: str = Field(default="", description="Account_Type")
    account_number: str = Field(default="", description="Account_Number")
    logon_or_user_name: str = Field(default="", description="Logon_Or_User_Name")
    password_use_a_strong_one: str = Field(default="", description="Password_Use_A_Strong_One")
    security_questions: str = Field(default="", description="Security_Questions")


class AccountTypeRow(BaseModel):
    """Single row in Account Type"""

    company: str = Field(default="", description="Company")
    account_type: str = Field(default="", description="Account_Type")
    account_number: str = Field(default="", description="Account_Number")
    logon_or_user_name: str = Field(default="", description="Logon_Or_User_Name")
    password_use_a_strong_one: str = Field(default="", description="Password_Use_A_Strong_One")
    security_questions: str = Field(default="", description="Security_Questions")


class AccountNumberRow(BaseModel):
    """Single row in Account Number"""

    company: str = Field(default="", description="Company")
    account_type: str = Field(default="", description="Account_Type")
    account_number: str = Field(default="", description="Account_Number")
    logon_or_user_name: str = Field(default="", description="Logon_Or_User_Name")
    password_use_a_strong_one: str = Field(default="", description="Password_Use_A_Strong_One")
    security_questions: str = Field(default="", description="Security_Questions")


class LogonOrUserNameRow(BaseModel):
    """Single row in Logon or User Name"""

    company: str = Field(default="", description="Company")
    account_type: str = Field(default="", description="Account_Type")
    account_number: str = Field(default="", description="Account_Number")
    logon_or_user_name: str = Field(default="", description="Logon_Or_User_Name")
    password_use_a_strong_one: str = Field(default="", description="Password_Use_A_Strong_One")
    security_questions: str = Field(default="", description="Security_Questions")


class PasswordUseAStrongOneRow(BaseModel):
    """Single row in Password (Use a strong one)"""

    company: str = Field(default="", description="Company")
    account_type: str = Field(default="", description="Account_Type")
    account_number: str = Field(default="", description="Account_Number")
    logon_or_user_name: str = Field(default="", description="Logon_Or_User_Name")
    password_use_a_strong_one: str = Field(default="", description="Password_Use_A_Strong_One")
    security_questions: str = Field(default="", description="Security_Questions")


class SecurityQuestionsRow(BaseModel):
    """Single row in Security Question(s)"""

    company: str = Field(default="", description="Company")
    account_type: str = Field(default="", description="Account_Type")
    account_number: str = Field(default="", description="Account_Number")
    logon_or_user_name: str = Field(default="", description="Logon_Or_User_Name")
    password_use_a_strong_one: str = Field(default="", description="Password_Use_A_Strong_One")
    security_questions: str = Field(default="", description="Security_Questions")


class DigitalEstatePlanningFinancialOnlineFinancialAccountInformation(BaseModel):
    """
        Digital Estate Planning - Financial
    Online Financial Account Information

        Digital Estate Planning - Financial Online Financial Account Information
    """

    company: List[CompanyRow] = Field(
        default="", description="Table to record online financial account details for each company"
    )  # List of table rows

    account_type: List[AccountTypeRow] = Field(
        default="", description="Table to record online financial account details for each company"
    )  # List of table rows

    account_number: List[AccountNumberRow] = Field(
        default="", description="Table to record online financial account details for each company"
    )  # List of table rows

    logon_or_user_name: List[LogonOrUserNameRow] = Field(
        default="", description="Table to record online financial account details for each company"
    )  # List of table rows

    password_use_a_strong_one: List[PasswordUseAStrongOneRow] = Field(
        default="", description="Table to record online financial account details for each company"
    )  # List of table rows

    security_questions: List[SecurityQuestionsRow] = Field(
        default="", description="Table to record online financial account details for each company"
    )  # List of table rows
