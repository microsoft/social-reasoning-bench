from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ServiceMemberVeteranInformation(BaseModel):
    """Personal, contact, and military service details for the service member or veteran"""

    name: str = Field(
        ...,
        description=(
            "Service member or veteran's full legal name .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(
        ..., description="Date of birth of the service member or veteran"
    )  # YYYY-MM-DD format

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    gender: str = Field(
        default="",
        description=(
            "Gender of the service member or veteran .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street address of the service member or veteran .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            'Email address for contact .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    town: str = Field(
        ...,
        description=(
            'Town or city of residence .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of residence")

    zip: str = Field(..., description="ZIP or postal code")

    county: str = Field(
        default="",
        description=(
            'County of residence .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    mil_branch_army: BooleanLike = Field(
        default="", description="Check if the military branch is Army"
    )

    mil_branch_navy: BooleanLike = Field(
        default="", description="Check if the military branch is Navy"
    )

    mil_branch_air_force: BooleanLike = Field(
        default="", description="Check if the military branch is Air Force"
    )

    mil_branch_marines: BooleanLike = Field(
        default="", description="Check if the military branch is Marines"
    )

    mil_branch_coast_guard: BooleanLike = Field(
        default="", description="Check if the military branch is Coast Guard"
    )

    component_guard: BooleanLike = Field(
        default="", description="Check if component is National Guard"
    )

    component_reserves: BooleanLike = Field(
        default="", description="Check if component is Reserves"
    )

    component_active_duty: BooleanLike = Field(
        default="", description="Check if component is Active Duty"
    )

    active_duty_time_other_than_training_yes: BooleanLike = Field(
        default="", description="Indicate Yes if there was active duty time other than training"
    )

    active_duty_time_other_than_training_no: BooleanLike = Field(
        default="", description="Indicate No if there was no active duty time other than training"
    )

    active_duty_time_other_than_training_unknown: BooleanLike = Field(
        default="",
        description="Indicate Unknown if unsure about active duty time other than training",
    )

    are_you_currently_serving: BooleanLike = Field(
        default="", description="Check if currently serving in the military"
    )

    are_you_retired: BooleanLike = Field(
        default="", description="Check if retired from the military"
    )

    are_you_completed_enlistment: BooleanLike = Field(
        default="", description="Check if completed enlistment"
    )

    are_you_medical_separation: BooleanLike = Field(
        default="", description="Check if separated for medical reasons"
    )

    are_you_other_separation_discharge: BooleanLike = Field(
        default="", description="Check if separated/discharged for other reasons"
    )

    are_you_unknown: BooleanLike = Field(
        default="", description="Check if current service status is unknown"
    )

    when_separated_separated_pre_9_11: BooleanLike = Field(
        default="", description="Check if separation occurred before 9/11"
    )

    when_separated_separated_post_9_11: BooleanLike = Field(
        default="", description="Check if separation occurred after 9/11"
    )

    when_separated_not_applicable_still_serving: BooleanLike = Field(
        default="", description="Check if still serving and separation date is not applicable"
    )

    discharge_status_honorable: BooleanLike = Field(
        default="", description="Check if discharge status is Honorable"
    )

    discharge_status_general_under_honorable_conditions: BooleanLike = Field(
        default="", description="Check if discharge status is General Under Honorable Conditions"
    )

    discharge_status_other_than_honorable: BooleanLike = Field(
        default="", description="Check if discharge status is Other Than Honorable"
    )

    discharge_status_bad_conduct: BooleanLike = Field(
        default="", description="Check if discharge status is Bad Conduct"
    )

    discharge_status_dishonorable: BooleanLike = Field(
        default="", description="Check if discharge status is Dishonorable"
    )

    proof_of_veteran_status_dd214: BooleanLike = Field(
        default="", description="Check if DD214 is provided as proof of veteran status"
    )

    proof_of_veteran_status_va_id_card: BooleanLike = Field(
        default="", description="Check if VA ID Card is provided as proof of veteran status"
    )

    proof_of_veteran_status_va_award_letter: BooleanLike = Field(
        default="", description="Check if VA Award Letter is provided as proof of veteran status"
    )

    proof_of_veteran_status_other: str = Field(
        default="",
        description=(
            "Specify other form of proof of veteran status .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dates_of_service: str = Field(
        default="",
        description=(
            "List the start and end dates of military service .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    service_era_didnt_serve_during_wartime: BooleanLike = Field(
        default="", description="Check if service did not occur during a wartime era"
    )

    service_era_oef_oif_ond: BooleanLike = Field(
        default="", description="Check if service was during OEF/OIF/OND"
    )

    service_era_persian_gulf: BooleanLike = Field(
        default="", description="Check if service was during the Persian Gulf era"
    )

    service_era_vietnam: BooleanLike = Field(
        default="", description="Check if service was during the Vietnam War era"
    )

    service_era_korean_war: BooleanLike = Field(
        default="", description="Check if service was during the Korean War era"
    )

    service_era_other_wartime_era: BooleanLike = Field(
        default="", description="Check if service was during another wartime era"
    )


class AdditionalInformation(BaseModel):
    """Household, employment, housing, insurance, and related background information"""

    is_veteran_working_with_another_agency_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the veteran is working with another agency"
    )

    is_veteran_working_with_another_agency_no: BooleanLike = Field(
        default="", description="Indicate No if the veteran is not working with another agency"
    )

    if_so_who: str = Field(
        default="",
        description=(
            "Name of the other agency the veteran is working with .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    people_in_household: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of people living in the household"
    )

    household_gross_income: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Total gross monthly or annual household income (specify as required by program)",
    )

    minor_children_yes: BooleanLike = Field(
        default="", description="Indicate Yes if there are minor children"
    )

    minor_children_no: BooleanLike = Field(
        default="", description="Indicate No if there are no minor children"
    )

    do_minors_reside_with_sm_v_yes: BooleanLike = Field(
        default="",
        description="Indicate Yes if minor children reside with the service member/veteran",
    )

    do_minors_reside_with_sm_v_no: BooleanLike = Field(
        default="",
        description="Indicate No if minor children do not reside with the service member/veteran",
    )

    does_sm_v_have_transportation_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the service member/veteran has transportation"
    )

    does_sm_v_have_transportation_no: BooleanLike = Field(
        default="",
        description="Indicate No if the service member/veteran does not have transportation",
    )

    does_sm_v_have_a_job_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the service member/veteran is currently employed"
    )

    does_sm_v_have_a_job_no: BooleanLike = Field(
        default="",
        description="Indicate No if the service member/veteran is not currently employed",
    )

    does_sm_v_need_a_job_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the service member/veteran needs employment"
    )

    does_sm_v_need_a_job_no: BooleanLike = Field(
        default="", description="Indicate No if the service member/veteran does not need employment"
    )

    underemployed: BooleanLike = Field(
        default="", description="Check if the service member/veteran is underemployed"
    )

    housing_rent: BooleanLike = Field(default="", description="Check if housing is rented")

    housing_own: BooleanLike = Field(default="", description="Check if housing is owned")

    housing_homeless: BooleanLike = Field(
        default="", description="Check if the service member/veteran is homeless"
    )

    housing_at_risk_of_homelessness: BooleanLike = Field(
        default="", description="Check if the service member/veteran is at risk of homelessness"
    )

    housing_resides_with_family_member: BooleanLike = Field(
        default="", description="Check if residing with a family member"
    )

    does_family_have_insurance_medicaid: BooleanLike = Field(
        default="", description="Check if family has Medicaid coverage"
    )

    does_family_have_insurance_medicare: BooleanLike = Field(
        default="", description="Check if family has Medicare coverage"
    )

    does_family_have_insurance_va_healthcare: BooleanLike = Field(
        default="", description="Check if family uses VA Healthcare"
    )

    does_family_have_insurance_private_insurance: BooleanLike = Field(
        default="", description="Check if family has private health insurance"
    )

    does_family_have_insurance_tricare: BooleanLike = Field(
        default="", description="Check if family has TriCare coverage"
    )

    does_family_have_insurance_other: str = Field(
        default="",
        description=(
            "Specify other type of insurance coverage .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    is_sm_v_a_class_member_under_maine_consent_decree_yes: BooleanLike = Field(
        default="",
        description="Indicate Yes if SM/V is a class member under the Maine Consent Decree",
    )

    is_sm_v_a_class_member_under_maine_consent_decree_no: BooleanLike = Field(
        default="",
        description="Indicate No if SM/V is not a class member under the Maine Consent Decree",
    )


class ExplanationofNeed(BaseModel):
    """Narrative description of the current financial hardship"""

    describe_the_financial_hardship_that_you_are_experiencing: str = Field(
        ...,
        description=(
            "Detailed explanation of the current financial hardship and circumstances .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class LongTermPlan(BaseModel):
    """Steps being taken to prevent similar financial needs in the future"""

    what_steps_are_you_taking_to_prevent_a_similar_financial_need_in_the_future: str = Field(
        ...,
        description=(
            "Describe your long-term plan to avoid similar financial hardship in the future "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class RiskandCertification(BaseModel):
    """Self-harm risk screening and applicant certification/signature"""

    in_the_last_week_have_you_had_any_thoughts_of_harming_yourself_yes: BooleanLike = Field(
        ..., description="Indicate Yes if there have been thoughts of self-harm in the last week"
    )

    in_the_last_week_have_you_had_any_thoughts_of_harming_yourself_no: BooleanLike = Field(
        ..., description="Indicate No if there have not been thoughts of self-harm in the last week"
    )

    signature: str = Field(
        ...,
        description=(
            "Applicant's signature affirming the accuracy of the information provided .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(..., description="Date the application is signed")  # YYYY-MM-DD format


class ALDeptMaineVetEmergencyFinancialAssistanceAppV042019(BaseModel):
    """
        American Legion Department of Maine
    Veteran’s Emergency Financial Assistance Program (VEFAP) Application – Version 04/2019

        Veteran’s Emergency Financial Assistance Program (VEFAP) Application – Version 04/2019
    """

    service_member__veteran_information: ServiceMemberVeteranInformation = Field(
        ..., description="Service Member / Veteran Information"
    )
    additional_information: AdditionalInformation = Field(..., description="Additional Information")
    explanation_of_need: ExplanationofNeed = Field(..., description="Explanation of Need")
    long_term_plan: LongTermPlan = Field(..., description="Long-Term Plan")
    risk_and_certification: RiskandCertification = Field(..., description="Risk and Certification")
