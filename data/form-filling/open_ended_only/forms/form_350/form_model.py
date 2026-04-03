from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ExemptionSelection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Select the type of exemption being requested"""

    exemption_for_certain_illegal_divisions_of_land: Literal["Unimproved ($1100)", "Improved with Valid County Occupancy Approval ($300)", "Improved without Proper County Occupancy Approval ($500)", "N/A", ""] = Field(
        ...,
        description="Select the type of exemption for the property"
    )


class OwnerInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the property owner(s)"""

    owners: str = Field(
        ...,
        description=(
            "Full legal name(s) of the property owner(s) .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    mailing_address: str = Field(
        ...,
        description=(
            "Mailing address of the owner(s) .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    city: str = Field(
        ...,
        description=(
            "City of the owner's mailing address .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    state: str = Field(
        ...,
        description="State of the owner's mailing address"
    )

    zip: str = Field(
        ...,
        description="Zip code of the owner's mailing address"
    )

    email_address: str = Field(
        ...,
        description=(
            "Email address of the owner(s) .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    home_phone: str = Field(
        ...,
        description=(
            "Home phone number of the owner(s) .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    work_phone: str = Field(
        ...,
        description=(
            "Work phone number of the owner(s) .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class ApplicantInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the applicant(s), if different from owner(s)"""

    applicants: str = Field(
        ...,
        description=(
            "Full legal name(s) of the applicant(s), if different from owner(s) .If you "
            "cannot fill this, write \"N/A\". If this field should not be filled by you "
            "(for example, it belongs to another person or office), leave it blank (empty "
            "string \"\")."
        )
    )

    mailing_address_applicant: str = Field(
        ...,
        description=(
            "Mailing address of the applicant(s) .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    city_applicant: str = Field(
        ...,
        description=(
            "City of the applicant's mailing address .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    state_applicant: str = Field(
        ...,
        description="State of the applicant's mailing address"
    )

    zip_applicant: str = Field(
        ...,
        description="Zip code of the applicant's mailing address"
    )

    email_address_applicant: str = Field(
        ...,
        description=(
            "Email address of the applicant(s) .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    home_phone_applicant: str = Field(
        ...,
        description=(
            "Home phone number of the applicant(s) .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    work_phone_applicant: str = Field(
        ...,
        description=(
            "Work phone number of the applicant(s) .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class PropertyInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details about the property and lots involved in the request"""

    legal_description_of_property: str = Field(
        ...,
        description=(
            "Legal description of the property (e.g., section, township, range, "
            "subdivision, lot, block) .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    parcel_identification_number_pin: str = Field(
        ...,
        description=(
            "Parcel Identification Number (PIN) for the property .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    current_number_of_lots: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current number of lots"
    )

    acreage_of_each_current: str = Field(
        ...,
        description=(
            "Acreage of each current lot .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    number_of_lots_proposed_for_legalization: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of lots proposed for legalization"
    )

    acreage_of_each_proposed: str = Field(
        ...,
        description=(
            "Acreage of each proposed lot .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )


class RequestDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Reason for the exemption request"""

    describe_reason_for_request: str = Field(
        ...,
        description=(
            "Describe the reason for this request .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class Signatures(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Signatures of owners and applicants"""

    owners_signature: str = Field(
        ...,
        description=(
            "Signature of owner(s) .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    date_owner_signature_1: str = Field(
        ...,
        description="Date of owner signature"
    )  # YYYY-MM-DD format

    owners_signature_2: str = Field(
        ...,
        description=(
            "Signature of second owner (if applicable) .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    date_owner_signature_2: str = Field(
        ...,
        description="Date of second owner signature"
    )  # YYYY-MM-DD format

    applicants_signature: str = Field(
        ...,
        description=(
            "Signature of applicant(s) .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    date_applicant_signature: str = Field(
        ...,
        description="Date of applicant signature"
    )  # YYYY-MM-DD format


class ExemptionForCertainIllegalDivisionsOfLand(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    Exemption for Certain Illegal Divisions of Land

    Exemption for Certain Illegal Divisions of Land application form for Clear Creek County Planning Department. This form is used to request legalization of certain land divisions that were previously considered illegal, with options for unimproved or improved properties. It collects owner and applicant information, property details, and the reason for the exemption request, and includes required fees for processing and creating vested property rights.
    """

    exemption_selection: ExemptionSelection = Field(
        ...,
        description="Exemption Selection"
    )
    owner_information: OwnerInformation = Field(
        ...,
        description="Owner Information"
    )
    applicant_information: ApplicantInformation = Field(
        ...,
        description="Applicant Information"
    )
    property_information: PropertyInformation = Field(
        ...,
        description="Property Information"
    )
    request_details: RequestDetails = Field(
        ...,
        description="Request Details"
    )
    signatures: Signatures = Field(
        ...,
        description="Signatures"
    )