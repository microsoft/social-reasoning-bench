from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RequiredInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Basic and required information about the organization and contact person."""

    organization_name: str = Field(
        ...,
        description=(
            "Full legal name of the organization .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    type_of_organization_covenant_based_homeowners_association: BooleanLike = Field(
        ...,
        description="Check if the organization is a covenant-based homeowner's association"
    )

    type_of_organization_other_incorporated: BooleanLike = Field(
        ...,
        description="Check if the organization is another type of incorporated entity"
    )

    type_of_organization_non_profit: BooleanLike = Field(
        ...,
        description="Check if the organization is a non-profit"
    )

    type_of_organization_llc: BooleanLike = Field(
        ...,
        description="Check if the organization is an LLC"
    )

    type_of_organization_other: str = Field(
        ...,
        description=(
            "Specify other type of organization .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    commission_districts: str = Field(
        ...,
        description=(
            "Commission districts covered by the organization .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    contact_person: str = Field(
        ...,
        description=(
            "Primary contact person for the organization .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    contact_person_mailing_address: str = Field(
        ...,
        description=(
            "Mailing address for the contact person .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    neighborhood_mailing_address_if_different: str = Field(
        ...,
        description=(
            "Neighborhood mailing address if different from contact person .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )

    telephone_number: str = Field(
        ...,
        description=(
            "Primary telephone number for contact .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    e_mail_address: str = Field(
        ...,
        description=(
            "Valid email address for the contact person .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class OptionalInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Additional, non-required information about the organization."""

    website: str = Field(
        ...,
        description=(
            "Website URL for the organization .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    newsletter_or_other_publication: str = Field(
        ...,
        description=(
            "Name or description of newsletter or other publication .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    regularly_scheduled_meetings_provide_date_time_and_location: str = Field(
        ...,
        description=(
            "Details of regularly scheduled meetings (date, time, location) .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )

    comments_questions_or_suggested_topics_for_neighborhood_planning_workshops: str = Field(
        ...,
        description=(
            "Comments, questions, or suggested topics for workshops .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )


class AdministrativeUse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """For use by the Planning Department."""

    date_received_by_planning_department: str = Field(
        ...,
        description="Date the form was received by the Planning Department"
    )  # YYYY-MM-DD format

    date_approved_by_mayor_and_commission: str = Field(
        ...,
        description="Date the form was approved by Mayor and Commission"
    )  # YYYY-MM-DD format


class RequiredInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    REQUIRED INFORMATION

    This form is used to register a neighborhood organization with the Planning Department. It collects required information about the organization, including its name, type, contact person, and boundaries, and requests supporting documentation to verify the organization's structure or formation. The form also provides space for optional information such as website, publications, meeting details, and suggestions for neighborhood planning workshops. A valid email address for the contact person is required to receive neighborhood notifications.
    """

    required_information: RequiredInformation = Field(
        ...,
        description="Required Information"
    )
    optional_information: OptionalInformation = Field(
        ...,
        description="Optional Information"
    )
    administrative_use: AdministrativeUse = Field(
        ...,
        description="Administrative Use"
    )