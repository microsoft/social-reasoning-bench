from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SupplementalandAddendumOptions(BaseModel):
    """Options related to supplemental pages and the Division of Corporations addendum"""

    if_you_have_attached_supplemental_pages_check_here: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether you have attached additional pages listing spouse/children "
            "information."
        ),
    )

    not_applicable_addendum_for_exemption_of_public_disclosure: BooleanLike = Field(
        default="",
        description="Check if the Addendum for Exemption of Public Disclosure does not apply to you.",
    )


class ExemptionCategory(BaseModel):
    """Category of eligibility for public records exemption to be selected by the requester"""

    code_enforcement_officer: BooleanLike = Field(
        default="",
        description="Check if you are a Code Enforcement Officer requesting this exemption.",
    )

    county_tax_collector: BooleanLike = Field(
        default="", description="Check if you are a County Tax Collector requesting this exemption."
    )

    dept_of_business_and_professional_regulation_investigators_and_inspectors: BooleanLike = Field(
        default="",
        description=(
            "Check if you are an investigator or inspector with the Department of Business "
            "and Professional Regulation."
        ),
    )

    dept_of_children_and_family_services_personnel_investigation_of_abuse_neglect_exploitation_fraud_theft_or_other_criminal_activities: BooleanLike = Field(
        default="",
        description=(
            "Check if you are DCF personnel whose duties involve investigation of abuse, "
            "neglect, exploitation, fraud, theft, or other criminal activities."
        ),
    )

    dept_of_health_personnel_support_investigation_child_abuse_or_neglect_determination_of_benefits_or_investigation_inspection_or_prosecution_of_health_care_practitioners: BooleanLike = Field(
        default="",
        description=(
            "Check if you are DOH personnel supporting child abuse/neglect investigations, "
            "benefit determinations, or investigations/inspections/prosecutions of health "
            "care practitioners."
        ),
    )

    dept_of_health_personnel_determination_or_adjudication_of_eligibility_for_social_security_disability_benefits_investigation_or_prosecution_of_complaints_or_licensure_of_health_care_practitioners_or_facilities: BooleanLike = Field(
        default="",
        description=(
            "Check if you are DOH personnel involved in disability eligibility "
            "determinations, complaint investigations/prosecutions, or licensure of health "
            "care practitioners or facilities."
        ),
    )

    dept_of_revenue_or_local_government_revenue_or_child_support_enforcement_personnel: BooleanLike = Field(
        default="",
        description=(
            "Check if you are DOR or local government personnel whose duties relate to "
            "revenue collection/enforcement or child support enforcement."
        ),
    )

    donor_or_prospective_donor_cultural_endowment_cso_or_national_historic_landmarks: BooleanLike = Field(
        default="",
        description=(
            "Check if you are a donor or prospective donor covered under the Cultural "
            "Endowment Program Trust Fund, Citizen Support Organizations, or National "
            "Historic Landmarks (publicly owned houses)."
        ),
    )

    firefighter_certified_in_compliance_with_s_633_408_fs: BooleanLike = Field(
        default="",
        description=(
            "Check if you are a firefighter certified in compliance with section 633.408, "
            "Florida Statutes."
        ),
    )

    guardian_ad_litem: BooleanLike = Field(
        default="", description="Check if you are a guardian ad litem."
    )

    human_resource_labor_relations_or_employee_relations_director_or_manager_local_government_or_water_management_district: BooleanLike = Field(
        default="",
        description=(
            "Check if you are HR/labor/employee relations director or manager (or "
            "assistant) of a local government agency or water management district with "
            "personnel-related duties."
        ),
    )

    impaired_practitioner_consultants: BooleanLike = Field(
        default="",
        description=(
            "Check if you are an impaired practitioner consultant who determines a person's "
            "skill and safety to practice a licensed profession."
        ),
    )

    judge_district_circuit_county_or_florida_supreme_court: BooleanLike = Field(
        default="",
        description=(
            "Check if you are a judge of a district court of appeal, circuit court, county "
            "court, or a justice of the Florida Supreme Court."
        ),
    )

    judicial_or_quasi_judicial_officer: BooleanLike = Field(
        default="",
        description=(
            "Check if you are a judicial or quasi-judicial officer as described "
            "(magistrate, judge of compensation claims, DOAH ALJ, or child support "
            "enforcement hearing officer)."
        ),
    )

    juvenile_justice_personnel_listed: BooleanLike = Field(
        default="",
        description=(
            "Check if you hold any of the listed juvenile justice positions with the "
            "Department of Juvenile Justice."
        ),
    )

    law_enforcement_personnel_including_correctional_and_correctional_probation_officers: BooleanLike = Field(
        default="",
        description=(
            "Check if you are law enforcement personnel, including correctional officers or "
            "correctional probation officers."
        ),
    )

    prosecutor: BooleanLike = Field(
        default="",
        description=(
            "Check if you are a prosecutor (state attorney, assistant state attorney, "
            "statewide prosecutor, or assistant statewide prosecutor)."
        ),
    )

    public_defenders_and_criminal_conflict_and_civil_regional_counsel: BooleanLike = Field(
        default="",
        description=(
            "Check if you are a public defender or criminal conflict and civil regional "
            "counsel (including assistants)."
        ),
    )

    servicemembers_after_9_11_2001: BooleanLike = Field(
        default="",
        description=(
            "Check if you are a servicemember who served in the armed forces, reserve "
            "forces, or National Guard after September 11, 2001."
        ),
    )

    us_attorney_or_federal_judge_or_magistrate: BooleanLike = Field(
        default="",
        description=(
            "Check if you are a U.S. attorney or assistant, U.S. appellate judge, U.S. "
            "district court judge, or U.S. magistrate."
        ),
    )

    victim_of_specified_crimes: BooleanLike = Field(
        default="",
        description=(
            "Check if you are a victim of sexual battery, aggravated child abuse, "
            "aggravated stalking, harassment, aggravated battery, or domestic violence "
            "(attach official verification; 5-year exemption)."
        ),
    )

    other_list_applicable_statute: str = Field(
        default="",
        description=(
            "If your exemption category is not listed, specify the applicable statute here. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class RequesterInformationandCertification(BaseModel):
    """Identifying information and signature of the person requesting the exemption"""

    printed_name: str = Field(
        ...,
        description=(
            'Your full printed name. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Your date of birth.")  # YYYY-MM-DD format

    phone_number: str = Field(
        ...,
        description=(
            'Your contact phone number. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    home_address: str = Field(
        ...,
        description=(
            'Your full home mailing address. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Your handwritten or electronic signature certifying the request. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(..., description="Date you sign this request.")  # YYYY-MM-DD format


class FloridaDepartmentOfStatePublicRecordsExemptionRequest(BaseModel):
    """
        FLORIDA DEPARTMENT OF STATE
    PUBLIC RECORDS EXEMPTION REQUEST

        Florida law allows certain persons to request that an agency not publicly disclose specific identification and/or location information contained in any of its agency records. Please refer to sections 119.071 (2)(j), (4)(d) and (5)(i), 265.605, and 267.17, Fla. Stat., or other applicable statute for scope of protection which may include home address, phone numbers, photos, names of spouse and/or children, and their place of employment, and/or school or daycare care facility, date of birth.
        To request the exemption for records in our agency, please complete the form and return to: Secretary of State, c/o Public Records Custodian Director, R.A. Gray Building, 500 S. Bronough St., Tallahassee, FL 32399. For more information, contact 850-245-6536.
        To request that the exemption extend to your spouse and/or children (not applicable for donor* or victim* of battery, abuse, harassment, or stalking) please submit a separate sheet with the name, date of birth, and relationship for purposes of identifying them in any public records within the custody of the agency.
    """

    supplemental_and_addendum_options: SupplementalandAddendumOptions = Field(
        ..., description="Supplemental and Addendum Options"
    )
    exemption_category: ExemptionCategory = Field(..., description="Exemption Category")
    requester_information_and_certification: RequesterInformationandCertification = Field(
        ..., description="Requester Information and Certification"
    )
