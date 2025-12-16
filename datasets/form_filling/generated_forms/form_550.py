from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class TellUsAboutYourChild(BaseModel):
    """Basic information about the child patient"""

    todays_date: str = Field(
        ..., description="Date this form is being completed"
    )  # YYYY-MM-DD format

    childs_name: str = Field(
        ...,
        description=(
            'Child\'s full legal name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    childs_name_last: str = Field(
        ...,
        description=(
            'Child\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    childs_name_first: str = Field(
        ...,
        description=(
            'Child\'s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    childs_name_mi: str = Field(
        default="",
        description=(
            'Child\'s middle initial .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    nickname: str = Field(
        default="",
        description=(
            'Name the child prefers to be called .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    male: BooleanLike = Field(..., description="Check if the child is male")

    female: BooleanLike = Field(..., description="Check if the child is female")

    childs_birthdate: str = Field(..., description="Child's date of birth")  # YYYY-MM-DD format

    childs_age: Union[float, Literal["N/A", ""]] = Field(..., description="Child's age in years")

    school: str = Field(
        default="",
        description=(
            'Name of the child\'s school .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    grade: str = Field(
        default="",
        description=(
            'Child\'s current grade level .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    general_pediatric_dentist: str = Field(
        default="",
        description=(
            "Name of the child's general or pediatric dentist .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_last_visit: str = Field(
        default="", description="Date of the child's last dental visit"
    )  # YYYY-MM-DD format

    who_may_we_thank_for_referring_your_child: str = Field(
        default="",
        description=(
            "Name of the person or source that referred your child .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AccompanyingAdultFamily(BaseModel):
    """Information about the adult accompanying the child and family status"""

    name_person_accompanying_child_today: str = Field(
        ...,
        description=(
            "Name of the person accompanying the child to this visit .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    relation_person_accompanying_child_today: str = Field(
        ...,
        description=(
            "Relationship of the accompanying person to the child .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    legal_custody_yes: BooleanLike = Field(
        ..., description="Check YES if you have legal custody of the child"
    )

    legal_custody_no: BooleanLike = Field(
        ..., description="Check NO if you do not have legal custody of the child"
    )

    other_family_members_seen_by_us: str = Field(
        default="",
        description=(
            "Names of other family members treated in this office .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parents_marital_status_single: BooleanLike = Field(
        default="", description="Check if parent's marital status is single"
    )

    parents_marital_status_widowed: BooleanLike = Field(
        default="", description="Check if parent's marital status is widowed"
    )

    parents_marital_status_separated: BooleanLike = Field(
        default="", description="Check if parent's marital status is separated"
    )

    parents_marital_status_married: BooleanLike = Field(
        default="", description="Check if parent's marital status is married"
    )

    parents_marital_status_divorced: BooleanLike = Field(
        default="", description="Check if parent's marital status is divorced"
    )


class ParentalInformation(BaseModel):
    """Contact and employment information for mother and father/guardians"""

    mother_step_mother: BooleanLike = Field(
        default="", description="Check if this person is a step mother"
    )

    mother_guardian: BooleanLike = Field(
        default="", description="Check if this person is a legal guardian (mother section)"
    )

    mother_name: str = Field(
        ...,
        description=(
            'Mother or female guardian\'s full name .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mother_address: str = Field(
        default="",
        description=(
            "Mother or female guardian's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mother_home_number: str = Field(
        default="",
        description=(
            "Mother or female guardian's home phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mother_work_number: str = Field(
        default="",
        description=(
            "Mother or female guardian's work phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mother_ext: str = Field(
        default="",
        description=(
            "Extension for mother's work phone, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mother_employer: str = Field(
        default="",
        description=(
            'Mother or female guardian\'s employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mother_ssn: str = Field(
        default="", description="Mother or female guardian's Social Security Number"
    )

    father_step_father: BooleanLike = Field(
        default="", description="Check if this person is a step father"
    )

    father_guardian: BooleanLike = Field(
        default="", description="Check if this person is a legal guardian (father section)"
    )

    father_name: str = Field(
        ...,
        description=(
            'Father or male guardian\'s full name .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    father_address: str = Field(
        default="",
        description=(
            "Father or male guardian's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    father_home_number: str = Field(
        default="",
        description=(
            "Father or male guardian's home phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    father_work_number: str = Field(
        default="",
        description=(
            "Father or male guardian's work phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    father_ext: str = Field(
        default="",
        description=(
            "Extension for father's work phone, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    father_employer: str = Field(
        default="",
        description=(
            'Father or male guardian\'s employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    father_ssn: str = Field(
        default="", description="Father or male guardian's Social Security Number"
    )


class PersonResponsibleforAccount(BaseModel):
    """Billing contact and appointment responsibility"""

    person_responsible_for_account_name: str = Field(
        ...,
        description=(
            "Full name of the person financially responsible for the account .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    person_responsible_for_account_relation: str = Field(
        ...,
        description=(
            "Relationship of the responsible person to the child .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    billing_address: str = Field(
        ...,
        description=(
            'Billing address for the account .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    billing_address_street: str = Field(
        ...,
        description=(
            'Street address for billing .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    billing_address_apt_condo: str = Field(
        default="",
        description=(
            "Apartment or condo number for billing address, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City for the billing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the billing address")

    zip: str = Field(..., description="ZIP code for the billing address")

    person_responsible_home_number: str = Field(
        ...,
        description=(
            "Home phone number of the person responsible for the account .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    person_responsible_work_number: str = Field(
        default="",
        description=(
            "Work phone number of the person responsible for the account .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    person_responsible_ext: str = Field(
        default="",
        description=(
            "Extension for the responsible person's work phone, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    person_responsible_employer: str = Field(
        default="",
        description=(
            "Employer of the person responsible for the account .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    person_responsible_ssn: str = Field(
        default="", description="Social Security Number of the person responsible for the account"
    )

    appointments_responsible_name: str = Field(
        default="",
        description=(
            "Name of the person who will schedule appointments .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    appointments_responsible_home_number: str = Field(
        default="",
        description=(
            "Home phone number of the person who will schedule appointments .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    appointments_responsible_work_number: str = Field(
        default="",
        description=(
            "Work phone number of the person who will schedule appointments .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    appointments_responsible_ext: str = Field(
        default="",
        description=(
            "Extension for the appointment contact's work phone, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PrimaryDentalInsurance(BaseModel):
    """Details of the primary dental/orthodontic insurance coverage"""

    primary_ortho_coverage_yes: BooleanLike = Field(
        default="",
        description="Check YES if the primary dental insurance includes orthodontic coverage",
    )

    primary_ortho_coverage_no: BooleanLike = Field(
        default="",
        description="Check NO if the primary dental insurance does not include orthodontic coverage",
    )

    primary_insurance_company_name: str = Field(
        default="",
        description=(
            "Name of the primary dental insurance company .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    primary_insurance_company_phone: str = Field(
        default="",
        description=(
            "Phone number of the primary dental insurance company .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_group_number: str = Field(
        default="",
        description=(
            "Primary dental insurance group, plan, or policy number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_insured_name: str = Field(
        default="",
        description=(
            'Name of the primary insured person .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    primary_relationship_to_patient: str = Field(
        default="",
        description=(
            "Relationship of the primary insured to the patient .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_insured_birthday: str = Field(
        default="", description="Date of birth of the primary insured"
    )  # YYYY-MM-DD format

    primary_insured_ssn: str = Field(
        default="", description="Social Security Number of the primary insured"
    )

    primary_insured_employer: str = Field(
        default="",
        description=(
            'Employer of the primary insured .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class SecondaryDentalInsurance(BaseModel):
    """Details of the secondary dental/orthodontic insurance coverage"""

    secondary_ortho_coverage_yes: BooleanLike = Field(
        default="",
        description="Check YES if the secondary dental insurance includes orthodontic coverage",
    )

    secondary_ortho_coverage_no: BooleanLike = Field(
        default="",
        description=(
            "Check NO if the secondary dental insurance does not include orthodontic coverage"
        ),
    )

    secondary_insurance_company_name: str = Field(
        default="",
        description=(
            "Name of the secondary dental insurance company .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    secondary_insurance_company_phone: str = Field(
        default="",
        description=(
            "Phone number of the secondary dental insurance company .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    secondary_group_number: str = Field(
        default="",
        description=(
            "Secondary dental insurance group, plan, or policy number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    secondary_insured_name: str = Field(
        default="",
        description=(
            'Name of the secondary insured person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    secondary_relationship_to_patient: str = Field(
        default="",
        description=(
            "Relationship of the secondary insured to the patient .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    secondary_insured_birthday: str = Field(
        default="", description="Date of birth of the secondary insured"
    )  # YYYY-MM-DD format

    secondary_insured_ssn: str = Field(
        default="", description="Social Security Number of the secondary insured"
    )

    secondary_insured_employer: str = Field(
        default="",
        description=(
            'Employer of the secondary insured .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class BrianWPayneDdsOrthodonticSpecialistForAdultsChildren(BaseModel):
    """
        BRIAN W PAYNE DDS
    orthodontic specialist for adults & children

        WE WOULD LIKE TO WELCOME YOU AND YOUR CHILD TO OUR OFFICE. OUR GOAL IS TO MAKE EVERY CHILD'S VISIT PLEASANT AND EDUCATIONAL. WE STRIVE TO TEACH GOOD ORAL CARE THAT WILL ENABLE YOUR CHILD TO HAVE A BEAUTIFUL SMILE THAT LASTS A LIFETIME.
    """

    tell_us_about_your_child: TellUsAboutYourChild = Field(
        ..., description="Tell Us About Your Child"
    )
    accompanying_adult__family: AccompanyingAdultFamily = Field(
        ..., description="Accompanying Adult & Family"
    )
    parental_information: ParentalInformation = Field(..., description="Parental Information")
    person_responsible_for_account: PersonResponsibleforAccount = Field(
        ..., description="Person Responsible for Account"
    )
    primary_dental_insurance: PrimaryDentalInsurance = Field(
        ..., description="Primary Dental Insurance"
    )
    secondary_dental_insurance: SecondaryDentalInsurance = Field(
        ..., description="Secondary Dental Insurance"
    )
