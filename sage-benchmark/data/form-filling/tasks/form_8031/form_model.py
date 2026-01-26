from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ReportHeader(BaseModel):
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
            "Names of the person or people completing the assessment .If you cannot fill "
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

    included_in_written_policy_yes: BooleanLike = Field(
        default="",
        description="Indicate YES if this item is included in the written wellness policy",
    )

    included_in_written_policy_no: BooleanLike = Field(
        default="",
        description="Indicate NO if this item is not included in the written wellness policy",
    )

    implemented_in_school_buildings_fully_in_place: BooleanLike = Field(
        default="", description="Check if the item is fully implemented in the school building(s)"
    )

    implemented_in_school_buildings_partially_in_place: BooleanLike = Field(
        default="",
        description="Check if the item is partially implemented in the school building(s)",
    )

    implemented_in_school_buildings_not_in_place: BooleanLike = Field(
        default="", description="Check if the item is not implemented in the school building(s)"
    )


class PublicInvolvementNotificationandAssessment(BaseModel):
    """Stakeholder involvement, public notification, record retention, and related notes"""

    names_titles: str = Field(
        default="",
        description=(
            "Names and titles of LEA official(s) or designee(s) in charge of wellness "
            'policy compliance .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    website_address_or_access_description_triennial_results: str = Field(
        default="",
        description=(
            "Website URL and/or description of how the public can access the triennial "
            'assessment results .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    website_address_for_policy_or_access_description: str = Field(
        default="",
        description=(
            "Website URL and/or description of how the public can access the written "
            'wellness policy .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    retain_written_school_wellness_policy: BooleanLike = Field(
        default="",
        description="Check if records of the written school wellness policy are retained as required",
    )

    retain_documentation_publicly_available: BooleanLike = Field(
        default="",
        description=(
            "Check if documentation of making the wellness policy publicly available is retained"
        ),
    )

    retain_documentation_outreach_efforts: BooleanLike = Field(
        default="",
        description=(
            "Check if documentation of outreach efforts to invite stakeholders to the "
            "wellness committee/policy process is retained"
        ),
    )

    retain_copy_triennial_assessment: BooleanLike = Field(
        default="",
        description=(
            "Check if a copy of the triennial assessment and documentation of reporting "
            "results to the public is retained"
        ),
    )

    stakeholder_administrators: BooleanLike = Field(
        default="", description="Check if administrators are included on the wellness committee"
    )

    stakeholder_food_service_staff: BooleanLike = Field(
        default="", description="Check if food service staff are included on the wellness committee"
    )

    stakeholder_school_health_professionals: BooleanLike = Field(
        default="",
        description="Check if school health professionals are included on the wellness committee",
    )

    stakeholder_parents: BooleanLike = Field(
        default="", description="Check if parents are included on the wellness committee"
    )

    stakeholder_school_board_members: BooleanLike = Field(
        default="",
        description="Check if school board members are included on the wellness committee",
    )

    stakeholder_pe_teachers: BooleanLike = Field(
        default="",
        description=(
            "Check if physical education (PE) teachers are included on the wellness committee"
        ),
    )

    stakeholder_students: BooleanLike = Field(
        default="", description="Check if students are included on the wellness committee"
    )

    stakeholder_public: BooleanLike = Field(
        default="",
        description="Check if members of the general public are included on the wellness committee",
    )

    other_stakeholders_describe: str = Field(
        default="",
        description=(
            "Describe any additional stakeholder groups included on the wellness committee "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    notes_on_public_involvement_notification_and_assessment: str = Field(
        default="",
        description=(
            "Additional notes or comments on public involvement, notification, and "
            'assessment practices .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class WellnessPolicyAssessmentToolAndReportTemplate(BaseModel):
    """
    Wellness Policy Assessment Tool and Report Template

    ''
    """

    report_header: ReportHeader = Field(..., description="Report Header")
    policy_inclusion_and_implementation_status: PolicyInclusionandImplementationStatus = Field(
        ..., description="Policy Inclusion and Implementation Status"
    )
    public_involvement_notification_and_assessment: PublicInvolvementNotificationandAssessment = (
        Field(..., description="Public Involvement, Notification, and Assessment")
    )
