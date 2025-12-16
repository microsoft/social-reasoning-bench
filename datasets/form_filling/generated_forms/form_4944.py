from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CalculatingMeanDifferences(BaseModel):
    """Computed mean differences and percent change for carapace measurements"""

    mean_difference_cw_mm: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Calculated mean difference in carapace width (CW) between 2019 and 2020, in "
            "millimeters"
        ),
    )

    mean_difference_ch_mm: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Calculated mean difference in carapace height (CH) between 2019 and 2020, in "
            "millimeters"
        ),
    )

    mean_difference_th_mm: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Calculated mean difference in total height (TH) between 2019 and 2020, in millimeters"
        ),
    )

    percent_change_cw_mm: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Percent change in mean carapace width (CW) from 2019 to 2020"
    )

    percent_change_ch_mm: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Percent change in mean carapace height (CH) from 2019 to 2020"
    )

    percent_change_th_mm: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Percent change in mean total height (TH) from 2019 to 2020"
    )


class InterpretingYourData(BaseModel):
    """Questions interpreting megalopae size changes and extremes"""

    megalopae_size_increase_or_decrease: str = Field(
        default="",
        description=(
            "State whether overall megalopae size increased or decreased across all metrics "
            'from 2019 to 2020 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    percent_change_carapace_width_positive_or_negative: str = Field(
        default="",
        description=(
            "Describe the percent change in carapace width and indicate whether it was a "
            'positive or negative change .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    percent_change_total_height: str = Field(
        default="",
        description=(
            "Describe the percent change in total height of megalopae .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    largest_megalopae_cw: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Record the largest carapace width (CW) measured for a single megalopae",
    )

    largest_megalopae_cw_date: str = Field(
        default="", description="Date when the largest megalopae by carapace width was caught"
    )  # YYYY-MM-DD format

    largest_megalopae_th: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Record the largest total height (TH) measured for a single megalopae",
    )

    largest_megalopae_th_date: str = Field(
        default="", description="Date when the largest megalopae by total height was caught"
    )  # YYYY-MM-DD format


class ShowYourWork(BaseModel):
    """Space to show calculations"""

    show_your_work_below: str = Field(
        default="",
        description=(
            "Space to show calculations and steps used to find mean differences and percent "
            'changes .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class DiscussionQuestions(BaseModel):
    """Open-ended questions about interpretation, limitations, and future sampling"""

    inference_about_larval_populations: str = Field(
        default="",
        description=(
            "Explain what the data suggests about whether larval Dungeness populations are "
            "growing or shrinking and cite evidence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    factors_influencing_size_differences: str = Field(
        default="",
        description=(
            "List and describe possible environmental or biological factors that could "
            "affect mean size differences between years .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    sufficiency_of_sample_size_and_location: str = Field(
        default="",
        description=(
            "Discuss whether the sample size and single-location data are adequate to "
            "assess larval health and represent the region .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    modifications_to_sampling_plan: str = Field(
        default="",
        description=(
            "Describe any changes you would make to improve the sampling plan in future "
            'seasons .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class PSILightTrapLarvalDungenessCarapaceSizeCalculator(BaseModel):
    """
        Pacific Shellfish Institute (PSI) - Light Trap Data Module (Grades 6-8)
    Task 2: Calculating Larval Dungeness Carapace Size

        Pacific Shellfish Institute (PSI) - Light Trap Data Module (Grades 6-8)
        Task 2: Calculating Larval Dungeness Carapace Size
    """

    calculating_mean_differences: CalculatingMeanDifferences = Field(
        ..., description="Calculating Mean Differences"
    )
    interpreting_your_data: InterpretingYourData = Field(..., description="Interpreting Your Data")
    show_your_work: ShowYourWork = Field(..., description="Show Your Work")
    discussion_questions: DiscussionQuestions = Field(..., description="Discussion Questions")
