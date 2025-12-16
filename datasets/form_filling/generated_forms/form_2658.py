from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantandFamilyParticulars(BaseModel):
    """Personal, nationality, and family-related details of the applicant"""

    name_of_applicant: str = Field(
        ...,
        description=(
            "Full legal name of the visa applicant as in passport .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    passport_number_and_nationality: str = Field(
        ...,
        description=(
            "Current passport number and nationality shown in the passport .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    please_specify_whether_holding_dual_nationality: BooleanLike = Field(
        ..., description="Indicate whether the applicant currently holds dual nationality"
    )

    dual_nationality_countries_and_passport_numbers: str = Field(
        default="",
        description=(
            "If holding dual nationality, list all countries and corresponding passport "
            'numbers .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    any_previous_nationality_held_if_yes_specify: str = Field(
        default="",
        description=(
            "State any previous nationalities held by the applicant and provide details .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    name_of_spouse_and_current_nationality: str = Field(
        default="",
        description=(
            "Full name of spouse and spouse's current nationality .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    spouse_previous_nationalities_and_passport_numbers: str = Field(
        default="",
        description=(
            "List any other nationalities previously held by the spouse, including country "
            'names and passport numbers .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    has_applicant_ever_changed_name_details: str = Field(
        default="",
        description=(
            "Indicate if the applicant has ever changed their name and provide full details "
            'with dates and documents .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    citizenship_of_specified_countries_details: str = Field(
        default="",
        description=(
            "Provide details if the applicant, parents, or grandparents ever held "
            "citizenship of Bangladesh, Afghanistan, Bhutan, China, Nepal, or Sri Lanka .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    citizenship_of_pakistan_nicop_poc_details: str = Field(
        default="",
        description=(
            "Provide details if the applicant, parents, or grandparents ever held Pakistani "
            'citizenship, NICOP, or POC .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class EmploymentandOfficialStatus(BaseModel):
    """Employment history, government service, and official passport details"""

    armed_forces_police_government_service_details: str = Field(
        default="",
        description=(
            "If the applicant has worked or is working with Armed Forces, Police, "
            "Para-Military, or Government service, provide organization, designation, "
            'posting place, and rank .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    official_diplomatic_passport_details: str = Field(
        default="",
        description=(
            "State whether the applicant ever held an official or diplomatic passport and "
            'provide details .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    current_employment_status_and_employer_details: str = Field(
        ...,
        description=(
            "Describe current employment status and provide full employer details including "
            "name, address, and contact information .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class LegalandAsylumHistory(BaseModel):
    """Criminal record and asylum-related information"""

    criminal_offense_or_charges_details: str = Field(
        default="",
        description=(
            "Indicate any past convictions or ongoing criminal charges and provide full "
            'details .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    asylum_application_details: str = Field(
        default="",
        description=(
            "Provide details if the applicant or any parent has ever applied for asylum in "
            'any country .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class PIOCardDeclaration(BaseModel):
    """Declaration related to PIO card application as spouse or not"""

    pio_as_spouse_of_indian_origin_person: BooleanLike = Field(
        default="",
        description="Select if applying for a PIO card as the spouse of a person of Indian origin",
    )

    pio_not_as_spouse_of_indian_origin_person: BooleanLike = Field(
        default="",
        description=(
            "Select if applying for a PIO card not as the spouse of a person of Indian origin"
        ),
    )


class DeclarationandSignatures(BaseModel):
    """Signing details for applicant and, in case of minor, parents/guardians"""

    date: str = Field(
        ..., description="Date on which the declaration is signed"
    )  # YYYY-MM-DD format

    place: str = Field(
        ...,
        description=(
            "City and country where the declaration is signed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_the_applicant: str = Field(
        ...,
        description=(
            "Signature of the applicant confirming the declaration .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_parent_legal_guardian_1: str = Field(
        default="",
        description=(
            "Signature of the first parent or legal guardian if the applicant is a minor "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    signature_of_parent_legal_guardian_2: str = Field(
        default="",
        description=(
            "Signature of the second parent or legal guardian if the applicant is a minor "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class AdditionalParticularsFormForVisaServices(BaseModel):
    """
    ADDITIONAL PARTICULARS FORM FOR VISA SERVICES

    ''
    """

    applicant_and_family_particulars: ApplicantandFamilyParticulars = Field(
        ..., description="Applicant and Family Particulars"
    )
    employment_and_official_status: EmploymentandOfficialStatus = Field(
        ..., description="Employment and Official Status"
    )
    legal_and_asylum_history: LegalandAsylumHistory = Field(
        ..., description="Legal and Asylum History"
    )
    pio_card_declaration: PIOCardDeclaration = Field(..., description="PIO Card Declaration")
    declaration_and_signatures: DeclarationandSignatures = Field(
        ..., description="Declaration and Signatures"
    )
