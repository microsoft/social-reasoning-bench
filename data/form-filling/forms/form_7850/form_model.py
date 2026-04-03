from typing import Literal, Optional, List, Union
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
            "Official name of the swim club submitting this application .If you cannot fill "
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
            "Email address for the primary club contact .If you cannot fill this, write "
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
            "Name and/or location of the pool or pools to be used .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    have_all_covid_19_declarations_been_received_yes_no: BooleanLike = Field(
        ..., description="Indicate whether all required COVID-19 declarations have been collected"
    )

    are_all_swimmers_and_coaches_fully_registered_with_swim_ns_yes_no: BooleanLike = Field(
        ..., description="Confirm that every swimmer and coach is fully registered with Swim NS"
    )

    have_you_submitted_all_information_required_to_activate_your_kinduct_account_yes_no: BooleanLike = Field(
        ...,
        description=(
            "Confirm that all information needed to activate the club's Kinduct account has "
            "been submitted"
        ),
    )

    are_you_familiar_with_the_use_of_the_kinduct_online_health_monitoring_platform_yes_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether club staff are familiar with using the Kinduct online health "
            "monitoring platform"
        ),
    )

    have_you_reviewed_your_club_plan_form_with_your_facility_aquatic_director_or_designate_yes_no: BooleanLike = Field(
        ...,
        description=(
            "Confirm that the Club Plan Form has been reviewed with the Facility Aquatic "
            "Director or their designate"
        ),
    )

    have_you_reviewed_facility_re_opening_plan_yes_no: BooleanLike = Field(
        ..., description="Confirm that you have reviewed the facility's re-opening plan"
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

    describe_how_the_return_to_swimming_plan_will_be_communicated_to_your_club: str = Field(
        ...,
        description=(
            "Explain the methods and channels you will use to communicate the Return to "
            'Swimming Plan to club members .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    describe_how_swimmers_parents_will_be_informed_of_all_safety_precautions_they_must_follow_that_are_implemented_by_your_club: str = Field(
        ...,
        description=(
            "Describe how you will inform swimmers and parents about all club-implemented "
            'safety precautions they must follow .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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
