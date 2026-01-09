from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RequesterInformation(BaseModel):
    """Basic identifying information about the requester"""

    title_name: str = Field(
        ...,
        description=(
            "Title for your primary name (e.g., Mr, Ms, Dr). .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    first_name_name: str = Field(
        ...,
        description=(
            'Your primary first (given) name. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    last_name_name: str = Field(
        ...,
        description=(
            'Your primary last (family) name. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    suffix_name: str = Field(
        default="",
        description=(
            "Name suffix for your primary name (e.g., Jr, Sr, III). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title_alias_or_previously_used_it: str = Field(
        default="",
        description=(
            "Title for any alias or previously used name. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    first_name_alias_or_previously_used_it: str = Field(
        default="",
        description=(
            "First name for any alias or previously used name. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    last_name_alias_or_previously_used_it: str = Field(
        default="",
        description=(
            "Last name for any alias or previously used name. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    suffix_alias_or_previously_used_it: str = Field(
        default="",
        description=(
            "Name suffix for any alias or previously used name. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            "Primary phone number where you can be reached. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Email address used to confirm your identity and send copies. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    contact_address_address_line_1: str = Field(
        ...,
        description=(
            "First line of your primary contact address. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_address_address_line_2: str = Field(
        default="",
        description=(
            "Second line of your primary contact address (optional). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_address_city: str = Field(
        ...,
        description=(
            "City for your primary contact address. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_address_state_province: str = Field(
        ...,
        description=(
            "State or province for your primary contact address. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_address_zip_postal_code: str = Field(
        ..., description="ZIP or postal code for your primary contact address."
    )

    contact_address_country: str = Field(
        ...,
        description=(
            "Country for your primary contact address. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_address_line_1: str = Field(
        default="",
        description=(
            "First line of your mailing address, if different from contact address. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mailing_address_address_line_2: str = Field(
        default="",
        description=(
            "Second line of your mailing address (optional). .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_city: str = Field(
        default="",
        description=(
            'City for your mailing address. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_state_province: str = Field(
        default="",
        description=(
            "State or province for your mailing address. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_zip_postal_code: str = Field(
        default="", description="ZIP or postal code for your mailing address."
    )

    mailing_address_country: str = Field(
        default="",
        description=(
            'Country for your mailing address. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    customer_policy_number: str = Field(
        default="",
        description=(
            "Your insurance policy number, if you are a customer. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_issuing_insurance_company: str = Field(
        default="",
        description=(
            "Name of the insurance company that issued your policy. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    claim_number: str = Field(
        default="",
        description=(
            "Your claim number, if you are a claimant. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dates_of_employment: str = Field(
        default="",
        description=(
            "Your dates of employment, if you are a current or former employee. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    proof_of_identity: str = Field(
        ...,
        description=(
            "Indicate and attach the form of photo ID you are providing for validation. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class RequestType(BaseModel):
    """Selection of the nature of the subject access or data protection request"""

    data_protection_complaint_request_type: BooleanLike = Field(
        ..., description="Select this if your request is a data protection complaint."
    )

    personal_data_access_request_request_type: BooleanLike = Field(
        ..., description="Select this if you are requesting access to your personal data."
    )

    correction_of_personal_data_request_type: BooleanLike = Field(
        ..., description="Select this if you are requesting correction of your personal data."
    )

    processing_information_inquiry_request_type: BooleanLike = Field(
        ...,
        description="Select this if you are inquiring about how your personal data is processed.",
    )

    restrict_processing_of_my_personal_data_request_type: BooleanLike = Field(
        ...,
        description=(
            "Select this if you are requesting restriction of processing of your personal data."
        ),
    )

    request_to_erase_my_personal_data_request_type: BooleanLike = Field(
        ..., description="Select this if you are requesting erasure of your personal data."
    )

    portability_request_for_my_personal_data_request_type: BooleanLike = Field(
        ..., description="Select this if you are requesting portability of your personal data."
    )


class DataProtectionComplaintDetails(BaseModel):
    """Information related to a data protection complaint"""

    details_of_your_complaint: str = Field(
        default="",
        description=(
            "Provide full details of your data protection complaint. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PersonalDataAccessRequestDetails(BaseModel):
    """Information related to a personal data access request"""

    details_of_the_specific_personal_data_you_seek_access_request: str = Field(
        default="",
        description=(
            "Describe the specific personal data you are requesting access to. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    why_we_are_likely_to_hold_the_above_personal_data_access_request: str = Field(
        default="",
        description=(
            "Explain why you believe we hold this personal data (relationship, context, "
            'desired results). .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class CorrectionofPersonalDataDetails(BaseModel):
    """Information and evidence for correcting personal data"""

    evidence_to_support_that_this_data_is_correct: str = Field(
        default="",
        description=(
            "List or describe any evidence you are attaching to show the data is correct. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    details_of_the_specific_personal_data_you_are_seeking_to_correct: str = Field(
        default="",
        description=(
            "Describe the specific personal data you want us to correct. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    why_we_are_likely_to_hold_the_above_personal_data_correction: str = Field(
        default="",
        description=(
            "Explain why you believe we hold the personal data you want corrected. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ProcessingInformationInquiryDetails(BaseModel):
    """Questions and context about processing of personal data"""

    your_questions_about_our_processing_of_personal_data: str = Field(
        default="",
        description=(
            "List your questions about how we process your personal data. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    why_we_are_likely_to_hold_the_above_personal_data_processing_inquiry: str = Field(
        default="",
        description=(
            "Explain why you believe we hold the personal data related to your processing "
            'inquiry. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class RestrictProcessingRequestDetails(BaseModel):
    """Information related to a request to restrict processing of personal data"""

    personal_data_for_which_you_seek_to_restrict_processing: str = Field(
        default="",
        description=(
            "Describe the personal data for which you want us to restrict processing. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    why_we_are_likely_to_hold_the_above_personal_data_restrict_processing: str = Field(
        default="",
        description=(
            "Explain why you believe we hold the personal data you want processing "
            'restricted for. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class ErasureRequestDetails(BaseModel):
    """Information related to a request to erase personal data"""

    personal_data_you_are_seeking_to_have_deleted: str = Field(
        default="",
        description=(
            "Describe the personal data you want us to erase. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    why_you_believe_we_should_delete_this_personal_data: str = Field(
        default="",
        description=(
            "Explain the reasons you believe this personal data should be deleted. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PortabilityRequestDetails(BaseModel):
    """Information related to a portability request for personal data"""

    details_of_the_specific_personal_data_you_seek_portability: str = Field(
        default="",
        description=(
            "Describe the specific personal data you want transferred (portability). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    why_we_are_likely_to_hold_the_above_personal_data_portability: str = Field(
        default="",
        description=(
            "Explain why you believe we hold the personal data you want transferred. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    to_whom_you_are_seeking_to_transfer_the_data: str = Field(
        default="",
        description=(
            "Identify the recipient or organization to whom you want your data transferred. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class SubjectAccessRightsRequest(BaseModel):
    """
    Subject Access Rights Request

    If you interacted with Ironshore as an EU resident up to 1/11/2020, please complete this form to submit your request and send to enquiries@hamiltongroup.com.
    """

    requester_information: RequesterInformation = Field(..., description="Requester Information")
    request_type: RequestType = Field(..., description="Request Type")
    data_protection_complaint_details: DataProtectionComplaintDetails = Field(
        ..., description="Data Protection Complaint Details"
    )
    personal_data_access_request_details: PersonalDataAccessRequestDetails = Field(
        ..., description="Personal Data Access Request Details"
    )
    correction_of_personal_data_details: CorrectionofPersonalDataDetails = Field(
        ..., description="Correction of Personal Data Details"
    )
    processing_information_inquiry_details: ProcessingInformationInquiryDetails = Field(
        ..., description="Processing Information Inquiry Details"
    )
    restrict_processing_request_details: RestrictProcessingRequestDetails = Field(
        ..., description="Restrict Processing Request Details"
    )
    erasure_request_details: ErasureRequestDetails = Field(
        ..., description="Erasure Request Details"
    )
    portability_request_details: PortabilityRequestDetails = Field(
        ..., description="Portability Request Details"
    )
