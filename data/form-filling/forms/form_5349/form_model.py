from pydantic import BaseModel, ConfigDict, Field


class PersonalLinesQuoteSheet(BaseModel):
    """Personal Lines Quote Sheet

    Agency staff submit this quote request sheet to RT Specialty/Ryan Turner personal lines underwriting to gather applicant, property, loss history, and coverage details for homeowners/dwelling/condo/builders risk risks. Underwriters review the information to assess eligibility, evaluate exposures and prior losses, and decide what terms, limits, deductibles, and premium quotes can be offered.
    """

    model_config = ConfigDict(extra="forbid")


    insured_information_phone: str = Field(
        ...,
        description='Insured phone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    premises_if_rental_description: str = Field(
        ...,
        description='If rental description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    premises_weeks_rented_annually: float | None = Field(
        ...,
        description="Weeks rented annually",
    )


    premises_construction_type: str = Field(
        ...,
        description='Construction type. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    premises_protection_class: str = Field(
        ...,
        description='Protection class. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    premises_heating_type: str = Field(
        ...,
        description='Heating type. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    premises_describe_renovations: str = Field(
        ...,
        description='Describe renovations. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    vacant_only_how_long_vacant: str = Field(
        ...,
        description='How long vacant. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    vacant_only_intended_use_of_building: str = Field(
        ...,
        description='Intended use of building. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )







    additional_information_for_underwriting: str = Field(
        ...,
        description='Additional underwriting info. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )