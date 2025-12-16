from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CadetInformation(BaseModel):
    """Basic information about the cadet"""

    cadet_legal_name: str = Field(
        ...,
        description=(
            'Cadet\'s full legal name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Cadet's date of birth")  # YYYY-MM-DD format


class MedicalExemptionDetails(BaseModel):
    """Details of the medical contraindication to COVID-19 vaccination"""

    contraindication_explanation: str = Field(
        ...,
        description=(
            "Detailed explanation of why the COVID-19 vaccine is contraindicated for this "
            'cadet .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    permanent: BooleanLike = Field(..., description="Check if the contraindication is permanent")

    temporary: BooleanLike = Field(..., description="Check if the contraindication is temporary")

    expected_to_preclude_immunizations_until: str = Field(
        default="",
        description="Date until which the contraindication is expected to prevent immunization",
    )  # YYYY-MM-DD format

    provider_section_date: str = Field(
        default="", description="Date this medical exemption form is completed by the provider"
    )  # YYYY-MM-DD format


class HealthCareProviderInformation(BaseModel):
    """Information and certification from the health care provider"""

    medical_provider_health_department_official_print_name: str = Field(
        ...,
        description=(
            "Printed name of the medical provider or health department official completing "
            'this form .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the medical provider or health department official .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    signature_date: str = Field(
        ..., description="Date the provider or official signed the form"
    )  # YYYY-MM-DD format

    address: str = Field(
        ...,
        description=(
            "Mailing address of the medical provider or health department office .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Phone number for the medical provider or health department office .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class VMI2021InfirmaryCovid19VaccineExemptionRequest(BaseModel):
    """
        VIRGINIA MILITARY INSTITUTE

    2021-22 Academic Year

    Infirmary

    Request for medical exemption related to COVID-19 vaccine

        Request for medical exemption related to COVID-19 vaccine
    """

    cadet_information: CadetInformation = Field(..., description="Cadet Information")
    medical_exemption_details: MedicalExemptionDetails = Field(
        ..., description="Medical Exemption Details"
    )
    health_care_provider_information: HealthCareProviderInformation = Field(
        ..., description="Health Care Provider Information"
    )
