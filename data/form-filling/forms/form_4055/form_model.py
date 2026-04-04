from pydantic import BaseModel, ConfigDict, Field


class ChainOfCustodyAnalysisRequestForm(BaseModel):
    """Chain-of-Custody / Analysis Request Form

    Field staff or clients submit this form with environmental samples to document who collected and handled the samples, where they came from, and what laboratory analyses and turnaround time are requested. ACM Engineering & Environmental Services’ lab staff and project administrators use it to verify sample condition and custody, assign a laboratory project ID, and determine which tests to perform and how quickly to report results.
    """

    model_config = ConfigDict(extra="forbid")

    acm_project_number: str = Field(
        ...,
        description='ACM project number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    client_contact_site_phone: str = Field(
        ...,
        description='Contact phone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    client_contact_site_reference_number: str = Field(
        ...,
        description='Reference number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )



    comments: str = Field(
        ...,
        description='Comments. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    requested_analysis_other_specify: str = Field(
        ...,
        description='Other analysis specify. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    custody_submitted_relinquished_by: str = Field(
        ...,
        description='Submitted/relinquished by name. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    custody_received_accepted_by: str = Field(
        ...,
        description='Received/accepted by name. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )