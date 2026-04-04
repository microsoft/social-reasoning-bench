from pydantic import BaseModel, ConfigDict, Field


class NoticeOfExemptionAppendixE(BaseModel):
    """Notice of Exemption (Appendix E)

    A California public agency (or sometimes a project applicant) submits this CEQA Notice of Exemption to the Office of Planning and Research and the County Clerk to publicly record that a project has been approved and determined exempt from environmental review. OPR and the County Clerk file and post the notice for administrative tracking and public notice; the information is used to document the project, the exemption basis, and key contacts and signatures supporting the exemption determination.
    """

    model_config = ConfigDict(extra="forbid")




    project_location_specific: str = Field(
        ...,
        description='Project location specific address/description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    project_description_nature_purpose_beneficiaries: str = Field(
        ...,
        description='Nature, purpose, beneficiaries description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    exempt_status_categorical_type_and_section: str = Field(
        ...,
        description='Categorical type and section number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    reasons_project_is_exempt: str = Field(
        ...,
        description='Reasons project is exempt. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )



