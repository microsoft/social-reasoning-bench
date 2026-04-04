from pydantic import BaseModel, ConfigDict, Field


class AnimalNuisanceComplaintForm(BaseModel):
    """ANIMAL NUISANCE COMPLAINT FORM

    Residents or affected parties submit this form to report an animal-related nuisance
    (such as a barking dog or other disturbance) and provide incident details plus
    information about the animal and its owner. Local animal control or code enforcement
    staff review the submission, log it with a received date and complaint/reference
    number, and use the details to decide whether to investigate and take enforcement
    action.
    """

    model_config = ConfigDict(extra="forbid")


    complainant_phone: str = Field(
        ...,
        description='Complainant phone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    additional_complainant_1_phone: str = Field(
        ...,
        description='Additional complainant 1 phone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    additional_complainant_2_phone: str = Field(
        ...,
        description='Additional complainant 2 phone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    incident_location: str = Field(
        ...,
        description='Nuisance occurred at (location). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    incident_other_notes: str = Field(
        ...,
        description='Other notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


