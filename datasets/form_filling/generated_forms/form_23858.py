from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Basic information about the insured/applicant"""

    insured_name: str = Field(
        ...,
        description=(
            "Full legal name of the insured entity or individual .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            'Street mailing address of the insured .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City for the mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the mailing address")

    zip: str = Field(..., description="ZIP code for the mailing address")

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            'Fax number .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            'Primary contact email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    applicant_is_individual: BooleanLike = Field(
        ..., description="Check if the applicant is an individual"
    )

    applicant_is_corporation: BooleanLike = Field(
        ..., description="Check if the applicant is a corporation"
    )

    applicant_is_partnership: BooleanLike = Field(
        ..., description="Check if the applicant is a partnership"
    )

    applicant_is_joint_venture: BooleanLike = Field(
        ..., description="Check if the applicant is a joint venture"
    )

    applicant_is_other: str = Field(
        default="",
        description=(
            "If 'Other' is selected, specify the applicant type .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_business_established: str = Field(
        default="", description="Date the business was originally established"
    )  # YYYY-MM-DD format


class HauntedHouseInformation(BaseModel):
    """Details about the haunted house location and operations"""

    locations_name_and_address_if_different_than_above_name: str = Field(
        default="",
        description=(
            "Name of the haunted house location if different from the insured name .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    locations_name_and_address_if_different_than_above_address: str = Field(
        default="",
        description=(
            "Street address of the haunted house location if different from mailing address "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    locations_name_and_address_if_different_than_above_city: str = Field(
        default="",
        description=(
            'City of the haunted house location .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    locations_name_and_address_if_different_than_above_state: str = Field(
        default="", description="State of the haunted house location"
    )

    locations_name_and_address_if_different_than_above_zip: str = Field(
        default="", description="ZIP code of the haunted house location"
    )

    website_address: str = Field(
        default="",
        description=(
            "Website URL for the haunted house or insured .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    hours_of_operation: str = Field(
        ...,
        description=(
            "Typical hours and days the haunted house operates .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    event_description: str = Field(
        ...,
        description=(
            "Detailed description of the haunted house event; attach any promotional "
            'material if available .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    haunted_hayride_yes: BooleanLike = Field(
        ..., description="Indicate 'Yes' if the event includes a haunted hayride"
    )

    haunted_hayride_no: BooleanLike = Field(
        ..., description="Indicate 'No' if the event does not include a haunted hayride"
    )

    effective_date: str = Field(
        ..., description="Policy effective date or start date of coverage"
    )  # YYYY-MM-DD format

    end_date: str = Field(
        ..., description="Policy end date or end date of coverage"
    )  # YYYY-MM-DD format

    estimated_attendance: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated total attendance for the event"
    )

    last_years_attendance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total attendance at last year’s event"
    )

    maximum_capacity_at_event_location: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Maximum number of people allowed at the event location at one time"
    )


class HauntedHouseGeneralLiabilityApplication(BaseModel):
    """
        Haunted House
    General Liability Application

        ''
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    haunted_house_information: HauntedHouseInformation = Field(
        ..., description="Haunted House Information"
    )
