from pydantic import BaseModel, ConfigDict, Field


class NoticeOfExemptionAppendixE(BaseModel):
    """Notice of Exemption (Appendix E)

    A public agency (or sometimes a project applicant) submits this California CEQA Notice of Exemption to notify the Office of Planning and Research (OPR) and the County Clerk that a specific project has been determined exempt from CEQA environmental review. The filer documents the project, location, exemption type, and the reasons the exemption applies. OPR and the County Clerk receive and record the notice for the public record and administrative tracking of CEQA exemption filings.
    """

    model_config = ConfigDict(extra="forbid")




    project_location_specific: str = Field(
        ...,
        description='Project location (specific). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    project_description_nature_purpose_beneficiaries: str = Field(
        ...,
        description='Nature, purpose, beneficiaries. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )



    reasons_project_is_exempt: str = Field(
        ...,
        description='Reasons project is exempt. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )




