from pydantic import BaseModel, ConfigDict, Field


class ParentGuardianRefusalStatewideAssessments(BaseModel):
    """Parent/Guardian Refusal for Student Participation in Statewide Assessments

    A parent or guardian submits this form to the student’s school to formally refuse the student’s participation in Minnesota’s state-required statewide standardized assessments for a specific school year and to indicate which assessments are being refused. School or district staff (such as testing coordinators and student records personnel) review the submission to document the opt-out decision, update testing participation plans, and retain the form in the student’s educational records for the applicable school year.
    """

    model_config = ConfigDict(extra="forbid")

    date: str = Field(
        ...,
        description='Date (YYYY-MM-DD).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    student_legal_middle_initial: str = Field(
        ...,
        description='Student legal middle initial.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    student_date_of_birth: str = Field(
        ...,
        description='Student date of birth (YYYY-MM-DD).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    student_district_school: str = Field(
        ...,
        description='Student district/school.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    reason_for_refusal: str = Field(
        ...,
        description='Reason for refusal.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )



    staff_only_student_id_or_marss_number: str = Field(
        ...,
        description='Student ID or MARSS number (staff).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )