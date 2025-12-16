from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ClaimantandWageEarnerInformation(BaseModel):
    """Identifying information for the claimant and, if different, the wage earner"""

    claimants_name: str = Field(
        ...,
        description=(
            'Full legal name of the claimant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    claimant_social_security_number: str = Field(
        ..., description="Claimant's Social Security Number"
    )

    wage_earner_leave_blank_if_name_is_the_same_as_the_claimants: str = Field(
        default="",
        description=(
            "Name of the wage earner, if different from the claimant .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    wage_earner_social_security_number: str = Field(
        default="", description="Wage earner's Social Security Number"
    )


class WorkandConditionChangesSinceReconsiderationDate(BaseModel):
    """Information about work activity, medical condition, and daily activities since the reconsideration date"""

    have_you_worked_since_the_date_your_request_for_reconsideration_was_filed: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have done any work since the date your request for "
            "reconsideration was filed"
        ),
    )

    worked_since_reconsideration_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if you have worked since the date your request for reconsideration was filed"
        ),
    )

    worked_since_reconsideration_no: BooleanLike = Field(
        default="",
        description=(
            "Check if you have not worked since the date your request for reconsideration was filed"
        ),
    )

    describe_the_nature_and_extent_of_work: str = Field(
        default="",
        description=(
            "If you have worked, describe what kind of work you did and how much you worked "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    has_there_been_any_change_in_your_condition_since_the_above_date: BooleanLike = Field(
        ...,
        description="Indicate whether your medical condition has changed since the date shown above",
    )

    condition_changed_yes: BooleanLike = Field(
        default="", description="Check if your condition has changed since the above date"
    )

    condition_changed_no: BooleanLike = Field(
        default="", description="Check if your condition has not changed since the above date"
    )

    describe_the_change_in_your_condition: str = Field(
        default="",
        description=(
            "If your condition has changed, describe how it has changed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    have_your_daily_activities_and_or_social_functioning_changed_since_the_above_date: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether your daily activities or social functioning have changed "
            "since the above date"
        ),
    )

    daily_activities_changed_yes: BooleanLike = Field(
        default="",
        description="Check if your daily activities and/or social functioning have changed",
    )

    daily_activities_changed_no: BooleanLike = Field(
        default="",
        description="Check if your daily activities and/or social functioning have not changed",
    )

    describe_the_changes_in_daily_activities_and_or_social_functioning: str = Field(
        default="",
        description=(
            "If there have been changes, describe how your daily activities and/or social "
            'functioning have changed .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class RecentMedicalTreatment(BaseModel):
    """Details about treatment or examinations by a physician since the above date"""

    have_you_been_treated_or_examined_by_a_physician_other_than_as_a_patient_in_a_hospital_since_the_above_date: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have seen or been treated by a physician since the above date"
        ),
    )

    treated_by_physician_since_above_date_yes: BooleanLike = Field(
        default="",
        description="Check if you have been treated or examined by a physician since the above date",
    )

    treated_by_physician_since_above_date_no: BooleanLike = Field(
        default="",
        description=(
            "Check if you have not been treated or examined by a physician since the above date"
        ),
    )

    name_of_physician: str = Field(
        default="",
        description=(
            "Full name of the physician who treated or examined you .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_include_zip_code: str = Field(
        default="",
        description=(
            "Mailing address of the physician, including ZIP code .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    area_code_and_telephone_number: str = Field(
        default="",
        description=(
            "Telephone number of the physician, including area code .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_often_do_you_see_this_physician: str = Field(
        default="",
        description=(
            "Frequency of visits to this physician (for example, weekly, monthly) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    dates_you_saw_this_physician: str = Field(
        default="",
        description=(
            'List the dates you saw this physician .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_visit: str = Field(
        default="",
        description=(
            "Explain why you visited this physician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    type_of_treatment_received_include_drugs_surgery_tests: str = Field(
        default="",
        description=(
            "Describe the treatment you received, including medications, surgery, and tests "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class ClaimantHearingRequestDisabilityIssueStatement(BaseModel):
    """
        CLAIMANT'S STATEMENT WHEN REQUEST FOR HEARING IS FILED
    AND THE ISSUE IS DISABILITY

        Print, type or write clearly and answer all questions to the best of your ability. Complete answers will aid in processing the claim. IF ADDITIONAL SPACE IS NEEDED, ATTACH A SEPARATE STATEMENT TO THIS FORM.
    """

    claimant_and_wage_earner_information: ClaimantandWageEarnerInformation = Field(
        ..., description="Claimant and Wage Earner Information"
    )
    work_and_condition_changes_since_reconsideration_date: WorkandConditionChangesSinceReconsiderationDate = Field(
        ..., description="Work and Condition Changes Since Reconsideration Date"
    )
    recent_medical_treatment: RecentMedicalTreatment = Field(
        ..., description="Recent Medical Treatment"
    )
