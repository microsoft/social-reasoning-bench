from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AgencyInformation(BaseModel):
    """Information about the reporting agency and its contact details"""

    agency_name: str = Field(
        ...,
        description=(
            'Name of the reporting agency .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    policy_number: str = Field(
        ...,
        description=(
            "Errors & Omissions policy number for this insured .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Mailing address of the agency .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    contact: str = Field(
        ...,
        description=(
            "Primary contact person for this report .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Email address for the primary contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    telephone_number: str = Field(
        ...,
        description=(
            "Telephone number for the primary contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ClaimantInformation(BaseModel):
    """Information about the client/customer/claimant and their attorney"""

    name_of_client_customer_claimant: str = Field(
        ...,
        description=(
            "Full name of the client, customer, or claimant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    client_customer_claimant_address_phone_number: str = Field(
        ...,
        description=(
            "Mailing address and phone number of the client, customer, or claimant .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    client_customer_claimant_attorney_if_known: str = Field(
        default="",
        description=(
            "Name of the claimant’s attorney, if known .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    client_customer_claimant_attorney_phone_number_if_known: str = Field(
        default="",
        description=(
            "Phone number of the claimant’s attorney, if known .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class OtherInsuranceCoverage(BaseModel):
    """Details about any other Errors & Omissions insurance coverage"""

    other_eo_program_policy_yes: BooleanLike = Field(
        default="",
        description="Check if the insured has another Errors & Omissions program or policy",
    )

    other_eo_program_policy_no: BooleanLike = Field(
        default="",
        description="Check if the insured does not have another Errors & Omissions program or policy",
    )

    carriers_name: str = Field(
        default="",
        description=(
            "Name of the other Errors & Omissions insurance carrier .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    policy_number_other_eo_program_or_policy: str = Field(
        default="",
        description=(
            "Policy number of the other Errors & Omissions program or policy .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ClaimIncidentDetails(BaseModel):
    """Details regarding the alleged error, demand, and discovery"""

    monetary_demand_made_yes: BooleanLike = Field(
        default="", description="Check if a monetary demand has been made on behalf of the claimant"
    )

    monetary_demand_made_no: BooleanLike = Field(
        default="",
        description="Check if no monetary demand has been made on behalf of the claimant",
    )

    monetary_demand_amount_if_yes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of the monetary demand, if any"
    )

    manner_first_charged_with_alleged_error: str = Field(
        ...,
        description=(
            "Describe how you were first notified or charged with the alleged error .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_first_charged_in_writing: str = Field(
        ...,
        description="Date you were first charged in writing; attach a copy of the written notice",
    )  # YYYY-MM-DD format

    licensed_agent_in_this_case_yes: BooleanLike = Field(
        default="",
        description="Check if you were a licensed agent for an insurance company in this case",
    )

    licensed_agent_in_this_case_no: BooleanLike = Field(
        default="",
        description="Check if you were not a licensed agent for an insurance company in this case",
    )

    insurance_company_name: str = Field(
        default="",
        description=(
            "Name of the insurance company for which you were a licensed agent, if "
            'applicable .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    date_of_alleged_error_first_blank: str = Field(
        ..., description="First date associated with the alleged error (if multiple dates apply)"
    )  # YYYY-MM-DD format

    date_of_alleged_error_second_blank: str = Field(
        default="", description="Second date associated with the alleged error, if applicable"
    )  # YYYY-MM-DD format

    date_error_discovered: str = Field(
        ..., description="Date when the alleged error was first discovered"
    )  # YYYY-MM-DD format

    business_written_direct_or_through_another_agency_or_broker: str = Field(
        ...,
        description=(
            "Indicate whether the business was written directly or through another agency "
            'or broker .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class UticaNationalInsuranceGroupErrorsOmissions(BaseModel):
    """
        Utica National Insurance Group®
    ERRORS & OMISSIONS

        FIRST REPORT — NOTICE OF CLAIM OR INCIDENT
        PLEASE ATTACH ANY INFORMATION WHICH YOU THINK WILL BE HELPFUL IN HANDLING THIS CLAIM AGAINST YOU.
        CAUTION: DO NOT DISCUSS THIS CLAIM OR SIGN ANY STATEMENT FOR ANYONE OTHER THAN A REPRESENTATIVE OF THIS COMPANY.
    """

    agency_information: AgencyInformation = Field(..., description="Agency Information")
    claimant_information: ClaimantInformation = Field(..., description="Claimant Information")
    other_insurance_coverage: OtherInsuranceCoverage = Field(
        ..., description="Other Insurance Coverage"
    )
    claim__incident_details: ClaimIncidentDetails = Field(
        ..., description="Claim / Incident Details"
    )
