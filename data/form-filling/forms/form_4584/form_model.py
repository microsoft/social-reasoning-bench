from pydantic import BaseModel, ConfigDict, Field


class WeriLabChainOfCustodyCocAnalysisRequest(BaseModel):
    """WERI LAB QUALITY MANAGEMENT PROGRAM Chain-of-Custody (COC) & Analysis Request

    Customers/clients submitting water samples use this form to request specific laboratory analyses from the UOG WERI Water Quality Laboratory and to document sample type, collection details, delivery method, and custody transfers. WERI lab receiving staff and analysts use it to log samples, assign lab IDs/order numbers, and confirm requested turnaround and payment; if results are nonconforming, the lab forwards the Certificate of Analysis to the Guam EPA Safe Drinking Water Program for regulatory review and follow-up decisions.
    """

    model_config = ConfigDict(extra="forbid")


    customer_client_information_bldg_permit_number: str = Field(
        ...,
        description='Building permit number (if applicable). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    sample_type_other_specify: str = Field(
        ...,
        description='Other sample type (specify). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )



    sample_information_facility_residential_name_and_location: str = Field(
        ...,
        description='Facility/residential name and location. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    sample_information_notes_instructions: str = Field(
        ...,
        description='Notes/instructions. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )



    received_by_time: str = Field(
        ...,
        description='Received by time. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    reviewed_accepted_by_weri_lab_print_sign: str = Field(
        ...,
        description='Reviewed/accepted by WERI lab (print/sign). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    payment_details_check_amount: float | None = Field(
        ..., description="Check amount"
    )
    payment_details_check_number: str = Field(
        ...,
        description='Check number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
