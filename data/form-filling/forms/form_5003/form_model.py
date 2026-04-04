from pydantic import BaseModel, ConfigDict, Field


class CapMemberHealthHistoryForm(BaseModel):
    """CAP MEMBER HEALTH HISTORY FORM

    CAP members complete this confidential health history form before a CAP special
    activity or encampment to disclose medical conditions, allergies, and any
    limitations that could affect participation. Activity/encampment staff and
    designated medical personnel review it to plan accommodations, manage risk,
    and respond appropriately in an emergency if the member cannot provide their
    own medical information.
    """

    model_config = ConfigDict(extra="forbid")

    member_grade: str = Field(
        ...,
        description='Member grade.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    member_capid_number: str = Field(
        ...,
        description='CAPID number.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    member_charter_number: str = Field(
        ...,
        description='Charter number.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    member_weight: str = Field(
        ...,
        description='Weight.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    member_eye_color: str = Field(
        ...,
        description='Eye color.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    allergies_list_and_reactions: str = Field(
        ...,
        description='Allergies and reactions details.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )



    remarks_explain_yes_answers: str = Field(
        ...,
        description='Remarks/explanations for "Yes" items.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )