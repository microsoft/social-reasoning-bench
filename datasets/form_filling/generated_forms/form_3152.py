from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class HumanInfluences(BaseModel):
    """
    Human Influences

    Humans tend to change the natural environment for their use. Some changes can affect the surfaces of earth and the composition of the atmosphere, and therefore, the energy balance. Many people are advocating for more care of our natural resources to reduce human impacts on the environment.
    """

    cutting_down_forests: str = Field(
        default="",
        description=(
            "Explain how cutting down forests might affect the earth's energy balance. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    using_energy_sources_like_wind_water_and_solar_energy: str = Field(
        default="",
        description=(
            "Describe how using renewable energy sources like wind, water, and solar might "
            'affect the earth\'s energy balance. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    producing_more_efficient_cars_and_trucks: str = Field(
        default="",
        description=(
            "Describe how producing more efficient cars and trucks might affect the earth's "
            'energy balance. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    burning_more_fossil_fuels: str = Field(
        default="",
        description=(
            "Explain how burning more fossil fuels might affect the earth's energy balance. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    constructing_more_buildings_roads_and_parking_lots: str = Field(
        default="",
        description=(
            "Explain how constructing more buildings, roads, and parking lots might affect "
            'the earth\'s energy balance. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    planting_more_trees_and_creating_more_green_space: str = Field(
        default="",
        description=(
            "Describe how planting more trees and creating more green space might affect "
            'the earth\'s energy balance. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    recycling: str = Field(
        default="",
        description=(
            "Explain how recycling might affect the earth's energy balance. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )
