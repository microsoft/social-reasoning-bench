from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProfessionalDevelopment(BaseModel):
    """Major workshops, seminars, classes, internships, grants, etc. from the last five years not part of a degree program"""

    professional_development_major_workshops_seminars_classes_internships_grants_etc_in_the_last_five_years_not_part_of_a_degree_program: str = Field(
        default="",
        description=(
            "List major workshops, seminars, classes, internships, grants, etc. from the "
            "last five years that are not part of a degree program. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    professional_development_additional_entry_1: str = Field(
        default="",
        description=(
            "Additional professional development entry. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    professional_development_additional_entry_2: str = Field(
        default="",
        description=(
            "Additional professional development entry. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CocurricularActivities(BaseModel):
    """Activities the applicant is prepared to moderate or coach"""

    football: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to moderate or coach Football."
    )

    basketball: BooleanLike = Field(
        default="",
        description="Check if you are prepared to commit to moderate or coach Basketball.",
    )

    baseball: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to moderate or coach Baseball."
    )

    softball: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to moderate or coach Softball."
    )

    soccer: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to moderate or coach Soccer."
    )

    tennis: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to moderate or coach Tennis."
    )

    track: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to moderate or coach Track."
    )

    cross_country: BooleanLike = Field(
        default="",
        description="Check if you are prepared to commit to moderate or coach Cross Country.",
    )

    golf: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to moderate or coach Golf."
    )

    swimming: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to moderate or coach Swimming."
    )

    skiing: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to moderate or coach Skiing."
    )

    volleyball: BooleanLike = Field(
        default="",
        description="Check if you are prepared to commit to moderate or coach Volleyball.",
    )

    cheerleading: BooleanLike = Field(
        default="",
        description="Check if you are prepared to commit to moderate or coach Cheerleading.",
    )

    service_clubs: BooleanLike = Field(
        default="",
        description="Check if you are prepared to commit to moderate or coach Service Clubs.",
    )

    model_un: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to moderate or coach Model UN."
    )

    lacrosse: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to moderate or coach Lacrosse."
    )

    christian_service: BooleanLike = Field(
        default="",
        description="Check if you are prepared to commit to Christian Service activities.",
    )

    campus_ministry: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to Campus Ministry activities."
    )

    robotics: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to moderate or coach Robotics."
    )

    mock_trial: BooleanLike = Field(
        default="",
        description="Check if you are prepared to commit to moderate or coach Mock Trial.",
    )

    coffeehouse: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to Coffeehouse activities."
    )

    science_clubs: BooleanLike = Field(
        default="",
        description="Check if you are prepared to commit to moderate or coach Science clubs.",
    )

    diversity_programs: BooleanLike = Field(
        default="", description="Check if you are prepared to commit to Diversity programs."
    )

    other_specify: str = Field(
        default="",
        description=(
            "Specify any other activity you are prepared to commit to moderate or coach. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class References(BaseModel):
    """Contact information for three references"""

    reference_1_name: str = Field(
        default="",
        description=(
            'Name of first reference. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    reference_1_email_address_and_telephone: str = Field(
        default="",
        description=(
            "Email address and telephone number of first reference. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_relationship: str = Field(
        default="",
        description=(
            "Relationship of first reference to you. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_name: str = Field(
        default="",
        description=(
            'Name of second reference. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    reference_2_email_address_and_telephone: str = Field(
        default="",
        description=(
            "Email address and telephone number of second reference. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_relationship: str = Field(
        default="",
        description=(
            "Relationship of second reference to you. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_3_name: str = Field(
        default="",
        description=(
            'Name of third reference. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    reference_3_email_address_and_telephone: str = Field(
        default="",
        description=(
            "Email address and telephone number of third reference. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_3_relationship: str = Field(
        default="",
        description=(
            "Relationship of third reference to you. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Certification(BaseModel):
    """Applicant certification of accuracy of information"""

    signature: str = Field(
        default="",
        description=(
            "Applicant's signature certifying that the information in the application is "
            'accurate and complete. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        default="", description="Date the application is signed."
    )  # YYYY-MM-DD format


class ProfessionalDevelopment(BaseModel):
    """
    Professional Development

    List major workshops, seminars, classes, internships, grants, etc., in which you have participated in the last five years which are not normally part of a degree program. (Do not include single meetings, conventions, etc.)
    What activities are you prepared to commit to moderate or coach at Jesuit High School?
    Provide the name, email address, and telephone number of three persons (other than those who have written letters of recommendation) able to give information about your qualifications for the position for which you are applying.
    Your answers to the following questions will provide us with information as to the ways you believe you can contribute to Jesuit High School. Upload a separate document with your application including the following questions with your responses.
    """

    professional_development: ProfessionalDevelopment = Field(
        ..., description="Professional Development"
    )
    co_curricular_activities: CocurricularActivities = Field(
        ..., description="Co-curricular Activities"
    )
    references: References = Field(..., description="References")
    certification: Certification = Field(..., description="Certification")
