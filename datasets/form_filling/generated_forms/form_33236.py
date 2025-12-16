from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Header(BaseModel):
    """General report metadata"""

    date_completed: str = Field(
        ..., description="Date this report form was completed"
    )  # YYYY-MM-DD format


class AVictim(BaseModel):
    """Information about the victim"""

    victim_consents_to_disclosure_of_information: BooleanLike = Field(
        default="",
        description="Check if the victim consents to disclosure of information (Ombudsman use only)",
    )

    name_first_name_middle_initial_last_name: str = Field(
        ...,
        description=(
            "Victim’s full legal name including first name, middle initial, and last name "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    age: Union[float, Literal["N/A", ""]] = Field(..., description="Victim’s age in years")

    date_of_birth: str = Field(
        default="", description="Victim’s date of birth"
    )  # YYYY-MM-DD format

    ssn: str = Field(default="", description="Victim’s Social Security Number, if known")

    gender_m: BooleanLike = Field(default="", description="Check if victim is male")

    gender_f: BooleanLike = Field(default="", description="Check if victim is female")

    ethnicity: str = Field(
        default="",
        description=(
            'Victim’s ethnicity .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    language_english: BooleanLike = Field(
        default="", description="Check if victim’s primary language is English"
    )

    language_non_verbal: BooleanLike = Field(
        default="", description="Check if victim is non-verbal"
    )

    language_other_specify: str = Field(
        default="",
        description=(
            "Specify victim’s primary language if not English or non-verbal .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address_of_facility_include_name_and_notify_ombudsman: str = Field(
        ...,
        description=(
            "Facility address where victim resides, including facility name; notify "
            'Ombudsman .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    city_victim_facility_address: str = Field(
        ...,
        description=(
            'City of the victim’s facility address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zip_code_victim_facility_address: str = Field(
        ..., description="ZIP code of the victim’s facility address"
    )

    telephone_victim_facility_address: str = Field(
        default="",
        description=(
            "Telephone number for the victim’s facility .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    present_location_if_different_from_above: str = Field(
        ...,
        description=(
            "Current location of the victim if different from the facility address .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    city_present_location: str = Field(
        ...,
        description=(
            'City of the victim’s present location .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zip_code_present_location: str = Field(
        ..., description="ZIP code of the victim’s present location"
    )

    telephone_present_location: str = Field(
        default="",
        description=(
            "Telephone number for the victim’s present location .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    elderly_65_plus: BooleanLike = Field(
        default="", description="Check if victim is elderly (65 or older)"
    )

    developmentally_disabled: BooleanLike = Field(
        default="", description="Check if victim is developmentally disabled"
    )

    mentally_ill_disabled: BooleanLike = Field(
        default="", description="Check if victim is mentally ill or mentally disabled"
    )

    physically_disabled: BooleanLike = Field(
        default="", description="Check if victim is physically disabled"
    )

    unknown_other_disability: BooleanLike = Field(
        default="", description="Check if victim’s condition is unknown or other"
    )

    lives_alone: BooleanLike = Field(default="", description="Check if victim lives alone")

    lives_with_others: BooleanLike = Field(
        default="", description="Check if victim lives with others"
    )


class BSuspectedAbuser(BaseModel):
    """Information about the suspected abuser"""

    self_neglect_checkbox: BooleanLike = Field(
        default="", description="Check if suspected abuser is the victim (self-neglect)"
    )

    name_of_suspected_abuser: str = Field(
        default="",
        description=(
            'Full name of the suspected abuser .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    care_custodian_type: str = Field(
        default="",
        description=(
            "If suspected abuser is a care custodian, specify type .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parent_relationship_checkbox: BooleanLike = Field(
        default="", description="Check if suspected abuser is the victim’s parent"
    )

    son_daughter_relationship_checkbox: BooleanLike = Field(
        default="", description="Check if suspected abuser is the victim’s son or daughter"
    )

    other_relationship_to_victim_checkbox_b: BooleanLike = Field(
        default="", description="Check if suspected abuser has another relationship to the victim"
    )

    health_practitioner_type: str = Field(
        default="",
        description=(
            "If suspected abuser is a health practitioner, specify type .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    spouse_relationship_checkbox: BooleanLike = Field(
        default="", description="Check if suspected abuser is the victim’s spouse"
    )

    other_relation_checkbox: BooleanLike = Field(
        default="",
        description="Check if suspected abuser has some other relationship to the victim",
    )

    address_suspected_abuser: str = Field(
        default="",
        description=(
            "Mailing or residence address of the suspected abuser .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    zip_code_suspected_abuser: str = Field(
        ..., description="ZIP code for the suspected abuser’s address"
    )

    telephone_suspected_abuser: str = Field(
        default="",
        description=(
            "Telephone number of the suspected abuser .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    gender_m_suspected_abuser: BooleanLike = Field(
        default="", description="Check if suspected abuser is male"
    )

    gender_f_suspected_abuser: BooleanLike = Field(
        default="", description="Check if suspected abuser is female"
    )

    ethnicity_suspected_abuser: str = Field(
        default="",
        description=(
            'Ethnicity of the suspected abuser .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    age_suspected_abuser: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of the suspected abuser"
    )

    dob_suspected_abuser: str = Field(
        default="", description="Date of birth of the suspected abuser"
    )  # YYYY-MM-DD format

    height_suspected_abuser: str = Field(
        default="",
        description=(
            'Height of the suspected abuser .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    weight_suspected_abuser: str = Field(
        default="",
        description=(
            'Weight of the suspected abuser .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    eyes_suspected_abuser: str = Field(
        default="",
        description=(
            'Eye color of the suspected abuser .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    hair_suspected_abuser: str = Field(
        default="",
        description=(
            'Hair color of the suspected abuser .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class CReportingParty(BaseModel):
    """Information about the person making the report"""

    waives_confidentiality_all: BooleanLike = Field(
        default="", description="Reporting party waives confidentiality to all parties"
    )

    waives_confidentiality_all_but_victim: BooleanLike = Field(
        default="", description="Reporting party waives confidentiality to all except the victim"
    )

    waives_confidentiality_all_but_perpetrator: BooleanLike = Field(
        default="",
        description="Reporting party waives confidentiality to all except the perpetrator",
    )

    name_reporting_party_print: str = Field(
        ...,
        description=(
            'Reporting party’s printed full name .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    signature_reporting_party: str = Field(
        ...,
        description=(
            'Signature of the reporting party .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    occupation_reporting_party: str = Field(
        default="",
        description=(
            'Reporting party’s occupation .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    agency_name_of_business_reporting_party: str = Field(
        default="",
        description=(
            "Agency or business name of the reporting party .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    relation_to_victim_how_knows_of_abuse: str = Field(
        default="",
        description=(
            "Describe relationship to victim or how the reporter knows of the abuse .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    street_reporting_party: str = Field(
        default="",
        description=(
            'Street address of the reporting party .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_reporting_party: str = Field(
        default="",
        description=(
            'City of the reporting party’s address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zip_code_reporting_party: str = Field(
        default="", description="ZIP code of the reporting party’s address"
    )

    email_address_reporting_party: str = Field(
        default="",
        description=(
            'Email address of the reporting party .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    telephone_reporting_party: str = Field(
        default="",
        description=(
            "Telephone number of the reporting party .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class DIncidentInformation(BaseModel):
    """Details about when and where the incident occurred"""

    date_time_of_incidents: str = Field(
        ...,
        description=(
            "Date and time when the incident or incidents occurred .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    place_of_incident_own_home: BooleanLike = Field(
        default="", description="Check if incident occurred in victim’s own home"
    )

    place_of_incident_community_care_facility: BooleanLike = Field(
        default="", description="Check if incident occurred in a community care facility"
    )

    place_of_incident_hospital_acute_care_hospital: BooleanLike = Field(
        default="", description="Check if incident occurred in a hospital or acute care hospital"
    )

    place_of_incident_home_of_another: BooleanLike = Field(
        default="", description="Check if incident occurred in the home of another person"
    )

    place_of_incident_nursing_facility_swing_bed: BooleanLike = Field(
        default="", description="Check if incident occurred in a nursing facility or swing bed"
    )

    place_of_incident_other_specify: str = Field(
        default="",
        description=(
            "Check and specify if incident occurred at some other location .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class EReportedTypesofAbuse(BaseModel):
    """Types and consequences of the abuse"""

    physical_perpetrated_by_others: BooleanLike = Field(
        default="", description="Check if there was physical abuse perpetrated by others"
    )

    assault_battery: BooleanLike = Field(
        default="", description="Check if there was assault or battery"
    )

    constraint_or_deprivation: BooleanLike = Field(
        default="", description="Check if there was unlawful constraint or deprivation"
    )

    sexual_assault: BooleanLike = Field(default="", description="Check if there was sexual assault")

    over_or_under_medication: BooleanLike = Field(
        default="", description="Check if there was over-medication or under-medication"
    )

    neglect_perpetrated_by_others: BooleanLike = Field(
        default="", description="Check if there was neglect by others"
    )

    financial_perpetrated_by_others: BooleanLike = Field(
        default="", description="Check if there was financial abuse by others"
    )

    abandonment: BooleanLike = Field(default="", description="Check if there was abandonment")

    abduction: BooleanLike = Field(default="", description="Check if there was abduction")

    isolation: BooleanLike = Field(
        default="", description="Check if there was isolation of the victim"
    )

    other_non_mandated_perpetrated_by_others: BooleanLike = Field(
        default="",
        description=(
            "Check if other non-mandated abuse occurred (e.g., deprivation of goods or "
            "medical care)"
        ),
    )

    severe_severe_physical_emotional: BooleanLike = Field(
        default="", description="Check if abuse was severe physical or emotional"
    )

    self_neglect_physical_care: BooleanLike = Field(
        default="",
        description="Self-neglect related to physical care (hygiene, food, clothing, shelter)",
    )

    self_neglect_medical_care: BooleanLike = Field(
        default="",
        description="Self-neglect related to medical care (physical and mental health needs)",
    )

    self_neglect_health_and_safety_hazards: BooleanLike = Field(
        default="", description="Self-neglect resulting in health and safety hazards"
    )

    self_neglect_malnutrition_dehydration: BooleanLike = Field(
        default="", description="Self-neglect resulting in malnutrition or dehydration"
    )

    self_neglect_other_non_mandated: BooleanLike = Field(
        default="", description="Other non-mandated self-neglect (e.g., financial)"
    )

    abuse_resulted_in_no_physical_injury: BooleanLike = Field(
        default="", description="Abuse resulted in no physical injury"
    )

    abuse_resulted_in_minor_medical_care: BooleanLike = Field(
        default="", description="Abuse resulted in minor medical care"
    )

    abuse_resulted_in_hospitalization: BooleanLike = Field(
        default="", description="Abuse resulted in hospitalization"
    )

    abuse_resulted_in_care_provider_required: BooleanLike = Field(
        default="", description="Abuse resulted in a care provider being required"
    )

    abuse_resulted_in_death: BooleanLike = Field(default="", description="Abuse resulted in death")

    abuse_resulted_in_mental_suffering: BooleanLike = Field(
        default="", description="Abuse resulted in mental suffering"
    )

    abuse_resulted_in_other_specify: str = Field(
        default="",
        description=(
            'Specify any other result of the abuse .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    abuse_resulted_in_unknown: BooleanLike = Field(
        default="", description="Outcome of abuse is unknown"
    )


class FReportersObservations(BaseModel):
    """Narrative description and observations by the reporter"""

    reporters_observations_beliefs_statements_free_text: str = Field(
        ...,
        description=(
            "Narrative description of observations, beliefs, victim statements, time frame, "
            'and potential danger for investigator .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class GTargetedAccount(BaseModel):
    """Financial account information related to the abuse"""

    account_number_last_4_digits: str = Field(
        default="",
        description=(
            "Last four digits of the targeted account number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    type_of_account_deposit: BooleanLike = Field(
        default="", description="Check if targeted account is a deposit account"
    )

    type_of_account_credit: BooleanLike = Field(
        default="", description="Check if targeted account is a credit account"
    )

    type_of_account_other: BooleanLike = Field(
        default="", description="Check if targeted account is some other type of account"
    )

    trust_account_yes: BooleanLike = Field(
        default="", description="Check YES if this is a trust account"
    )

    trust_account_no: BooleanLike = Field(
        default="", description="Check NO if this is not a trust account"
    )

    power_of_attorney_yes: BooleanLike = Field(
        default="", description="Check YES if a power of attorney exists"
    )

    power_of_attorney_no: BooleanLike = Field(
        default="", description="Check NO if no power of attorney exists"
    )

    direct_deposit_yes: BooleanLike = Field(
        default="", description="Check YES if direct deposit is used"
    )

    direct_deposit_no: BooleanLike = Field(
        default="", description="Check NO if direct deposit is not used"
    )

    other_accounts_yes: BooleanLike = Field(
        default="", description="Check YES if there are other related accounts"
    )

    other_accounts_no: BooleanLike = Field(
        default="", description="Check NO if there are no other related accounts"
    )


class HOtherPersonwithKnowledgeofAbuse(BaseModel):
    """Contact information for others who may know about the abuse"""

    name_other_person_with_knowledge: str = Field(
        default="",
        description=(
            "Name of another person believed to have knowledge of the abuse .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address_other_person_with_knowledge: str = Field(
        default="",
        description=(
            "Address of the person believed to have knowledge of the abuse .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    telephone_other_person_with_knowledge: str = Field(
        default="",
        description=(
            "Telephone number of the person believed to have knowledge of the abuse .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    relationship_other_person_with_knowledge: str = Field(
        default="",
        description=(
            "Relationship of this person to the victim or situation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IFamilyMemberorResponsiblePerson(BaseModel):
    """Family member or other person responsible for the victim’s care"""

    name_family_member_or_responsible_person: str = Field(
        ...,
        description=(
            "Name of family member or other person responsible for the victim’s care, or "
            'contact person .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    if_contact_person_only_checkbox: BooleanLike = Field(
        default="",
        description="Check if this person is a contact person only, not responsible for care",
    )

    relationship_family_or_responsible_person: str = Field(
        default="",
        description=(
            "Relationship of this person to the victim .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_family_or_responsible_person: str = Field(
        ...,
        description=(
            "Address of the family member or other responsible person .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_family_or_responsible_person: str = Field(
        ...,
        description=(
            "City of the responsible person’s address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    zip_code_family_or_responsible_person: str = Field(
        ..., description="ZIP code of the responsible person’s address"
    )

    telephone_family_or_responsible_person: str = Field(
        ...,
        description=(
            "Telephone number of the responsible or contact person .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class JTelephoneReport(BaseModel):
    """Details of the telephone report made to authorities"""

    telephone_report_local_aps: BooleanLike = Field(
        default="", description="Check if telephone report was made to Local APS"
    )

    telephone_report_law_enforcement: BooleanLike = Field(
        default="", description="Check if telephone report was made to Law Enforcement"
    )

    telephone_report_local_ombudsman: BooleanLike = Field(
        default="", description="Check if telephone report was made to Local Ombudsman"
    )

    telephone_report_calif_dept_of_mental_health: BooleanLike = Field(
        default="",
        description="Check if telephone report was made to California Department of Mental Health",
    )

    telephone_report_calif_dept_of_developmental_services: BooleanLike = Field(
        default="",
        description=(
            "Check if telephone report was made to California Department of Developmental Services"
        ),
    )

    name_of_official_contacted_by_phone: str = Field(
        default="",
        description=(
            "Name of the official contacted by telephone .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_official_contacted: str = Field(
        ...,
        description=(
            "Telephone number used to contact the official .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_time_telephone_report: str = Field(
        default="",
        description=(
            "Date and time the telephone report was made .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class KWrittenReport(BaseModel):
    """Information about the agency receiving the written report"""

    agency_name_receiving_written_report: str = Field(
        default="",
        description=(
            "Name of the agency receiving the written report .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_or_fax_receiving_written_report: str = Field(
        default="",
        description=(
            "Mailing address or fax number of the agency receiving the written report .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_mailed: str = Field(
        default="", description="Date the written report was mailed"
    )  # YYYY-MM-DD format

    date_faxed: str = Field(
        default="", description="Date the written report was faxed"
    )  # YYYY-MM-DD format


class LReceivingAgencyUseOnly(BaseModel):
    """For use by the receiving agency to document intake and cross-reporting"""

    receiving_agency_telephone_report_checkbox: BooleanLike = Field(
        default="", description="Receiving agency indicates this is a telephone report"
    )

    receiving_agency_written_report_checkbox: BooleanLike = Field(
        default="", description="Receiving agency indicates this is a written report"
    )

    report_received_by: str = Field(
        default="",
        description=(
            "Name of staff member who received the report .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_time_report_received: str = Field(
        default="",
        description=(
            'Date and time the report was received .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    assigned_immediate_response: BooleanLike = Field(
        default="", description="Case assigned for immediate response"
    )

    assigned_ten_day_response: BooleanLike = Field(
        default="", description="Case assigned for ten-day response"
    )

    assigned_no_initial_face_to_face_required: BooleanLike = Field(
        default="", description="Case assigned with no initial face-to-face contact required"
    )

    assigned_not_aps: BooleanLike = Field(
        default="", description="Check if case is determined not to be APS"
    )

    assigned_not_ombudsman: BooleanLike = Field(
        default="", description="Check if case is determined not to be Ombudsman"
    )

    approved_by: str = Field(
        default="",
        description=(
            "Name of supervisor or official who approved the assignment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    assigned_to_optional: str = Field(
        default="",
        description=(
            "Name of worker or unit the case is assigned to (optional) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cross_reported_to_cws_chms_licensing_cert: BooleanLike = Field(
        default="", description="Check if cross-reported to CWS & CHMS, Licensing & Certification"
    )

    cross_reported_to_cdss_ccl: BooleanLike = Field(
        default="",
        description="Check if cross-reported to CDSS Community Care Licensing (CDSS-CCL)",
    )

    cross_reported_to_cda_ombudsman: BooleanLike = Field(
        default="", description="Check if cross-reported to CDA Ombudsman"
    )

    cross_reported_to_bureau_of_medi_cal_fraud_elder_abuse: BooleanLike = Field(
        default="",
        description="Check if cross-reported to the Bureau of Medi-Cal Fraud & Elder Abuse",
    )

    cross_reported_to_mental_health: BooleanLike = Field(
        default="", description="Check if cross-reported to Mental Health"
    )

    cross_reported_to_law_enforcement: BooleanLike = Field(
        default="", description="Check if cross-reported to Law Enforcement"
    )

    cross_reported_to_professional_board: BooleanLike = Field(
        default="", description="Check if cross-reported to a professional licensing board"
    )

    cross_reported_to_developmental_services: BooleanLike = Field(
        default="", description="Check if cross-reported to Developmental Services"
    )

    cross_reported_to_aps: BooleanLike = Field(
        default="", description="Check if cross-reported to Adult Protective Services (APS)"
    )

    cross_reported_to_other_specify: str = Field(
        default="",
        description=(
            "Check and specify any other agency to which the report was cross-reported .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_of_cross_report: str = Field(
        default="", description="Date the cross-report was made"
    )  # YYYY-MM-DD format

    aps_ombudsman_law_enforcement_case_file_number: str = Field(
        default="",
        description=(
            "Case file number used by APS, Ombudsman, or Law Enforcement .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ReportOfSuspectedDependentAdultelderAbuse(BaseModel):
    """
    REPORT OF SUSPECTED DEPENDENT ADULT/ELDER ABUSE

    CONFIDENTIAL REPORT - NOT SUBJECT TO PUBLIC DISCLOSURE
    REPORT OF SUSPECTED DEPENDENT ADULT/ELDER ABUSE
    """

    header: Header = Field(..., description="Header")
    a_victim: AVictim = Field(..., description="A. Victim")
    b_suspected_abuser: BSuspectedAbuser = Field(..., description="B. Suspected Abuser")
    c_reporting_party: CReportingParty = Field(..., description="C. Reporting Party")
    d_incident_information: DIncidentInformation = Field(..., description="D. Incident Information")
    e_reported_types_of_abuse: EReportedTypesofAbuse = Field(
        ..., description="E. Reported Types of Abuse"
    )
    f_reporters_observations: FReportersObservations = Field(
        ..., description="F. Reporter’s Observations"
    )
    g_targeted_account: GTargetedAccount = Field(..., description="G. Targeted Account")
    h_other_person_with_knowledge_of_abuse: HOtherPersonwithKnowledgeofAbuse = Field(
        ..., description="H. Other Person with Knowledge of Abuse"
    )
    i_family_member_or_responsible_person: IFamilyMemberorResponsiblePerson = Field(
        ..., description="I. Family Member or Responsible Person"
    )
    j_telephone_report: JTelephoneReport = Field(..., description="J. Telephone Report")
    k_written_report: KWrittenReport = Field(..., description="K. Written Report")
    l_receiving_agency_use_only: LReceivingAgencyUseOnly = Field(
        ..., description="L. Receiving Agency Use Only"
    )
