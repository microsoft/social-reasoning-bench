from typing import List, Literal, Optional, Union

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

    date: str = Field(
        ..., description="Date the requesting party completes Part I"
    )  # YYYY-MM-DD format

    time_local_hrs: str = Field(
        ...,
        description=(
            "Local time in hours when the form is completed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mission_no: str = Field(
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
            "Name of the primary point of contact for the requesting party .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    telephone_no: str = Field(
        ...,
        description=(
            "Telephone number for the point of contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
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
            "Name of the jurisdiction or entity requesting assistance .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    assisting_party: str = Field(
        ...,
        description=(
            "Name of the jurisdiction or entity providing assistance .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    incident_requiring_assistance: str = Field(
        ...,
        description=(
            "Description of the incident or event requiring mutual aid .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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
            "Estimated date and time when resources will be released .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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
            "Title or position of the authorized official (Part I) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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

    contact_person: str = Field(
        ...,
        description=(
            "Primary contact person for the assisting party .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_no_assisting_party: str = Field(
        ...,
        description=(
            "Telephone number for the assisting party contact person .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address_assisting_party: str = Field(
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
            "Date and time when the assisting party’s resources are available .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    to_date_time_resources_available: str = Field(
        ...,
        description=(
            "End date and time through which resources are available .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    location_address_part_ii: str = Field(
        ...,
        description=(
            "Address where the assisting party’s resources will report or be deployed .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    approximate_total_cost_for_mission: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated total cost for the mission in dollars"
    )

    travel: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated travel cost in dollars"
    )

    personnel: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated personnel cost in dollars"
    )

    equipment_materials: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated equipment and materials cost in dollars"
    )

    contract_rental: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated contract rental cost in dollars"
    )

    logistics_required_from_requesting_party_yes: BooleanLike = Field(
        default="",
        description="Indicate Yes if logistics support is required from the requesting party",
    )

    logistics_required_from_requesting_party_no: BooleanLike = Field(
        default="",
        description="Indicate No if logistics support is not required from the requesting party",
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
            "Title or position of the authorized official (Part II) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_part_ii: str = Field(
        ..., description="Date the assisting party completes Part II"
    )  # YYYY-MM-DD format

    signature_part_ii: str = Field(
        ...,
        description=(
            "Signature of the authorized official for the assisting party (Part II) .If you "
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
            "Title or position of the authorized official (Part III) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_part_iii: str = Field(
        ...,
        description=(
            "Signature of the authorized official for the requesting party (Part III) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    agency_part_iii: str = Field(
        ...,
        description=(
            "Agency or organization of the authorized official (Part III) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
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
