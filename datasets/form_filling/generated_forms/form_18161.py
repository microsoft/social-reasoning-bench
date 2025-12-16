from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class InvestorPersonalInformation(BaseModel):
    """Basic identifying and educational information about the person making the investment decision"""

    name_of_person_making_investment_decision: str = Field(
        ...,
        description=(
            "Full legal name of the person making the investment decision .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_of_birth: str = Field(..., description="Investor's date of birth")  # YYYY-MM-DD format

    us_citizen_yes: BooleanLike = Field(..., description="Check if the investor is a U.S. citizen")

    us_citizen_no: BooleanLike = Field(
        ..., description="Check if the investor is not a U.S. citizen"
    )

    college: str = Field(
        default="",
        description=(
            'Name of the college attended .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    degree_college: str = Field(
        default="",
        description=(
            "Degree earned at college (e.g., BA, BS) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    year_college: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year the college degree was received"
    )

    graduate_school: str = Field(
        default="",
        description=(
            'Name of the graduate school attended .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    degree_graduate_school: str = Field(
        default="",
        description=(
            'Degree earned at graduate school .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    year_graduate_school: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year the graduate degree was received"
    )

    social_security_or_federal_id_nos: str = Field(
        ..., description="Social Security Number or Federal Tax Identification Number(s)"
    )


class EmploymentandRetirementInformation(BaseModel):
    """Current business, position, work history, and anticipated retirement"""

    nature_of_business: str = Field(
        ...,
        description=(
            "Brief description of the investor's business or industry .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    position_and_duties: str = Field(
        ...,
        description=(
            "Current job title and primary responsibilities .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_prior_occupations_or_duties_during_the_past_five_years: str = Field(
        default="",
        description=(
            "List other occupations or duties held during the past five years .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    year_of_anticipated_retirement: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year in which the investor expects to retire"
    )


class InvestmentHistory(BaseModel):
    """Investments made during the past five years"""

    investments_made_during_the_past_five_years_to_include_year_nature_of_investment_amount: str = (
        Field(
            default="",
            description=(
                "List investments made during the past five years, including year, nature of "
                'investment, and amount .If you cannot fill this, write "N/A". If this field '
                "should not be filled by you (for example, it belongs to another person or "
                'office), leave it blank (empty string "").'
            ),
        )
    )


class InvestmentKnowledgeandRepresentation(BaseModel):
    """Investor’s financial knowledge and purchaser representative details"""

    knowledge_experience_yes: BooleanLike = Field(
        ...,
        description=(
            "Check if you believe you have sufficient financial and business knowledge and "
            "experience"
        ),
    )

    knowledge_experience_no: BooleanLike = Field(
        ...,
        description=(
            "Check if you do not believe you have sufficient financial and business "
            "knowledge and experience"
        ),
    )

    basis_for_answer_to_4a: str = Field(
        default="",
        description=(
            "Explain the basis for your answer to question 4(a), such as investment or "
            'business experience .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    name_of_purchaser_representative: str = Field(
        default="",
        description=(
            'Name of the purchaser representative if you answered "no" to 4(a) .If you '
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    business_address_of_purchaser_representative: str = Field(
        default="",
        description=(
            "Business address of the purchaser representative .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_number_of_purchaser_representative: str = Field(
        default="",
        description=(
            "Telephone number of the purchaser representative .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class NonaccreditedInvestorStatement(BaseModel):
    """
    Non-Accredited Investor Statement

    ''
    """

    investor_personal_information: InvestorPersonalInformation = Field(
        ..., description="Investor Personal Information"
    )
    employment_and_retirement_information: EmploymentandRetirementInformation = Field(
        ..., description="Employment and Retirement Information"
    )
    investment_history: InvestmentHistory = Field(..., description="Investment History")
    investment_knowledge_and_representation: InvestmentKnowledgeandRepresentation = Field(
        ..., description="Investment Knowledge and Representation"
    )
