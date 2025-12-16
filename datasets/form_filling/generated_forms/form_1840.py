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
    """Basic information about the insured applicant and business entity"""

    insureds: str = Field(
        ...,
        description=(
            "Named insured(s) applying for coverage .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    street_address: str = Field(
        ...,
        description=(
            'Street address of the insured .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the insured\'s address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the insured's address")

    zip_code: str = Field(..., description="Zip code of the insured's address")

    contact_name: str = Field(
        ...,
        description=(
            'Primary contact person\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_title: str = Field(
        ...,
        description=(
            "Job title or position of the primary contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            'Primary business telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            'Company website URL .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    year_established: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year the business was established"
    )

    the_insured_is_an_individual: BooleanLike = Field(
        default="", description="Check if the insured is an individual"
    )

    the_insured_is_an_corporation: BooleanLike = Field(
        default="", description="Check if the insured is a corporation"
    )

    the_insured_is_an_llc: BooleanLike = Field(
        default="", description="Check if the insured is a limited liability company (LLC)"
    )

    the_insured_is_an_public_entity: BooleanLike = Field(
        default="", description="Check if the insured is a public entity"
    )

    the_insured_is_an_partnership: BooleanLike = Field(
        default="", description="Check if the insured is a partnership"
    )

    the_insured_is_an_joint_venture: BooleanLike = Field(
        default="", description="Check if the insured is a joint venture"
    )

    the_insured_is_an_not_for_profit: BooleanLike = Field(
        default="", description="Check if the insured is a not-for-profit organization"
    )

    the_insured_is_an_other: str = Field(
        default="",
        description=(
            "Describe the insured's entity type if 'Other' is selected .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    associated_controlled_owned_yes: BooleanLike = Field(
        default="",
        description=(
            "Select 'Yes' if the applicant is associated with, controlled by, or owned by "
            "another person or entity"
        ),
    )

    associated_controlled_owned_no: BooleanLike = Field(
        default="",
        description=(
            "Select 'No' if the applicant is not associated with, controlled by, or owned "
            "by another person or entity"
        ),
    )

    association_explanation: str = Field(
        default="",
        description=(
            "Explanation of any association with, control by, or ownership by another "
            'person or entity .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    past_five_years_name_or_entity_changed: BooleanLike = Field(
        default="",
        description=(
            "Indicate if the applicant's name or type of business entity has changed in the "
            "past five years"
        ),
    )

    past_five_years_discontinued_operations: BooleanLike = Field(
        default="",
        description=(
            "Indicate if the applicant has discontinued any operations in the past five years"
        ),
    )

    past_five_years_purchased_merged_consolidated: BooleanLike = Field(
        default="",
        description=(
            "Indicate if any other person or entity has been purchased by, merged with, or "
            "consolidated into the applicant in the past five years"
        ),
    )

    past_five_discontinued_merged_yes: BooleanLike = Field(
        default="",
        description=(
            "Select 'Yes' if any of the past five years / discontinued / merged questions "
            "are answered yes"
        ),
    )

    past_five_discontinued_merged_no: BooleanLike = Field(
        default="",
        description=(
            "Select 'No' if none of the past five years / discontinued / merged questions apply"
        ),
    )

    past_five_discontinued_merged_explanation: str = Field(
        default="",
        description=(
            "Explanation of any changes, discontinued operations, or mergers/acquisitions "
            'in the past five years .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class PersonnelInformation(BaseModel):
    """Details about personnel counts and employee certifications"""

    principals_officers_directors_number: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of principals, officers, and directors"
    )

    architects_number: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of architects employed or contracted"
    )

    engineers_number: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of engineers employed or contracted"
    )

    geologists_scientists_industrial_hygienists_number: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of geologists, scientists, and industrial hygienists"
    )

    project_managers_supervisors_foremen_number: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of project managers, supervisors, and foremen"
    )

    field_personnel_number: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of field personnel"
    )

    drivers_number: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of drivers"
    )

    volunteers_number: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of volunteers"
    )

    other_type_of_personnel_number: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of personnel in other categories not listed"
    )

    types_of_certifications_held_by_employees: str = Field(
        default="",
        description=(
            "List the professional or technical certifications held by employees .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ApplicationForContractorsPollutionLiability(BaseModel):
    """
        Application for
    Contractors Pollution Liability

        Please complete the application in its entirety.
        Note: Completion of this application does not bind coverage. The applicant's acceptance of the Company's quotation is required prior to binding coverage.
        This application must be signed and dated by an authorized representative of your company.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    personnel_information: PersonnelInformation = Field(..., description="Personnel Information")
