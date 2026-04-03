from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class TenancyDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the property and tenancy commencement"""

    property_address: str = Field(
        ...,
        description=(
            "Address of the property you are applying to rent .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    commencement_of_tenancy: str = Field(
        ...,
        description=(
            "Planned start date or description of tenancy commencement .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    date: str = Field(
        ...,
        description="Date the tenancy is to commence"
    )  # YYYY-MM-DD format


class ApplicantDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Personal information about the applicant"""

    full_name: str = Field(
        ...,
        description=(
            "Applicant's full legal name .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    date_of_birth: str = Field(
        ...,
        description="Applicant's date of birth"
    )  # YYYY-MM-DD format

    phone_number: str = Field(
        ...,
        description=(
            "Applicant's primary phone number .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    mobile_phone: str = Field(
        ...,
        description=(
            "Applicant's mobile phone number .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    email: str = Field(
        ...,
        description=(
            "Applicant's email address .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    current_address: str = Field(
        ...,
        description=(
            "Applicant's current residential address .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    how_long_have_you_lived_there_years: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of years at current address"
    )

    how_long_have_you_lived_there_months: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of months at current address (in addition to years)"
    )

    please_state_why_you_are_leaving_this_address: str = Field(
        ...,
        description=(
            "Reason for leaving your current address .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class Identification(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Identification details for verification purposes"""

    drivers_licence_number: str = Field(
        ...,
        description=(
            "Your driver's licence number (optional, for identity verification) .If you "
            "cannot fill this, write \"N/A\". If this field should not be filled by you "
            "(for example, it belongs to another person or office), leave it blank (empty "
            "string \"\")."
        )
    )

    version_no_if_applicable: str = Field(
        ...,
        description=(
            "Driver's licence version number (if applicable) .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    alternative_form_of_id: str = Field(
        ...,
        description=(
            "Alternative identification if no driver's licence is provided .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )


class CurrentLandlordsDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Contact information for current landlord and reference permission"""

    landlord_name: str = Field(
        ...,
        description=(
            "Current landlord's full name .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    landlord_phone_number: str = Field(
        ...,
        description=(
            "Current landlord's phone number .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    landlord_mobile_phone: str = Field(
        ...,
        description=(
            "Current landlord's mobile phone number .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    landlord_email: str = Field(
        ...,
        description=(
            "Current landlord's email address .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    may_i_contact_this_person_for_a_reference_yes: BooleanLike = Field(
        ...,
        description="Permission to contact landlord for a reference (Yes)"
    )

    may_i_contact_this_person_for_a_reference_no: BooleanLike = Field(
        ...,
        description="Permission to contact landlord for a reference (No)"
    )


class TenancyservicesPretenancyApplicationForm(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    TenancyServices

Pre-tenancy application form

    Please complete this form to apply for the tenancy at the address below. The information you provide is for applying for this tenancy and may be used for a credit and reference check. Your privacy is protected under the Privacy Act 2020.
    """

    tenancy_details: TenancyDetails = Field(
        ...,
        description="Tenancy Details"
    )
    applicant_details: ApplicantDetails = Field(
        ...,
        description="Applicant Details"
    )
    identification: Identification = Field(
        ...,
        description="Identification"
    )
    current_landlords_details: CurrentLandlordsDetails = Field(
        ...,
        description="Current Landlord’s Details"
    )