from pydantic import BaseModel, ConfigDict, Field


class NoticeOfExemptionFormD(BaseModel):
    """Notice of Exemption (Form D)

    A public agency (or an applicant, when applicable) submits this Notice of Exemption to document that a proposed project is exempt from environmental review under CEQA. It is filed with the California Office of Planning and Research and/or the County Clerk in the county where the project is located. These offices and other reviewers use it to record the project details, the exemption basis, and the responsible contacts, and to track the exemption determination and filing status.
    """

    model_config = ConfigDict(extra="forbid")




    project_location_specific: str = Field(
        ...,
        description='Project location specific. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    project_description: str = Field(
        ...,
        description='Project description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )



    exemption_reasons: str = Field(
        ...,
        description='Reasons project is exempt. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )




