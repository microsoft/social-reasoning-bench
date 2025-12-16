from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AccidentalDeathClaimDetails(BaseModel):
    """Information about the group, insured, deceased, and accident circumstances"""

    group_name: str = Field(
        ...,
        description=(
            "Name of the group or employer associated with the policy .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_insured: str = Field(
        ...,
        description=(
            "Full name of the insured person under the policy .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_deceased_if_different_from_above: str = Field(
        default="",
        description=(
            "Full name of the deceased, if not the same as the insured .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    relationship_to_insured: str = Field(
        default="",
        description=(
            "Relationship of the deceased to the insured person .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    on_what_date_did_the_accident_occur_mm_dd_yy: str = Field(
        ..., description="Date on which the accident occurred, in MM/DD/YY format"
    )  # YYYY-MM-DD format

    where_did_the_accident_occur_address_city_state: str = Field(
        ...,
        description=(
            "Location where the accident occurred, including address, city, and state .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    describe_in_detail_how_the_accident_occurred: str = Field(
        ...,
        description=(
            "Detailed description of the circumstances of the accident .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    did_the_deceased_have_any_disease_or_physical_defect_yes: BooleanLike = Field(
        ..., description="Indicate Yes if the deceased had any disease or physical defect"
    )

    did_the_deceased_have_any_disease_or_physical_defect_no: BooleanLike = Field(
        ..., description="Indicate No if the deceased did not have any disease or physical defect"
    )

    if_yes_please_describe_in_detail: str = Field(
        default="",
        description=(
            "If the deceased had a disease or physical defect, provide detailed description "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    was_a_police_or_other_investigative_report_completed_yes: BooleanLike = Field(
        ..., description="Indicate Yes if a police or other investigative report was completed"
    )

    was_a_police_or_other_investigative_report_completed_no: BooleanLike = Field(
        ..., description="Indicate No if no police or other investigative report was completed"
    )

    contact_information_for_official_investigative_report: str = Field(
        default="",
        description=(
            "Contact details or other information related to the official investigative "
            'report .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    list_physicians_who_treated_deceased_for_accident: str = Field(
        default="",
        description=(
            "Names, addresses, and phone numbers of all physicians who treated the deceased "
            'for the accident .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    list_hospitals_who_treated_deceased_for_accident: str = Field(
        default="",
        description=(
            "Names, addresses, and phone numbers of all hospitals that treated the deceased "
            'for the accident .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    was_an_autopsy_performed_yes: BooleanLike = Field(
        ..., description="Indicate Yes if an autopsy was performed"
    )

    was_an_autopsy_performed_no: BooleanLike = Field(
        ..., description="Indicate No if an autopsy was not performed"
    )

    contact_information_for_autopsy_report: str = Field(
        default="",
        description=(
            "Contact details or other information related to the autopsy report .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PersonCompletingForm(BaseModel):
    """Contact details and signature of the person completing this form"""

    person_completing_form: str = Field(
        ...,
        description=(
            "Name of the person completing this form .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Phone number of the person completing the form .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address of the person completing the form .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City of the person completing the form .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of residence of the person completing the form")

    zip: str = Field(..., description="ZIP code of the person completing the form")

    relationship_to_deceased: str = Field(
        ...,
        description=(
            "Relationship of the person completing the form to the deceased .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    signature_of_person_completing_this_form: str = Field(
        ...,
        description=(
            "Signature of the person who completed the form .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the form was signed")  # YYYY-MM-DD format


class AccidentalDeathBenefitInformation(BaseModel):
    """
    ACCIDENTAL DEATH BENEFIT INFORMATION

    A beneficiary or the personal/legal representative of the deceased will only complete this page when applying for Accidental Death Benefits.
    """

    accidental_death_claim_details: AccidentalDeathClaimDetails = Field(
        ..., description="Accidental Death Claim Details"
    )
    person_completing_form: PersonCompletingForm = Field(..., description="Person Completing Form")
