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
    """Basic club details and readiness for return to pool training"""

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
            "Name of the primary coach or contact coach for the club .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            "Email address for the primary club or coach contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this application is completed")  # YYYY-MM-DD format

    proposed_start_date: str = Field(
        ..., description="Planned start date for return to pool training"
    )  # YYYY-MM-DD format

    proposed_pools: str = Field(
        ...,
        description=(
            "Name and/or location of the pool or pools to be used .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    covid_19_declarations_received: BooleanLike = Field(
        ..., description="Indicate whether all required COVID-19 declarations have been collected"
    )

    swimmers_coaches_registered_swim_ns: BooleanLike = Field(
        ..., description="Confirm that every swimmer and coach is fully registered with Swim NS"
    )

    kinduct_account_info_submitted: BooleanLike = Field(
        ...,
        description=(
            "Confirm submission of all information needed to activate the club's Kinduct account"
        ),
    )

    familiar_with_kinduct_platform: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether club staff are familiar with using the Kinduct health "
            "monitoring platform"
        ),
    )

    club_plan_reviewed_with_facility_director: BooleanLike = Field(
        ...,
        description=(
            "Confirm that the Club Plan Form has been reviewed with the Facility Aquatic "
            "Director or designate"
        ),
    )

    facility_reopening_plan_reviewed: BooleanLike = Field(
        ..., description="Confirm that you have reviewed the facility's re-opening plan"
    )

    additional_planning_notes: str = Field(
        default="",
        description=(
            "Any extra notes or details related to your return to pool training plan .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Communication(BaseModel):
    """How the return to swimming plan and safety precautions will be communicated"""

    communication_plan_to_club: str = Field(
        ...,
        description=(
            "Explain the methods and channels you will use to share the Return to Swimming "
            "Plan with club members and stakeholders .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    communication_safety_precautions_to_swimmers_parents: str = Field(
        ...,
        description=(
            "Describe how you will inform swimmers and parents about all required safety "
            'precautions .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class ClubApplicationReturnToPoolTrainingPhase3(BaseModel):
    """
        CLUB APPLICATION - RETURN TO POOL TRAINING
    PHASE 3

        ''
    """

    general_information: GeneralInformation = Field(..., description="General Information")
    communication: Communication = Field(..., description="Communication")
