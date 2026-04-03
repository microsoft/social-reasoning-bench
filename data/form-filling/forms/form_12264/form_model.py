from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PartIRequestingParty(BaseModel):
    """Information to be completed by the requesting party"""

    date_part_i: str = Field(
        ..., description="Date this request form (Part I) is completed"
    )  # YYYY-MM-DD format

    time_part_i: str = Field(
        ...,
        description=(
            "Local time this request form (Part I) is completed, in hours .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    mission_no_part_i: str = Field(
        ...,
        description=(
            "Mission number assigned to this request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    point_of_contact: str = Field(
        ...,
        description=(
            "Primary point of contact for the requesting party .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_no_part_i: str = Field(
        ...,
        description=(
            "Telephone number for the point of contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address_part_i: str = Field(
        ...,
        description=(
            "Email address for the point of contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    requesting_party: str = Field(
        ...,
        description=(
            "Name of the jurisdiction or agency requesting assistance .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    assisting_party: str = Field(
        ...,
        description=(
            "Name of the jurisdiction or agency providing assistance .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    incident_requiring_assistance: str = Field(
        ...,
        description=(
            "Description of the incident or event requiring mutual aid assistance .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    type_of_assistance_resources_needed: str = Field(
        ...,
        description=(
            "Description of the specific assistance or resources requested .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_time_resources_needed: str = Field(
        ...,
        description=(
            "Date and time when requested resources are needed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    location_address_part_i: str = Field(
        ...,
        description=(
            "Address where the requested resources are needed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    approximated_date_time_resources_released: str = Field(
        default="",
        description=(
            "Estimated date and time when resources will be released from the mission .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    authorized_officials_name_part_i: str = Field(
        ...,
        description=(
            "Name of the authorized official for the requesting party (Part I) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    signature_part_i: str = Field(
        ...,
        description=(
            "Signature of the authorized official for the requesting party (Part I) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    title_part_i: str = Field(
        ...,
        description=(
            "Official title or position of the authorized official (Part I) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    agency_part_i: str = Field(
        ...,
        description=(
            "Agency or organization of the authorized official (Part I) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PartIIAssistingParty(BaseModel):
    """Information to be completed by the assisting party"""

    contact_person_part_ii: str = Field(
        ...,
        description=(
            "Primary contact person for the assisting party .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_no_part_ii: str = Field(
        ...,
        description=(
            "Telephone number for the assisting party contact person .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address_part_ii: str = Field(
        ...,
        description=(
            "Email address for the assisting party contact person .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    type_of_assistance_available: str = Field(
        ...,
        description=(
            "Description of the assistance or resources the assisting party can provide .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_time_resources_available: str = Field(
        ...,
        description=(
            "Date and time when the assisting party’s resources will be available .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    to_time_part_ii: str = Field(
        default="",
        description=(
            "End date and/or time through which resources will be available .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    location_address_part_ii: str = Field(
        ...,
        description=(
            "Location or address where assisting party resources will report or be staged "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    approximate_total_cost_for_mission: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated total cost for the mission in dollars"
    )

    travel_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated travel cost in dollars"
    )

    personnel_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated personnel cost in dollars"
    )

    equipment_materials_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated equipment and materials cost in dollars"
    )

    contract_rental_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated contract rental cost in dollars"
    )

    logistics_required_from_requesting_party_yes: BooleanLike = Field(
        default="",
        description="Indicates that logistics support is required from the requesting party",
    )

    logistics_required_from_requesting_party_no: BooleanLike = Field(
        default="",
        description="Indicates that logistics support is not required from the requesting party",
    )

    authorized_officials_name_part_ii: str = Field(
        ...,
        description=(
            "Name of the authorized official for the assisting party (Part II) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    title_part_ii: str = Field(
        ...,
        description=(
            "Official title or position of the assisting party’s authorized official (Part "
            'II) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date_part_ii: str = Field(
        ..., description="Date the assisting party’s authorized official signs (Part II)"
    )  # YYYY-MM-DD format

    signature_part_ii: str = Field(
        ...,
        description=(
            "Signature of the assisting party’s authorized official (Part II) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    local_mission_no: str = Field(
        default="",
        description=(
            "Local mission number assigned by the assisting party .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PartIIIRequestingPartyAuthorization(BaseModel):
    """Final authorization by the requesting party"""

    authorized_officials_name_part_iii: str = Field(
        ...,
        description=(
            "Name of the authorized official for the requesting party (Part III) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    title_part_iii: str = Field(
        ...,
        description=(
            "Official title or position of the requesting party’s authorized official (Part "
            'III) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    signature_part_iii: str = Field(
        ...,
        description=(
            "Signature of the requesting party’s authorized official (Part III) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    agency_part_iii: str = Field(
        ...,
        description=(
            "Agency or organization of the requesting party’s authorized official (Part "
            'III) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Attachment1StatewideMutualAidAgreementFormB(BaseModel):
    """
        Attachment 1

    STATEWIDE MUTUAL AID AGREEMENT
    Form B

        Type or print all information except signatures
    """

    part_i___requesting_party: PartIRequestingParty = Field(
        ..., description="Part I - Requesting Party"
    )
    part_ii___assisting_party: PartIIAssistingParty = Field(
        ..., description="Part II - Assisting Party"
    )
    part_iii___requesting_party_authorization: PartIIIRequestingPartyAuthorization = Field(
        ..., description="Part III - Requesting Party Authorization"
    )
