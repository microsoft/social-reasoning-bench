from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ComplainantInformation(BaseModel):
    """Information about the business or person defrauded and the person who accepted the check"""

    name_of_business_or_person_defrauded: str = Field(
        ...,
        description=(
            "Full legal name of the business or individual who was defrauded .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    business_address: str = Field(
        ...,
        description=(
            "Street address of the defrauded business .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the defrauded business .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the defrauded business")

    zip: str = Field(..., description="ZIP code of the defrauded business")

    phone_number: str = Field(
        ...,
        description=(
            "Primary phone number for the defrauded business .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    business_owners_name: str = Field(
        ...,
        description=(
            'Name of the business owner .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    name_of_person_who_actually_accepted_the_check: str = Field(
        ...,
        description=(
            "Full name of the person who actually accepted the check .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    home_address_of_person_who_accepted_the_check: str = Field(
        ...,
        description=(
            "Home street address of the person who accepted the check .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_person_who_accepted_the_check: str = Field(
        ...,
        description=(
            "Home city of the person who accepted the check .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_person_who_accepted_the_check: str = Field(
        ..., description="Home state of the person who accepted the check"
    )

    zip_person_who_accepted_the_check: str = Field(
        ..., description="Home ZIP code of the person who accepted the check"
    )

    phone_number_person_who_accepted_the_check: str = Field(
        ...,
        description=(
            "Phone number of the person who accepted the check .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    saw_id_and_verified_information_yes: BooleanLike = Field(
        ...,
        description=(
            "Select if the person who accepted the check saw the check writer's ID and "
            "verified the information (Yes option)"
        ),
    )

    saw_id_and_verified_information_no: BooleanLike = Field(
        ...,
        description=(
            "Select if the person who accepted the check did not see or verify the check "
            "writer's ID (No option)"
        ),
    )

    can_recognize_check_writer_in_court_yes: BooleanLike = Field(
        ...,
        description=(
            "Select if the person can recognize the check writer and identify them in court "
            "(Yes option)"
        ),
    )

    can_recognize_check_writer_in_court_no: BooleanLike = Field(
        ...,
        description="Select if the person cannot recognize the check writer in court (No option)",
    )

    check_received_by_mail_yes: BooleanLike = Field(
        ..., description="Indicate that the check was received by mail (Yes option)"
    )

    check_received_by_mail_no: BooleanLike = Field(
        ..., description="Indicate that the check was not received by mail (No option)"
    )

    check_postdated_yes: BooleanLike = Field(
        ..., description="Indicate that the check was postdated (Yes option)"
    )

    check_postdated_no: BooleanLike = Field(
        ..., description="Indicate that the check was not postdated (No option)"
    )

    check_passed_in_lincoln_county_yes: BooleanLike = Field(
        ..., description="Indicate that the check was passed in Lincoln County (Yes option)"
    )

    check_passed_in_lincoln_county_no: BooleanLike = Field(
        ..., description="Indicate that the check was not passed in Lincoln County (No option)"
    )

    partial_payment_accepted_yes: BooleanLike = Field(
        ..., description="Indicate that partial payment on the check was accepted (Yes option)"
    )

    partial_payment_accepted_no: BooleanLike = Field(
        ..., description="Indicate that no partial payment on the check was accepted (No option)"
    )

    agreement_to_hold_check_yes: BooleanLike = Field(
        ..., description="Indicate that there was an agreement to hold the check (Yes option)"
    )

    agreement_to_hold_check_no: BooleanLike = Field(
        ..., description="Indicate that there was no agreement to hold the check (No option)"
    )

    goods_or_services_description: str = Field(
        ...,
        description=(
            "Describe the goods or services for which the check was written .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    notification_of_improper_services_or_defective_goods: str = Field(
        default="",
        description=(
            "Indicate if you were ever notified that services were improper or goods "
            "defective; include brief details if space allows .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CheckWriterInformation(BaseModel):
    """Identifying and contact information for the check writer and check details"""

    name_check_writer: str = Field(
        ...,
        description=(
            'Full name of the check writer .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address_check_writer: str = Field(
        ...,
        description=(
            'Street address of the check writer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_check_writer: str = Field(
        ...,
        description=(
            'City of the check writer .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state_check_writer: str = Field(..., description="State of the check writer")

    zip_check_writer: str = Field(..., description="ZIP code of the check writer")

    telephone_check_writer: str = Field(
        ...,
        description=(
            'Telephone number of the check writer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth_check_writer: str = Field(
        ..., description="Date of birth of the check writer"
    )  # YYYY-MM-DD format

    drivers_license_or_social_security_number: str = Field(
        ...,
        description=(
            "Driver's license number or Social Security number of the check writer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    state_of_issue_id_ssn: str = Field(
        ..., description="State that issued the driver's license or ID used"
    )

    check_number: str = Field(
        ...,
        description=(
            'Number printed on the check .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    amount_of_check: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Dollar amount of the check"
    )

    date_received: str = Field(..., description="Date the check was received")  # YYYY-MM-DD format

    additional_information_location_of_check_writer: str = Field(
        default="",
        description=(
            "Any additional information that may help locate the check writer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SignaturesandCertification(BaseModel):
    """Signatures and certification related to the referral"""

    signature_of_owner_manager: str = Field(
        ...,
        description=(
            "Signature of the business owner or manager affirming the information .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    signature_of_person_who_accepted_the_check: str = Field(
        ...,
        description=(
            "Signature of the person who accepted the check .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    printed_name: str = Field(
        ...,
        description=(
            "Printed name of the person signing the form .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format


class StopPaymentCheckReferralForm(BaseModel):
    """
    STOP PAYMENT CHECK REFERRAL FORM

    ''
    """

    complainant_information: ComplainantInformation = Field(
        ..., description="Complainant Information"
    )
    check_writer_information: CheckWriterInformation = Field(
        ..., description="Check Writer Information"
    )
    signatures_and_certification: SignaturesandCertification = Field(
        ..., description="Signatures and Certification"
    )
