from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SectionIForCompletionbytheEmployer(BaseModel):
    """Employer information"""

    employer_name_and_contact: str = Field(
        ...,
        description=(
            "Employer’s name and contact information .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class SectionIIForCompletionbyEmployee(BaseModel):
    """Employee and family member information and care details"""

    your_name_first: str = Field(
        ...,
        description=(
            'Employee’s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    your_name_middle: str = Field(
        default="",
        description=(
            'Employee’s middle name or initial .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    your_name_last: str = Field(
        ...,
        description=(
            'Employee’s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    name_of_family_member_for_whom_you_will_provide_care_first: str = Field(
        ...,
        description=(
            'Family member’s first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    name_of_family_member_for_whom_you_will_provide_care_middle: str = Field(
        default="",
        description=(
            "Family member’s middle name or initial .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_family_member_for_whom_you_will_provide_care_last: str = Field(
        ...,
        description=(
            'Family member’s last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    relationship_of_family_member_to_you: str = Field(
        ...,
        description=(
            "Describe how the family member is related to you (e.g., spouse, parent, child) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    if_family_member_is_your_son_or_daughter_date_of_birth: str = Field(
        default="", description="Date of birth if the family member is your son or daughter"
    )  # YYYY-MM-DD format

    describe_care_you_will_provide_to_your_family_member_and_estimate_leave_needed_to_provide_care: str = Field(
        ...,
        description=(
            "Describe the type of care you will provide and estimate how much leave you "
            'will need .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    employee_signature: str = Field(
        ...,
        description=(
            "Employee’s signature certifying the information provided .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employee_signature_date: str = Field(
        ..., description="Date the employee signed the form"
    )  # YYYY-MM-DD format


class SectionIIIForCompletionbytheHealthCareProvider(BaseModel):
    """Health care provider and medical certification details"""

    providers_name_and_business_address: str = Field(
        ...,
        description=(
            "Health care provider’s full name and business address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    type_of_practice_medical_specialty: str = Field(
        ...,
        description=(
            "Provider’s type of practice or medical specialty .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            'Provider’s telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            'Provider’s fax number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    approximate_date_patients_condition_commenced: str = Field(
        ..., description="Approximate date when the patient’s condition began"
    )  # YYYY-MM-DD format

    probable_duration_of_patients_condition: str = Field(
        ...,
        description=(
            "Estimated length of time the patient’s condition will last .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    was_patient_admitted_for_an_overnight_stay_no: BooleanLike = Field(
        ..., description="Indicate that the patient was not admitted for an overnight stay"
    )

    was_patient_admitted_for_an_overnight_stay_yes: BooleanLike = Field(
        ..., description="Indicate that the patient was admitted for an overnight stay"
    )

    if_so_dates_of_admission: str = Field(
        default="",
        description=(
            "List the dates of any overnight admissions .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dates_you_treated_the_patient_for_the_condition: str = Field(
        ...,
        description=(
            "All dates on which you treated the patient for this condition .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    description_of_appropriate_medical_facts: str = Field(
        ...,
        description=(
            "Describe medical facts supporting the need for leave, including symptoms, "
            'diagnosis, treatment, and referrals .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    explain_the_care_needed_by_the_patient: str = Field(
        ...,
        description=(
            "Explain the type of care needed, why it is medically necessary, and whether it "
            'is continuous or intermittent .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    signature_of_health_care_provider: str = Field(
        ...,
        description=(
            'Health care provider’s signature .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_health_care_provider_date: str = Field(
        ..., description="Date the health care provider signed the form"
    )  # YYYY-MM-DD format


class CertificationOfHealthCareProviderForFamilyMemberFMLA(BaseModel):
    """
    Certification of Health Care Provider for Family Member’s Serious Health Condition(FMLA)

    Please complete Section II before giving this form to your family member or his/her medical provider. The FMLA permits an employer to require that you submit a timely, complete, and sufficient medical certification to support a request for FMLA leave to care for a covered family with a serious health condition. If requested by your employer, your response is required to obtain or retain the benefit of FMLA protections 29 U.S.C. 2613, 2614 c 3. **Failure to provide a complete and sufficient medical certification may result in denial of your FMLA request.** 29 C.F.R. 825.313. Your employer must give you at least 15 calendar days to return this form to your employer. 29C.F.R. 825.305.
    """

    section_i_for_completion_by_the_employer: SectionIForCompletionbytheEmployer = Field(
        ..., description="Section I: For Completion by the Employer"
    )
    section_ii_for_completion_by_employee: SectionIIForCompletionbyEmployee = Field(
        ..., description="Section II: For Completion by Employee"
    )
    section_iii_for_completion_by_the_health_care_provider: SectionIIIForCompletionbytheHealthCareProvider = Field(
        ..., description="Section III: For Completion by the Health Care Provider"
    )
