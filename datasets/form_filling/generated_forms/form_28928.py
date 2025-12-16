from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicationDetails(BaseModel):
    """General application information and applicant personal/business details"""

    application_date: str = Field(
        ..., description="Date this membership application is completed"
    )  # YYYY-MM-DD format

    surname: str = Field(
        ...,
        description=(
            'Applicant\'s family name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    given_names: str = Field(
        ...,
        description=(
            'Applicant\'s first and middle names .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    business_name: str = Field(
        default="",
        description=(
            'Registered business or trading name .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    abn_no: str = Field(
        default="",
        description=(
            'Australian Business Number (ABN) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    business_address: str = Field(
        default="",
        description=(
            'Street address of the business .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    business_address_post_code: str = Field(
        default="", description="Post code for the business address"
    )

    postal_address: str = Field(
        default="",
        description=(
            "Mailing or postal address if different from business address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    postal_address_post_code: str = Field(
        default="", description="Post code for the postal address"
    )

    business_telephone_no: str = Field(
        default="",
        description=(
            "Primary business landline telephone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mobile_no: str = Field(
        default="",
        description=(
            'Mobile or cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        default="",
        description=(
            "Preferred email address for correspondence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    fax_no: str = Field(
        default="",
        description=(
            'Business fax number, if applicable .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    nsw_builder_licence_yes: BooleanLike = Field(
        default="", description="Select if you hold a NSW Builder Licence"
    )

    nsw_builder_licence_no: BooleanLike = Field(
        default="", description="Select if you do not hold a NSW Builder Licence"
    )

    licence_no: str = Field(
        default="",
        description=(
            "NSW Builder Licence number, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class QualificationsExperience(BaseModel):
    """Applicant’s qualifications, experience and professional memberships"""

    formal_qualifications_field_of_expertise: str = Field(
        ...,
        description=(
            "List your formal qualifications and primary field(s) of expertise .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    years_experience_building_construction: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Total number of years of experience in the building or construction industry",
    )

    total_years_practising_building_consultant: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of years you have practised as a building consultant"
    )

    member_of_association_yes: BooleanLike = Field(
        default="", description="Select if you are currently a member of a professional association"
    )

    member_of_association_no: BooleanLike = Field(
        default="", description="Select if you are not a member of any professional association"
    )

    association: str = Field(
        default="",
        description=(
            "Name of the professional association you belong to .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    category_of_membership: str = Field(
        default="",
        description=(
            "Type or category of membership held in the association .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    years_as_a_member: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years you have been a member of the association"
    )


class LegalActionHistory(BaseModel):
    """Disclosure of any legal action related to professional services"""

    legal_action_taken_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if legal action has been taken against you in relation to your advice, "
            "reports, or services"
        ),
    )

    legal_action_taken_no: BooleanLike = Field(
        default="",
        description=(
            "Select if no legal action has been taken against you in relation to your "
            "advice, reports, or services"
        ),
    )

    legal_action_details: str = Field(
        default="",
        description=(
            "Provide details of any legal action taken against you, including nature of the "
            'action and outcomes .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class AustralianBuildingConsultantsMembershipApplicationIndividual(BaseModel):
    """
        The Australian Society of Building Consultants
    APPLICATION FOR MEMBERSHIP
    APPLICATION FOR MEMBERSHIP - INDIVIDUAL

        ''
    """

    application_details: ApplicationDetails = Field(..., description="Application Details")
    qualifications__experience: QualificationsExperience = Field(
        ..., description="Qualifications & Experience"
    )
    legal_action_history: LegalActionHistory = Field(..., description="Legal Action History")
