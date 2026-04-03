from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class HeaderInformation(BaseModel):
    """Basic information about the LEA/district, school, reviewers, and grades covered"""

    lea_district_name: str = Field(
        ...,
        description=(
            'Name of the LEA or school district .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reporting_timeframe_month_year_to_month_year: str = Field(
        ...,
        description=(
            "Reporting period for this assessment, from month/year to month/year .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    names_of_reviewers: str = Field(
        ...,
        description=(
            "Name or names of the individuals completing the assessment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    school_name_if_applicable: str = Field(
        default="",
        description=(
            "School name if this assessment is for a specific school .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    grade_pk: BooleanLike = Field(
        default="", description="Check if pre-kindergarten (PK) grade level is included"
    )

    grade_k: BooleanLike = Field(
        default="", description="Check if kindergarten (K) grade level is included"
    )

    grade_1: BooleanLike = Field(default="", description="Check if 1st grade is included")

    grade_2: BooleanLike = Field(default="", description="Check if 2nd grade is included")

    grade_3: BooleanLike = Field(default="", description="Check if 3rd grade is included")

    grade_4: BooleanLike = Field(default="", description="Check if 4th grade is included")

    grade_5: BooleanLike = Field(default="", description="Check if 5th grade is included")

    grade_6: BooleanLike = Field(default="", description="Check if 6th grade is included")

    grade_7: BooleanLike = Field(default="", description="Check if 7th grade is included")

    grade_8: BooleanLike = Field(default="", description="Check if 8th grade is included")

    grade_9: BooleanLike = Field(default="", description="Check if 9th grade is included")

    grade_10: BooleanLike = Field(default="", description="Check if 10th grade is included")

    grade_11: BooleanLike = Field(default="", description="Check if 11th grade is included")

    grade_12: BooleanLike = Field(default="", description="Check if 12th grade is included")


class PolicyInclusionandImplementationStatus(BaseModel):
    """Status of inclusion in written policy and implementation in school buildings"""

    included_in_the_written_policy_yes: BooleanLike = Field(
        default="",
        description="Indicate YES if the item is included in the written wellness policy",
    )

    included_in_the_written_policy_no: BooleanLike = Field(
        default="",
        description="Indicate NO if the item is not included in the written wellness policy",
    )

    implemented_in_the_school_buildings_fully_in_place: BooleanLike = Field(
        default="", description="Check if the item is fully implemented in the school building(s)"
    )

    implemented_in_the_school_buildings_partially_in_place: BooleanLike = Field(
        default="",
        description="Check if the item is partially implemented in the school building(s)",
    )

    implemented_in_the_school_buildings_not_in_place: BooleanLike = Field(
        default="", description="Check if the item is not implemented in the school building(s)"
    )


class PublicInvolvementNotificationandAssessment(BaseModel):
    """Details on wellness policy oversight, public access, records, stakeholders, and notes"""

    names_titles: str = Field(
        default="",
        description=(
            "Names and titles of LEA official(s) or designee(s) in charge of wellness "
            'policy compliance .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    website_address_and_or_description_of_how_to_access_copy: str = Field(
        default="",
        description=(
            "Website URL and/or description of how the public can access the triennial "
            'assessment results .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    website_address_for_policy_and_or_description_of_how_to_access_copy: str = Field(
        default="",
        description=(
            "Website URL and/or description of how the public can access the written "
            'wellness policy .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    the_written_school_wellness_policy: BooleanLike = Field(
        default="",
        description="Check to confirm records of the written school wellness policy are retained",
    )

    documentation_of_making_the_wellness_policy_publicly_available: BooleanLike = Field(
        default="",
        description=(
            "Check to confirm documentation is retained showing the wellness policy was "
            "made publicly available"
        ),
    )

    documentation_of_outreach_efforts_inviting_stakeholders_to_participate_in_the_wellness_committee_wellness_policy_process: BooleanLike = Field(
        default="",
        description="Check to confirm documentation of outreach efforts to stakeholders is retained",
    )

    copy_of_triennial_assessment_and_documentation_of_reporting_results_to_public: BooleanLike = (
        Field(
            default="",
            description=(
                "Check to confirm a copy of the triennial assessment and documentation of "
                "reporting results to the public is retained"
            ),
        )
    )

    administrators: BooleanLike = Field(
        default="",
        description="Check if administrators are included as stakeholders on the wellness committee",
    )

    food_service_staff: BooleanLike = Field(
        default="",
        description=(
            "Check if food service staff are included as stakeholders on the wellness committee"
        ),
    )

    school_health_professionals: BooleanLike = Field(
        default="",
        description=(
            "Check if school health professionals are included as stakeholders on the "
            "wellness committee"
        ),
    )

    parents: BooleanLike = Field(
        default="",
        description="Check if parents are included as stakeholders on the wellness committee",
    )

    school_board_members: BooleanLike = Field(
        default="",
        description=(
            "Check if school board members are included as stakeholders on the wellness committee"
        ),
    )

    pe_teachers: BooleanLike = Field(
        default="",
        description=(
            "Check if physical education (PE) teachers are included as stakeholders on the "
            "wellness committee"
        ),
    )

    students: BooleanLike = Field(
        default="",
        description="Check if students are included as stakeholders on the wellness committee",
    )

    public: BooleanLike = Field(
        default="",
        description=(
            "Check if members of the general public are included as stakeholders on the "
            "wellness committee"
        ),
    )

    other_stakeholders_describe: str = Field(
        default="",
        description=(
            "Describe any additional stakeholder groups involved in the wellness committee "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    notes_on_public_involvement_notification_and_assessment: str = Field(
        default="",
        description=(
            "Additional notes or comments on public involvement, notification, and "
            'assessment .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class WellnessPolicyAssessmentToolAndReportTemplate(BaseModel):
    """
    Wellness Policy Assessment Tool and Report Template

    ''
    """

    header_information: HeaderInformation = Field(..., description="Header Information")
    policy_inclusion_and_implementation_status: PolicyInclusionandImplementationStatus = Field(
        ..., description="Policy Inclusion and Implementation Status"
    )
    public_involvement_notification_and_assessment: PublicInvolvementNotificationandAssessment = (
        Field(..., description="Public Involvement, Notification, and Assessment")
    )
