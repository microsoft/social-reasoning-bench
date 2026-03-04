from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class GeneralInformation(BaseModel):
    """Basic club details and readiness checks for return to pool training"""

    club_name: str = Field(
        ...,
        description=(
            "Official name of the club submitting this application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    coach_name: str = Field(
        ...,
        description=(
            'Primary coach\'s full name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            "Contact email address for the club or coach .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this application is completed")  # YYYY-MM-DD format

    proposed_start_date: str = Field(
        ..., description="Planned start date for return to pool training"
    )  # YYYY-MM-DD format

    proposed_pools: str = Field(
        ...,
        description=(
            "Name and location of the pool or pools to be used .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    covid_19_declarations_received_yes: BooleanLike = Field(
        ..., description="Indicate YES if all required COVID-19 declarations have been received"
    )

    covid_19_declarations_received_no: BooleanLike = Field(
        ..., description="Indicate NO if all required COVID-19 declarations have not been received"
    )

    swimmers_coaches_registered_swim_ns_yes: BooleanLike = Field(
        ...,
        description="Indicate YES if all swimmers and coaches are fully registered with Swim NS",
    )

    swimmers_coaches_registered_swim_ns_no: BooleanLike = Field(
        ...,
        description="Indicate NO if all swimmers and coaches are not fully registered with Swim NS",
    )

    kinduct_info_submitted_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate YES if all information to activate the Kinduct account has been submitted"
        ),
    )

    kinduct_info_submitted_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate NO if all information to activate the Kinduct account has not been submitted"
        ),
    )

    familiar_with_kinduct_platform_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate YES if you are familiar with using the Kinduct online health "
            "monitoring platform"
        ),
    )

    familiar_with_kinduct_platform_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate NO if you are not familiar with using the Kinduct online health "
            "monitoring platform"
        ),
    )

    club_plan_reviewed_with_facility_director_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate YES if the Club Plan Form has been reviewed with the Facility Aquatic "
            "Director or designate"
        ),
    )

    club_plan_reviewed_with_facility_director_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate NO if the Club Plan Form has not been reviewed with the Facility "
            "Aquatic Director or designate"
        ),
    )

    facility_reopening_plan_reviewed_yes: BooleanLike = Field(
        ..., description="Indicate YES if the facility re-opening plan has been reviewed"
    )

    facility_reopening_plan_reviewed_no: BooleanLike = Field(
        ..., description="Indicate NO if the facility re-opening plan has not been reviewed"
    )

    additional_planning_notes: str = Field(
        default="",
        description=(
            "Any additional notes or details related to planning the return to pool "
            'training .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Communication(BaseModel):
    """How the return to swimming plan and safety precautions will be communicated"""

    communication_plan_to_club: str = Field(
        ...,
        description=(
            "Explain the methods and channels you will use to communicate the Return to "
            'Swimming Plan to club members .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    communication_of_safety_precautions: str = Field(
        ...,
        description=(
            "Describe how swimmers and parents will be informed about all required safety "
            'precautions .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class ClubApplicationReturnToPoolTrainingPhase3(BaseModel):
    """CLUB APPLICATION - RETURN TO POOL TRAINING

    PHASE 3"""

    general_information: GeneralInformation = Field(..., description="General Information")
    communication: Communication = Field(..., description="Communication")
