from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ComplainantInformation(BaseModel):
    """Contact information for the complainant(s)"""

    complainants_name: str = Field(
        ...,
        description=(
            'Full name of the first complainant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    tel_no_home: str = Field(
        default="",
        description=(
            "Home telephone number of the first complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    tel_no_work: str = Field(
        default="",
        description=(
            "Work telephone number of the first complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    fax_no: str = Field(
        default="",
        description=(
            'Fax number of the first complainant .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        default="",
        description=(
            "Email address of the first complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_street: str = Field(
        ...,
        description=(
            "Street address of the first complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City of the first complainant's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the first complainant's address")

    zip: str = Field(..., description="ZIP code of the first complainant's address")

    complainants_name_second_complainant: str = Field(
        default="",
        description=(
            "Full name of the second complainant, if any .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    tel_no_home_second_complainant: str = Field(
        default="",
        description=(
            "Home telephone number of the second complainant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tel_no_work_second_complainant: str = Field(
        default="",
        description=(
            "Work telephone number of the second complainant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fax_no_second_complainant: str = Field(
        default="",
        description=(
            'Fax number of the second complainant .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_address_second_complainant: str = Field(
        default="",
        description=(
            "Email address of the second complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_street_second_complainant: str = Field(
        default="",
        description=(
            "Street address of the second complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_second_complainant: str = Field(
        default="",
        description=(
            "City of the second complainant's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_second_complainant: str = Field(
        default="", description="State of the second complainant's address"
    )

    zip_second_complainant: str = Field(
        default="", description="ZIP code of the second complainant's address"
    )


class RespondentInformation(BaseModel):
    """Registered persons and/or firms alleged to have violated the Commodity Exchange Act"""

    respondents_name: str = Field(
        ...,
        description=(
            "Name of the first respondent (person or firm) alleged to have violated the Act "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    tel_no: str = Field(
        default="",
        description=(
            "Telephone number of the first respondent .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    fax_no_respondent: str = Field(
        default="",
        description=(
            'Fax number of the first respondent .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_address_respondent: str = Field(
        default="",
        description=(
            'Email address of the first respondent .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_street_respondent: str = Field(
        default="",
        description=(
            "Street address of the first respondent .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_respondent: str = Field(
        default="",
        description=(
            "City of the first respondent's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_respondent: str = Field(default="", description="State of the first respondent's address")

    zip_respondent: str = Field(
        default="", description="ZIP code of the first respondent's address"
    )

    registered_with_cftc_yes: BooleanLike = Field(
        default="",
        description=(
            "Indicate YES if the first respondent was registered with the CFTC at the time "
            "of the alleged violation"
        ),
    )

    registered_with_cftc_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate NO if the first respondent was not registered with the CFTC at the "
            "time of the alleged violation"
        ),
    )

    respondents_name_second_respondent: str = Field(
        default="",
        description=(
            "Name of the second respondent (person or firm), if any .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tel_no_second_respondent: str = Field(
        default="",
        description=(
            "Telephone number of the second respondent .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    fax_no_second_respondent: str = Field(
        default="",
        description=(
            'Fax number of the second respondent .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_address_second_respondent: str = Field(
        default="",
        description=(
            "Email address of the second respondent .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_street_second_respondent: str = Field(
        default="",
        description=(
            "Street address of the second respondent .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_second_respondent: str = Field(
        default="",
        description=(
            "City of the second respondent's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_second_respondent: str = Field(
        default="", description="State of the second respondent's address"
    )

    zip_second_respondent: str = Field(
        default="", description="ZIP code of the second respondent's address"
    )

    registered_with_cftc_yes_second_respondent: BooleanLike = Field(
        default="",
        description=(
            "Indicate YES if the second respondent was registered with the CFTC at the time "
            "of the alleged violation"
        ),
    )

    registered_with_cftc_no_second_respondent: BooleanLike = Field(
        default="",
        description=(
            "Indicate NO if the second respondent was not registered with the CFTC at the "
            "time of the alleged violation"
        ),
    )

    respondents_name_third_respondent: str = Field(
        default="",
        description=(
            "Name of the third respondent (person or firm), if any .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tel_no_third_respondent: str = Field(
        default="",
        description=(
            "Telephone number of the third respondent .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    fax_no_third_respondent: str = Field(
        default="",
        description=(
            'Fax number of the third respondent .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_address_third_respondent: str = Field(
        default="",
        description=(
            'Email address of the third respondent .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_street_third_respondent: str = Field(
        default="",
        description=(
            "Street address of the third respondent .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_third_respondent: str = Field(
        default="",
        description=(
            "City of the third respondent's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_third_respondent: str = Field(
        default="", description="State of the third respondent's address"
    )

    zip_third_respondent: str = Field(
        default="", description="ZIP code of the third respondent's address"
    )

    registered_with_cftc_yes_third_respondent: BooleanLike = Field(
        default="",
        description=(
            "Indicate YES if the third respondent was registered with the CFTC at the time "
            "of the alleged violation"
        ),
    )

    registered_with_cftc_no_third_respondent: BooleanLike = Field(
        default="",
        description=(
            "Indicate NO if the third respondent was not registered with the CFTC at the "
            "time of the alleged violation"
        ),
    )


class AllegedViolationsandDamages(BaseModel):
    """Details of the alleged violations and claimed damages"""

    specific_portions_violated: str = Field(
        default="",
        description=(
            "Citations to specific sections of the Commodity Exchange Act, rules, or "
            'regulations allegedly violated .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    description_of_complaint: str = Field(
        ...,
        description=(
            "Detailed description of the complaint, including names, dates, facts, and how "
            'you were injured .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    amount_of_damages_claimed: str = Field(
        ...,
        description=(
            "Total dollar amount of damages you are claiming .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    explanation_of_how_damages_were_calculated: str = Field(
        ...,
        description=(
            "Explanation of the method and calculations used to arrive at the claimed "
            'damages amount .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class RelatedProceedings(BaseModel):
    """Information about related actions, decisions, and other proceedings"""

    another_action_brought_yes: BooleanLike = Field(
        default="",
        description=(
            "Select YES if you have brought another action based on the same facts in "
            "arbitration or civil court"
        ),
    )

    another_action_brought_no: BooleanLike = Field(
        default="",
        description=(
            "Select NO if you have not brought another action based on the same facts in "
            "arbitration or civil court"
        ),
    )

    case_decided_yes: BooleanLike = Field(
        default="",
        description="If another action was brought, select YES if that case has been decided",
    )

    case_decided_no: BooleanLike = Field(
        default="",
        description="If another action was brought, select NO if that case has not yet been decided",
    )

    respondents_in_receivership_or_bankruptcy_yes: BooleanLike = Field(
        default="",
        description=(
            "Select YES if, to your knowledge, any respondent is in ongoing receivership or "
            "bankruptcy proceedings"
        ),
    )

    respondents_in_receivership_or_bankruptcy_no: BooleanLike = Field(
        default="",
        description=(
            "Select NO if, to your knowledge, none of the respondents is in ongoing "
            "receivership or bankruptcy proceedings"
        ),
    )


class CommodityFuturesTradingCommissionReparationsComplaintForm(BaseModel):
    """
        Commodity Futures Trading Commission
    Reparations Complaint Form

        If the space provided on this form is not sufficient, attach your own supplementary sheets containing the required information. This form must be typed or printed legibly. Note: Fill out both sides completely.
    """

    complainant_information: ComplainantInformation = Field(
        ..., description="Complainant Information"
    )
    respondent_information: RespondentInformation = Field(..., description="Respondent Information")
    alleged_violations_and_damages: AllegedViolationsandDamages = Field(
        ..., description="Alleged Violations and Damages"
    )
    related_proceedings: RelatedProceedings = Field(..., description="Related Proceedings")
