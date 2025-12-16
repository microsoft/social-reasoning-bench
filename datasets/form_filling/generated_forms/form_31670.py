from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PersonalDetails(BaseModel):
    """Basic personal information about the applicant"""

    title: str = Field(
        ...,
        description=(
            "Your preferred title (e.g. Mr, Ms, Dr) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Your given first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    i_like_to_be_called: str = Field(
        default="",
        description=(
            "The name you prefer to be called, if different from your first name .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    surname: str = Field(
        ...,
        description=(
            'Your family name or last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Your date of birth")  # YYYY-MM-DD format

    nationality: str = Field(
        ...,
        description=(
            'Your nationality or citizenship .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    marital_status: str = Field(
        default="",
        description=(
            'Your current marital status .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class ContactInformation(BaseModel):
    """Current and permanent contact details for the applicant"""

    present_address: str = Field(
        ...,
        description=(
            'Your current residential address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    country_present_address: str = Field(
        ...,
        description=(
            'Country for your present address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    telephone_present_address: str = Field(
        ...,
        description=(
            "Main telephone number for your present address (include country code if "
            'outside UK) .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    mobile: str = Field(
        default="",
        description=(
            'Your mobile/cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Your primary email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    permanent_address: str = Field(
        default="",
        description=(
            "Your permanent or home address, if different from your present address .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    country_permanent_address: str = Field(
        default="",
        description=(
            'Country for your permanent address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    telephone_permanent_address: str = Field(
        default="",
        description=(
            "Telephone number for your permanent address (include country code if outside "
            'UK) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class EducationandExperience(BaseModel):
    """Applicant’s educational background and work history"""

    details_of_education_and_qualifications: str = Field(
        ...,
        description=(
            "Provide details of your education history and any qualifications obtained .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    details_of_previous_work_experience: str = Field(
        ...,
        description=(
            "Describe your previous work experience, including roles and dates where "
            'possible .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class CoursePlansandFunding(BaseModel):
    """Plans after the course and how the applicant will finance study and living costs"""

    what_do_you_plan_to_do_after_the_course: str = Field(
        ...,
        description=(
            "Explain your plans and intentions after completing the course .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    how_do_you_plan_to_finance_the_course_and_your_living_expenses: str = Field(
        ...,
        description=(
            "Describe how you intend to pay for the course fees and your living costs .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    self: BooleanLike = Field(
        default="", description="Check if you will finance the course and living expenses yourself"
    )

    parent_legal_guardian: BooleanLike = Field(
        default="",
        description="Check if a parent or legal guardian will finance the course and living expenses",
    )

    corporate_government_sponsor: BooleanLike = Field(
        default="", description="Check if a company or government body will sponsor you"
    )

    other_please_specify: str = Field(
        default="",
        description=(
            "Indicate any other source of funding and specify details .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class pythonChippendaleFurnitureDesignMakingRestorationCourse20222023(BaseModel):
    """
        APPLICATION FORM

    THE CHIPPENDALE INTERNATIONAL SCHOOL OF FURNITURE

    FURNITURE DESIGN, MAKING AND RESTORATION COURSE 2022-2023

        Please complete this form and email it to info@chippendale.co.uk, along with a digital passport style photo.
    """

    personal_details: PersonalDetails = Field(..., description="Personal Details")
    contact_information: ContactInformation = Field(..., description="Contact Information")
    education_and_experience: EducationandExperience = Field(
        ..., description="Education and Experience"
    )
    course_plans_and_funding: CoursePlansandFunding = Field(
        ..., description="Course Plans and Funding"
    )
