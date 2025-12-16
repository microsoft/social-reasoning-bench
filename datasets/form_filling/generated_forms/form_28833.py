from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ParentorGuardianInformation(BaseModel):
    """Child and parent / guardian details completed by the parent or guardian"""

    name_child_last_first_mi: str = Field(
        ...,
        description=(
            "Child's full legal name (last, first, middle initial) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    birthdate_child_mm_dd_yyyy: str = Field(
        ..., description="Child's date of birth in mm/dd/yyyy format"
    )  # YYYY-MM-DD format

    address_child_street_city_state_zip_code: str = Field(
        ...,
        description=(
            "Child's home address including street, city, state, and zip code .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    name_parent_or_guardian_last_first_mi: str = Field(
        ...,
        description=(
            "Parent or legal guardian's full name (last, first, middle initial) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address_parent_or_guardian_street_city_state_zip_code: str = Field(
        ...,
        description=(
            "Parent or guardian's mailing address including street, city, state, and zip "
            'code .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class HealthProfessional(BaseModel):
    """Health information and medical instructions completed by the health professional"""

    instructions_for_feeding_and_care_of_child_with_special_problems_including_allergies_specify: str = Field(
        default="",
        description=(
            "Detailed instructions for feeding and care related to special problems or "
            "allergies; attach additional information if needed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    yes_does_the_child_have_a_milk_allergy: BooleanLike = Field(
        ..., description="Check if the child has a diagnosed milk allergy"
    )

    no_does_the_child_have_a_milk_allergy: BooleanLike = Field(
        ..., description="Check if the child does not have a diagnosed milk allergy"
    )

    recommended_milk_substitute: str = Field(
        default="",
        description=(
            "If the child has a milk allergy, specify the recommended milk substitute .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_of_most_recent_blood_lead_test_mm_dd_yyyy: str = Field(
        default="",
        description="Most recent date the child received a blood lead test in mm/dd/yyyy format",
    )  # YYYY-MM-DD format

    immunizations_not_to_be_administered_to_child_due_to_medical_reasons_specify: str = Field(
        default="",
        description=(
            "List any immunizations that should not be given to the child and the medical "
            'reasons .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Authorization(BaseModel):
    """Provider certification and exam details"""

    name_md_pa_or_healthcheck_provider_type_or_print: str = Field(
        ...,
        description=(
            "Printed name of the medical doctor, physician assistant, or HealthCheck "
            'provider .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    address_md_pa_or_healthcheck_provider_street_city_state_zip_code: str = Field(
        ...,
        description=(
            "Business address of the MD, PA, or HealthCheck provider including street, "
            'city, state, and zip code .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    signature_md_pa_or_healthcheck_provider: str = Field(
        ...,
        description=(
            "Signature of the MD, PA, or HealthCheck provider who examined the child .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_of_examination: str = Field(
        ..., description="Date the child was examined by the health professional"
    )  # YYYY-MM-DD format


class ChildHealthReportChildCareCenters(BaseModel):
    """
    CHILD HEALTH REPORT – CHILD CARE CENTERS

    Use of form: Use of this form is voluntary; however, completion of this form meets the requirements of DCF 202.08(4), DCF 250.07(6)(L)3., and DCF 251.07(6)(k)3. Failure to comply with these rules may result in issuance of a noncompliance statement. Personal information you provide may be used for secondary purposes [Privacy Law, s. 15.04(1)(m), Wisconsin Statutes].
    """

    parent_or_guardian_information: ParentorGuardianInformation = Field(
        ..., description="Parent or Guardian Information"
    )
    health_professional: HealthProfessional = Field(..., description="Health Professional")
    authorization: Authorization = Field(..., description="Authorization")
