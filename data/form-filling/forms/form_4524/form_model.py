from pydantic import BaseModel, ConfigDict, Field


class SeiBiobasedTestingLabAcceptanceApplication(BaseModel):
    """Application for Acceptance as an SEI Biobased Testing Laboratory

    A testing laboratory submits this application to SEI to be accepted/registered as an approved biobased testing
    laboratory eligible to perform ASTM D6866 testing in support of the USDA BioPreferred Product Certification and
    Labeling Program. SEI Biobased Certification Program staff and technical reviewers evaluate the lab’s contact
    information, organizational status, staffing, and related qualifications to decide whether to list the lab as an
    accepted testing laboratory and proceed with required agreements and compliance expectations.
    """

    model_config = ConfigDict(extra="forbid")

    applicant_info_laboratory_name: str = Field(
        ...,
        description='Laboratory name. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    applicant_info_website: str = Field(
        ...,
        description='Laboratory website. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    applicant_info_contact_first_name: str = Field(
        ...,
        description='Primary contact first name. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    applicant_info_contact_last_name: str = Field(
        ...,
        description='Primary contact last name. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    applicant_info_address_line_1: str = Field(
        ...,
        description='Address line 1. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    applicant_info_address_line_2: str = Field(
        ...,
        description='Address line 2. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    applicant_info_city: str = Field(
        ...,
        description='City. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    applicant_info_state_province: str = Field(
        ...,
        description='State or province. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    applicant_info_country: str = Field(
        ...,
        description='Country. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    applicant_info_postal_code: str = Field(
        ...,
        description='Postal code. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    applicant_info_tel_no_country_code: str = Field(
        ...,
        description='Telephone (no country code or "1"). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    applicant_info_email: str = Field(
        ...,
        description='Email address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    org_hr_organization_legal_status: str = Field(
        ...,
        description='Legal status (corp/partnership/division). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    org_hr_number_of_persons_employed: float | None = Field(
        ...,
        description="Number of persons employed",
    )