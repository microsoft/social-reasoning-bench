from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Section1DetailsofApplicant(BaseModel):
    """Basic company details, subsidiaries, acquisitions/mergers, and employee plans information for the applicant."""

    name_of_company: str = Field(
        ...,
        description=(
            'Legal name of the applicant company .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    principal_address: str = Field(
        ...,
        description=(
            "Principal business address of the company .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    website_address: str = Field(
        default="",
        description=(
            'Primary website URL of the company .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            "Main contact email address for the company .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    country_of_registration: str = Field(
        ...,
        description=(
            "Country where the company is legally registered .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_establishment: str = Field(
        ..., description="Date the company was established or incorporated"
    )  # YYYY-MM-DD format

    nature_of_business: str = Field(
        ...,
        description=(
            "Brief description of the company’s main business activities .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    are_all_subsidiaries_to_be_covered: BooleanLike = Field(
        ..., description="Indicate whether all subsidiaries are to be included in the coverage"
    )

    are_all_subsidiaries_to_be_covered_no: BooleanLike = Field(
        default="",
        description="Indicate if not all subsidiaries are to be included in the coverage",
    )

    details_of_any_acquisitions_or_mergers_since_the_last_published_accounts: str = Field(
        default="",
        description=(
            "Provide details of any acquisitions or mergers since the last published "
            'accounts .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    are_there_any_employee_plans_to_be_covered: BooleanLike = Field(
        ..., description="Indicate whether any employee plans are to be covered"
    )

    are_there_any_employee_plans_to_be_covered_no: BooleanLike = Field(
        default="", description="Indicate if no employee plans are to be covered"
    )

    confirm_pension_funds_managed_by_independent_company: BooleanLike = Field(
        default="",
        description=(
            "Confirm that all pension plan funds are managed by an independent professional "
            "investment management company"
        ),
    )

    confirm_pension_funds_managed_by_independent_company_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate that not all pension plan funds are managed by an independent "
            "professional investment management company"
        ),
    )


class GeographicSplitofOperations(BaseModel):
    """Employee counts, payroll figures, and locations by region."""

    canada_employee_count: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of employees in Canada"
    )

    canada_payroll_for_previous_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total payroll amount for the previous year in Canada"
    )

    canada_estimated_payroll_for_forthcoming_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated total payroll amount for the forthcoming year in Canada"
    )

    canada_locations: str = Field(
        default="",
        description=(
            'Locations of operations within Canada .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    uk_employee_count: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of employees in the UK"
    )

    uk_payroll_for_previous_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total payroll amount for the previous year in the UK"
    )

    uk_estimated_payroll_for_forthcoming_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated total payroll amount for the forthcoming year in the UK"
    )

    uk_locations: str = Field(
        default="",
        description=(
            'Locations of operations within the UK .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    europe_employee_count: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of employees in Europe (excluding UK if treated separately)"
    )

    europe_payroll_for_previous_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total payroll amount for the previous year in Europe"
    )

    europe_estimated_payroll_for_forthcoming_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated total payroll amount for the forthcoming year in Europe"
    )

    europe_locations: str = Field(
        default="",
        description=(
            'Locations of operations within Europe .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    usa_employee_count: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of employees in the USA"
    )

    usa_payroll_for_previous_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total payroll amount for the previous year in the USA"
    )

    usa_estimated_payroll_for_forthcoming_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated total payroll amount for the forthcoming year in the USA"
    )

    usa_locations: str = Field(
        default="",
        description=(
            "Locations of operations within the USA .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    asia_pacific_employee_count: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of employees in the Asia/Pacific region"
    )

    asia_pacific_payroll_for_previous_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total payroll amount for the previous year in the Asia/Pacific region"
    )

    asia_pacific_estimated_payroll_for_forthcoming_year: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Estimated total payroll amount for the forthcoming year in the Asia/Pacific region"
        ),
    )

    asia_pacific_locations: str = Field(
        default="",
        description=(
            "Locations of operations within the Asia/Pacific region .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_employee_count: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees in other regions not listed above"
    )

    other_payroll_for_previous_year: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Total payroll amount for the previous year in other regions not listed above",
    )

    other_estimated_payroll_for_forthcoming_year: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated total payroll amount for the forthcoming year in other regions not "
            "listed above"
        ),
    )

    other_locations: str = Field(
        default="",
        description=(
            "Locations of operations in other regions not listed above .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    total_employee_count: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of employees across all regions"
    )

    total_payroll_for_previous_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total payroll amount for the previous year across all regions"
    )

    total_estimated_payroll_for_forthcoming_year: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Estimated total payroll amount for the forthcoming year across all regions",
    )

    total_locations: str = Field(
        default="",
        description=(
            "Summary of all locations of operations across all regions .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CommercialCrimeInsuranceApplicationForm(BaseModel):
    """
        Commercial Crime Insurance
    Application Form

        Please answer all questions fully, and including all subsidiaries. If there is insufficient space, please provide further details as appropriate. Copies of the following documents should be submitted with this Application Form:
        • Latest Consolidated audited report and accounts for the Company
        • Latest interim statement (if applicable)
    """

    section_1___details_of_applicant: Section1DetailsofApplicant = Field(
        ..., description="Section 1 – Details of Applicant"
    )
    geographic_split_of_operations: GeographicSplitofOperations = Field(
        ..., description="Geographic Split of Operations"
    )
