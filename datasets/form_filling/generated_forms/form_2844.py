from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ContactInformation(BaseModel):
    """Primary contact and address details for the applicant"""

    mr: BooleanLike = Field(..., description="Select if your preferred title is Mr.")

    ms: BooleanLike = Field(..., description="Select if your preferred title is Ms.")

    mrs: BooleanLike = Field(..., description="Select if your preferred title is Mrs.")

    name_first_mi_last: str = Field(
        ...,
        description=(
            "Full legal name including first name, middle initial, and last name .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    nickname: str = Field(
        default="",
        description=(
            'Preferred name or nickname .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    current_address: str = Field(
        ...,
        description=(
            'Current street address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    city_current_address: str = Field(
        ...,
        description=(
            'City for your current address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state_province_current_address: str = Field(
        ...,
        description=(
            "State or province for your current address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    zip_postal_code_current_address: str = Field(
        ..., description="ZIP or postal code for your current address"
    )

    phone_number: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Primary email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    home_address_if_different_than_current_address: str = Field(
        default="",
        description=(
            "Home street address if different from current address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_home_address: str = Field(
        default="",
        description=(
            'City for your home address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state_province_home_address: str = Field(
        default="",
        description=(
            "State or province for your home address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    zip_postal_code_home_address: str = Field(
        default="", description="ZIP or postal code for your home address"
    )


class MemberProfile(BaseModel):
    """Academic program and student status information"""

    bachelors: BooleanLike = Field(
        ..., description="Select if you are pursuing a Bachelor's degree"
    )

    masters: BooleanLike = Field(..., description="Select if you are pursuing a Master's degree")

    ph_d: BooleanLike = Field(..., description="Select if you are pursuing a Ph.D. degree")

    university_college: str = Field(
        ...,
        description=(
            "Name of the university or college you attend .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    expected_date_of_graduation_month_year: str = Field(
        ...,
        description=(
            "Expected graduation date in month/year format .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major: str = Field(
        ...,
        description=(
            'Your academic major or field of study .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class PaymentInformation(BaseModel):
    """Membership dues payment method and card details"""

    visa: BooleanLike = Field(..., description="Select if paying by Visa credit card")

    mastercard: BooleanLike = Field(..., description="Select if paying by MasterCard credit card")

    amex: BooleanLike = Field(..., description="Select if paying by American Express credit card")

    check_payable_to_naiop: BooleanLike = Field(
        ..., description="Select if paying by check payable to NAIOP"
    )

    credit_card_number: str = Field(
        ...,
        description=(
            'Credit card number for payment .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    exp_date: str = Field(
        ...,
        description=(
            'Credit card expiration date .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    name_of_cardholder_please_print: str = Field(
        ...,
        description=(
            "Name of the cardholder as it appears on the card .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cvv: str = Field(
        ...,
        description=(
            'Card security code (CVV) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class MembershipAgreement(BaseModel):
    """Agreement to membership terms and communications"""

    signature: str = Field(
        ...,
        description=(
            "Applicant's signature agreeing to the membership terms .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_membership_agreement: str = Field(
        ..., description="Date the membership agreement is signed"
    )  # YYYY-MM-DD format


class DemographicProfile(BaseModel):
    """Optional demographic and marketing information"""

    birthdate: str = Field(default="", description="Your date of birth")  # YYYY-MM-DD format

    gender_male: BooleanLike = Field(default="", description="Select if your gender is male")

    gender_female: BooleanLike = Field(default="", description="Select if your gender is female")

    ethnic_background_african_american: BooleanLike = Field(
        default="", description="Select if your ethnic background is African American"
    )

    ethnic_background_hispanic: BooleanLike = Field(
        default="", description="Select if your ethnic background is Hispanic"
    )

    ethnic_background_caucasian: BooleanLike = Field(
        default="", description="Select if your ethnic background is Caucasian"
    )

    ethnic_background_asian_pacific_islander_or_native_hawaiian: BooleanLike = Field(
        default="",
        description="Select if your ethnic background is Asian, Pacific Islander, or Native Hawaiian",
    )

    ethnic_background_american_indian_or_native_alaskan: BooleanLike = Field(
        default="",
        description="Select if your ethnic background is American Indian or Native Alaskan",
    )

    ethnic_background_other_please_specify: str = Field(
        default="",
        description=(
            "If your ethnic background is not listed, specify it here .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_did_you_hear_about_naiop_local_chapter: BooleanLike = Field(
        default="", description="Select if you heard about NAIOP from a local chapter"
    )

    how_did_you_hear_about_naiop_naiop_website: BooleanLike = Field(
        default="", description="Select if you heard about NAIOP from the NAIOP website"
    )

    how_did_you_hear_about_naiop_social_media: BooleanLike = Field(
        default="", description="Select if you heard about NAIOP through social media"
    )

    how_did_you_hear_about_naiop_development_magazine: BooleanLike = Field(
        default="", description="Select if you heard about NAIOP from Development magazine"
    )

    how_did_you_hear_about_naiop_naiop_conference_event: BooleanLike = Field(
        default="", description="Select if you heard about NAIOP at a NAIOP conference or event"
    )

    how_did_you_hear_about_naiop_member_referral_name: str = Field(
        default="",
        description=(
            "Name of the member who referred you, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_did_you_hear_about_naiop_ad_publication: str = Field(
        default="",
        description=(
            "Name of the publication where you saw the advertisement .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_did_you_hear_about_naiop_direct_mail: BooleanLike = Field(
        default="", description="Select if you heard about NAIOP through direct mail"
    )

    how_did_you_hear_about_naiop_other: str = Field(
        default="",
        description=(
            "If you heard about NAIOP through another source, describe it here .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class NaiopRealEstateDevAssocStudentMembershipApp2021(BaseModel):
    """
        NAIOP
    COMMERCIAL REAL ESTATE
    DEVELOPMENT ASSOCIATION

    2021 STUDENT MEMBERSHIP APPLICATION

        Reserved for full-time students as defined by the university. Individuals employed full-time are not eligible. Documentation to verify full-time student status is required.
    """

    contact_information: ContactInformation = Field(..., description="Contact Information")
    member_profile: MemberProfile = Field(..., description="Member Profile")
    payment_information: PaymentInformation = Field(..., description="Payment Information")
    membership_agreement: MembershipAgreement = Field(..., description="Membership Agreement")
    demographic_profile: DemographicProfile = Field(..., description="Demographic Profile")
