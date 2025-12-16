from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ReferencesTableRow(BaseModel):
    """Single row in Reference Name"""

    reference_name: str = Field(default="", description="Reference_Name")
    title: str = Field(default="", description="Title")
    phone_number_e_mail_address: str = Field(default="", description="Phone_Number_E_Mail_Address")


class SitePreferences(BaseModel):
    """Preferred Carewest locations for volunteering"""

    carewest_administration_southport_tower: BooleanLike = Field(
        default="",
        description="Select if you prefer the Carewest Administration (Southport Tower) site.",
    )

    carewest_beddington: BooleanLike = Field(
        default="", description="Select if you prefer the Carewest Beddington site."
    )

    carewest_colonel_belcher: BooleanLike = Field(
        default="", description="Select if you prefer the Carewest Colonel Belcher site."
    )

    carewest_dr_vernon_fanning_centre: BooleanLike = Field(
        default="", description="Select if you prefer the Carewest Dr. Vernon Fanning Centre site."
    )

    carewest_garrison_green: BooleanLike = Field(
        default="", description="Select if you prefer the Carewest Garrison Green site."
    )

    carewest_george_boyack: BooleanLike = Field(
        default="", description="Select if you prefer the Carewest George Boyack site."
    )

    carewest_glenmore_park: BooleanLike = Field(
        default="", description="Select if you prefer the Carewest Glenmore Park site."
    )

    carewest_nickle_house: BooleanLike = Field(
        default="", description="Select if you prefer the Carewest Nickle House site."
    )

    carewest_osi: BooleanLike = Field(
        default="", description="Select if you prefer the Carewest OSI site."
    )

    carewest_rouleau_manor: BooleanLike = Field(
        default="", description="Select if you prefer the Carewest Rouleau Manor site."
    )

    carewest_royal_park: BooleanLike = Field(
        default="", description="Select if you prefer the Carewest Royal Park site."
    )

    carewest_sarcee: BooleanLike = Field(
        default="", description="Select if you prefer the Carewest Sarcee site."
    )

    carewest_signal_pointe: BooleanLike = Field(
        default="", description="Select if you prefer the Carewest Signal Pointe site."
    )

    no_preference: BooleanLike = Field(
        default="", description="Select if you have no preference for volunteer site."
    )


class BackgroundInformation(BaseModel):
    """Previous volunteering/employment and how you heard about Carewest"""

    previously_volunteered_yes: BooleanLike = Field(
        default="", description="Check YES if you have previously volunteered at Carewest."
    )

    previously_volunteered_no: BooleanLike = Field(
        default="", description="Check NO if you have not previously volunteered at Carewest."
    )

    last_volunteer_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year you last volunteered at Carewest."
    )

    current_employee_yes: BooleanLike = Field(
        default="", description="Check YES if you are currently employed by Carewest."
    )

    current_employee_no: BooleanLike = Field(
        default="", description="Check NO if you are not currently employed by Carewest."
    )

    previously_employed_yes: BooleanLike = Field(
        default="", description="Check YES if you have previously been employed by Carewest."
    )

    previously_employed_no: BooleanLike = Field(
        default="", description="Check NO if you have not previously been employed by Carewest."
    )

    year_of_termination: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year your employment with Carewest ended."
    )

    carewest_website: BooleanLike = Field(
        default="", description="Select if you heard about Carewest from the Carewest website."
    )

    other_where_you_saw_opportunity: str = Field(
        default="",
        description=(
            "If other, describe where you saw this volunteer opportunity. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class Experience(BaseModel):
    """Description of volunteer and work experience"""

    experience_description: str = Field(
        default="",
        description=(
            "Brief description of your current and previous volunteer and work experience "
            'and any additional information. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class References(BaseModel):
    """Reference contact information"""

    references_table: List[ReferencesTableRow] = Field(
        default="",
        description=(
            "Contact information for your references, including name, title, and phone "
            "number or email address."
        ),
    )  # List of table rows


class DeclarationandAttachments(BaseModel):
    """Signature, date, and resume attachment"""

    applicants_signature: str = Field(
        ...,
        description=(
            "Signature of the applicant confirming the information provided. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    signature_date: str = Field(
        ..., description="Date the application form is signed."
    )  # YYYY-MM-DD format

    attached_resume_yes: BooleanLike = Field(
        default="", description="Check YES if you attached a resume or additional information."
    )

    attached_resume_no: BooleanLike = Field(
        default="", description="Check NO if you did not attach a resume or additional information."
    )


class CarewestVolunteerApplicationForm(BaseModel):
    """
    Carewest Volunteer Application Form

    The personal information on this form will only be collected and shared for purposes outlined in the Freedom of Information and Protection of Privacy Act and Health Information Act which includes: determining eligibility for employment; determining eligibility for Carewest programs and services; for programs designed to evaluate and improve Carewest programs and services; for the operation of approved Carewest education and research programs and services; and for legal requirements where these purposes are consistent with the FOIPP and HIA Act and under the Alberta Labour Relations and Employment Standards Codes. If you have any questions regarding the collection of information you may contact the Carewest Manager of Information Management & Privacy, 722 - 16 Avenue NE, Calgary, AB T2E 6V7.
    """

    site_preferences: SitePreferences = Field(..., description="Site Preferences")
    background_information: BackgroundInformation = Field(..., description="Background Information")
    experience: Experience = Field(..., description="Experience")
    references: References = Field(..., description="References")
    declaration_and_attachments: DeclarationandAttachments = Field(
        ..., description="Declaration and Attachments"
    )
