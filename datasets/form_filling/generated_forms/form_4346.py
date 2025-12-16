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
    """Basic information and contact details for the complainant"""

    date: str = Field(
        ..., description="Date this grievance/complaint form is being completed"
    )  # YYYY-MM-DD format

    name_of_complainant: str = Field(
        ...,
        description=(
            "Full name of the person making the complaint .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address of the complainant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the complainant\'s address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the complainant's address")

    zip: str = Field(..., description="ZIP code of the complainant's address")

    telephone: str = Field(
        ...,
        description=(
            "Primary telephone number for the complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        default="",
        description=(
            'Email address for the complainant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    preferred_way_to_be_contacted: str = Field(
        default="",
        description=(
            "Preferred method of contact (e.g., phone, email, mail) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FilingPartyWitnessRepresentative(BaseModel):
    """Information if the grievance is filed by a witness or on behalf of another person"""

    i_am_filing_as_a_witness_my_name_is: str = Field(
        default="",
        description=(
            "Name of the witness filing the complaint, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    i_am_filing_on_behalf_of_another_person_my_name_is: str = Field(
        default="",
        description=(
            "Name of the person filing on behalf of someone else, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address_of_person_filing_grievance_if_different: str = Field(
        default="",
        description=(
            "Street address of the person filing the grievance if different from the "
            'complainant .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    city_for_person_filing_grievance_if_different: str = Field(
        default="",
        description=(
            "City of the person filing the grievance if different from the complainant .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    state_for_person_filing_grievance_if_different: str = Field(
        default="",
        description="State of the person filing the grievance if different from the complainant",
    )

    zip_for_person_filing_grievance_if_different: str = Field(
        default="",
        description="ZIP code of the person filing the grievance if different from the complainant",
    )

    telephone_for_person_filing_grievance_if_different: str = Field(
        default="",
        description=(
            "Telephone number of the person filing the grievance if different from the "
            'complainant .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    email_address_for_person_filing_grievance_if_different: str = Field(
        default="",
        description=(
            "Email address of the person filing the grievance if different from the "
            'complainant .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class IncidentDetails(BaseModel):
    """Details about the alleged discrimination and requested resolution"""

    date_the_discrimination_occurred: str = Field(
        ..., description="Date on which the alleged discrimination took place"
    )  # YYYY-MM-DD format

    who_committed_the_alleged_discrimination: str = Field(
        ...,
        description=(
            "Name or description of the person, department, or entity that committed the "
            'alleged discrimination .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    location_of_the_discrimination_if_applicable: str = Field(
        default="",
        description=(
            "Location where the alleged discrimination occurred .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    detailed_description_of_complaint_grievance: str = Field(
        ...,
        description=(
            "Detailed narrative of the complaint or grievance, including what happened and "
            'who was involved .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    proposed_resolution_of_grievance: str = Field(
        default="",
        description=(
            "What actions or outcomes you believe would resolve this grievance .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class CityOfSantaFeAdaGrievancecomplaintForm(BaseModel):
    """City of Santa Fe
    ADA Grievance/Complaint Form"""

    complainant_information: ComplainantInformation = Field(
        ..., description="Complainant Information"
    )
    filing_party_witnessrepresentative: FilingPartyWitnessRepresentative = Field(
        ..., description="Filing Party (Witness/Representative)"
    )
    incident_details: IncidentDetails = Field(..., description="Incident Details")
