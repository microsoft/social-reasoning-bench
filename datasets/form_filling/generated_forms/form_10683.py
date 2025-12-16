from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Consent(BaseModel):
    """Permission to disclose information to the supplier"""

    disclose_information_yes: BooleanLike = Field(
        ...,
        description=(
            "Select YES to allow your information to be shared with your supplier to help "
            "resolve the issues."
        ),
    )

    disclose_information_no: BooleanLike = Field(
        ...,
        description="Select NO if you do not want your information to be shared with your supplier.",
    )


class PartAGeneraldetails(BaseModel):
    """General details about the holding and identification products"""

    cph_number: str = Field(
        ...,
        description=(
            "CPH (County Parish Holding) number, including all segments. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    name: str = Field(
        ...,
        description=(
            "Name of the person completing the form. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    herd_flock_mark: str = Field(
        default="",
        description=(
            "Herd or flock mark associated with the animals concerned. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    manufacturer_name: str = Field(
        ...,
        description=(
            "Full name of the manufacturer of the ear tag, pastern or bolus. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    product_name: str = Field(
        ...,
        description=(
            "Product name or model of the ear tag, pastern or bolus. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    type_of_ear_tag: Literal["Primary", "Secondary", "Other/Not specified", "N/A", ""] = Field(
        default="", description="Indicate whether the ear tag is a primary or secondary tag."
    )

    welfare_issue: BooleanLike = Field(
        default="", description="Tick if there is a welfare issue such as lesions or infection."
    )

    performance_issue: BooleanLike = Field(
        default="",
        description="Tick if there is a performance issue such as breakage or high loss rate.",
    )

    ear_tag_position_cattle: str = Field(
        default="",
        description=(
            "Indicate or mark the position of the ear tag on the cattle figure. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    ear_tag_position_sheep_goat: str = Field(
        default="",
        description=(
            "Indicate or mark the position of the ear tag on the sheep/goat figure. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    details_of_findings: str = Field(
        ...,
        description=(
            "Provide full details of your findings, including timing of "
            "attachment/ingestion, number of losses, breakages, readability, and any other "
            'relevant information. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class EarTagPasternAndBolusFeedbackForm(BaseModel):
    """
    Ear tag Pastern and Bolus feedback form

    This form should be used to report any complaints you have with the tags, pastern or bolus (for example - infection, losses, performance, breakages, legibility etc). You may also use it to report any positive comments you have. It is also advisable to contact your ear tag, pastern or bolus manufacturer who may be able to resolve your issue.
    """

    consent: Consent = Field(..., description="Consent")
    part_a___general_details: PartAGeneraldetails = Field(
        ..., description="Part A – General details"
    )
