from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class InformationofApplicantsLaboratory(BaseModel):
    """Contact and identification details for the applicant laboratory"""

    laboratory_name: str = Field(
        ...,
        description=(
            "Full legal name of the applicant’s testing laboratory .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            "Primary website URL for the laboratory .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            "First name of the primary contact person for the laboratory .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            "Last name of the primary contact person for the laboratory .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Primary street address line for the laboratory .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_second_line: str = Field(
        default="",
        description=(
            "Second line of the street address (suite, building, etc.), if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City where the laboratory is located .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state_province: str = Field(
        ...,
        description=(
            "State or province where the laboratory is located .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    country: str = Field(
        ...,
        description=(
            "Country where the laboratory is located .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    postal_code: str = Field(..., description="Postal or ZIP code for the laboratory’s address")

    tel_please_do_not_include_country_code_or_1: str = Field(
        ...,
        description=(
            "Primary telephone number for the laboratory, without country code or leading "
            "'1' .If you cannot fill this, write \"N/A\". If this field should not be "
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            "Primary email address for communication with the laboratory .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class OrganizationandHumanResourcesoftheTestingLaboratory(BaseModel):
    """Organizational structure and staffing of the testing laboratory"""

    legal_status_of_the_testing_laboratory: str = Field(
        ...,
        description=(
            "Describe the legal status (e.g., corporation, partnership, division, "
            "subsidiary, or part of a larger corporate entity) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    number_of_persons_employed_in_the_testing_laboratory: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of staff employed in the testing laboratory"
    )


class ApplicationForAcceptanceAsAnSeiBiobasedTestingLaboratory(BaseModel):
    """
        Application for Acceptance as an SEI Biobased
    Testing Laboratory

        SEI has been awarded a contract by the U.S. Department of Agriculture (“USDA”) to provide certification services supporting the USDA’s development and administration of the BioPreferred Product Certification and Labeling Program (“the Program”).
        To be registered by SEI as an accepted biobased testing laboratory, a laboratory shall meet the following requirements:
        » Be accredited to ISO 17025 General Requirements for the Competence of Calibration and Testing Laboratory
        » Demonstrated capability to perform testing according to ASTM D6866, Standard Test Method for Determining the Biobased Content of Solid, Liquid, and Gaseous Radiocarbon Analysis
        » Willingness to comply with the SEI Practice for Documentation and Reporting of Laboratory Results for Biobased Products in accord with ASTM Test Method D6866 (Annex to the Laboratory Testing Agreement for Biobased Products)
        » Execution of the SEI Laboratory Testing Agreement
        » Laboratory shall not have direct exposure to artificial carbon-14
    """

    information_of_applicants_laboratory: InformationofApplicantsLaboratory = Field(
        ..., description="Information of Applicant’s Laboratory"
    )
    organization_and_human_resources_of_the_testing_laboratory: OrganizationandHumanResourcesoftheTestingLaboratory = Field(
        ..., description="Organization and Human Resources of the Testing Laboratory"
    )
