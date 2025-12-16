from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Eo50ComplianceEmploymentReport(BaseModel):
    """
    E.O. 50 COMPLIANCE: EMPLOYMENT REPORT

    ''
    """

    number_of_full_time_employees: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of full-time employees in the firm or entity."
    )

    employment_report_already_submitted_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate YES if an Employment Report has already been submitted for a "
            "different contract for which a compliance certificate has not yet been "
            "received."
        ),
    )

    employment_report_already_submitted_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate NO if no such Employment Report has been submitted for a different contract."
        ),
    )

    date_submitted: str = Field(
        default="", description="Date on which the other Employment Report was submitted."
    )  # YYYY-MM-DD format

    agency_to_which_submitted: str = Field(
        default="",
        description=(
            "Name of the agency to which the other Employment Report was submitted. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    name_of_agency_person: str = Field(
        default="",
        description=(
            "Name of the contact person at the agency. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contract_no: str = Field(
        default="",
        description=(
            "Contract number associated with the previously submitted Employment Report. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    telephone: str = Field(
        default="",
        description=(
            "Telephone number for the agency contact person. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ext: str = Field(
        default="",
        description=(
            "Telephone extension for the agency contact person, if applicable. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    trade_association_member_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate YES if your company or its affiliates belong to an employers' trade "
            "association that negotiates CBAs affecting construction site hiring."
        ),
    )

    trade_association_member_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate NO if your company or its affiliates are not members of such an "
            "employers' trade association."
        ),
    )

    name_of_parent_company: str = Field(
        default="",
        description=(
            "Legal name of the parent company, if applicable. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employer_identification_number_or_federal_tax_id: str = Field(
        default="",
        description=(
            "Employer Identification Number (EIN) or Federal Tax ID of the parent company. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    parent_company_address_and_zip_code: str = Field(
        default="",
        description=(
            "Mailing address and ZIP code of the parent company. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    company_telephone: str = Field(
        default="",
        description=(
            "Telephone number of the parent company. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        default="",
        description=(
            "Email address for the parent company or primary contact. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    president_or_ceo: str = Field(
        default="",
        description=(
            "Name of the President or Chief Executive Officer of the parent company. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    firm_reviewed_by_dls_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate YES if your firm has been reviewed by SBS/DLS within the past 36 months."
        ),
    )

    firm_reviewed_by_dls_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate NO if your firm has not been reviewed by SBS/DLS within the past 36 months."
        ),
    )
