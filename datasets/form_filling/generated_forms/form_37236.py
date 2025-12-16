from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class StudentInformation(BaseModel):
    """Basic information about the student and their academic status"""

    student_first_last_name: str = Field(
        ...,
        description=(
            'Your full legal first and last name .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    spire_id: str = Field(
        ...,
        description=(
            'Your UMass SPIRE student ID number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    primary_academic_major: str = Field(
        ...,
        description=(
            "Your primary academic major as listed in university records .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    number_of_credits_currently_registered_for: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of academic credits you are currently registered for"
    )

    expected_graduation: str = Field(
        ...,
        description=(
            "Your expected graduation term and year (e.g., Spring 2026) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ContactInformation(BaseModel):
    """Student contact and address details"""

    local_address: str = Field(
        ...,
        description=(
            "Your current local mailing address while attending UMass .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    permanent_address: str = Field(
        ...,
        description=(
            'Your permanent home mailing address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    cell_home_phone: str = Field(
        ...,
        description=(
            "Your primary cell or home phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    umass_amherst_email: str = Field(
        ...,
        description=(
            "Your official UMass Amherst email address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class RequestDetails(BaseModel):
    """Details about the meal plan scholarship request"""

    date_of_request: str = Field(
        ..., description="Date you are submitting this request"
    )  # YYYY-MM-DD format

    number_meals_requested: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of meal swipes you are requesting"
    )

    nature_of_emergency_and_amount_of_support_requested_in_meal_swipes: str = Field(
        ...,
        description=(
            "Briefly explain the nature of your emergency and how many meal swipes you are "
            'requesting .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    how_this_meal_plan_scholarship_would_assist_in_mitigating_hardship: str = Field(
        ...,
        description=(
            "Describe how receiving this Meal Plan Scholarship would help address your "
            'current hardship .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    efforts_made_to_procure_support_from_other_sources: str = Field(
        ...,
        description=(
            "Explain what steps you have taken to seek support from other resources or "
            'programs .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class UndergraduateStudentMealPlanScholarshipApplication(BaseModel):
    """
    Undergraduate Student Meal Plan Scholarship Application

    The information requested below will help determine your eligibility for this grant.
    """

    student_information: StudentInformation = Field(..., description="Student Information")
    contact_information: ContactInformation = Field(..., description="Contact Information")
    request_details: RequestDetails = Field(..., description="Request Details")
