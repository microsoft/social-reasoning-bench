from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MilitaryStopoverRouteTableRow(BaseModel):
    """Single row in TAS / DEP. PT / ETD / ALTITUDE / ROUTE OF FLIGHT / DESTINATION / ETE / REMARKS (table)"""

    tas: str = Field(default="", description="Tas")
    dep_pt: str = Field(default="", description="Dep_Pt")
    etd: str = Field(default="", description="Etd")
    altitude: str = Field(default="", description="Altitude")
    route_of_flight: str = Field(default="", description="Route_Of_Flight")
    destination: str = Field(default="", description="Destination")
    ete: str = Field(default="", description="Ete")
    remarks: str = Field(default="", description="Remarks")


class FormUseOnly(BaseModel):
    """For specialist use when providing pilot briefing or VNR and recording stopover details"""

    pilot_briefing: BooleanLike = Field(
        default="", description="Check if this form is being used for a pilot briefing"
    )

    vnr: BooleanLike = Field(
        default="", description="Check if this is a VNR (visual no-radio) briefing"
    )

    time_started: str = Field(
        default="",
        description=(
            "Time the briefing or form processing was started .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    stopover: BooleanLike = Field(default="", description="Check if this is a stopover briefing")

    specialist_initials: str = Field(
        default="",
        description=(
            "Initials of the specialist handling the briefing .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FlightPlan(BaseModel):
    """Primary civil flight plan information (FAA Form 7233-1 main section)"""

    type_vfr: BooleanLike = Field(..., description="Check if the flight plan type is VFR")

    type_ifr: BooleanLike = Field(..., description="Check if the flight plan type is IFR")

    type_dvfr: BooleanLike = Field(..., description="Check if the flight plan type is DVFR")

    aircraft_identification: str = Field(
        ...,
        description=(
            "Aircraft tail number or identification code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    aircraft_type_special_equipment: str = Field(
        ...,
        description=(
            "Aircraft type and any special equipment codes .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    true_airspeed: Union[float, Literal["N/A", ""]] = Field(
        ..., description="True airspeed in knots"
    )

    departure_point: str = Field(
        ...,
        description=(
            'Departure airport identifier or name .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    departure_time_proposed_z: str = Field(
        ...,
        description=(
            'Proposed departure time in Zulu (UTC) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    departure_time_actual_z: str = Field(
        default="",
        description=(
            'Actual departure time in Zulu (UTC) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    cruising_altitude: str = Field(
        ...,
        description=(
            "Planned cruising altitude or flight level .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    route_of_flight: str = Field(
        ...,
        description=(
            "Planned route of flight, including fixes and airways .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    destination_name_of_airport_and_city: str = Field(
        ...,
        description=(
            'Destination airport name and city .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    est_time_enroute_hours: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated time enroute in whole hours"
    )

    est_time_enroute_minutes: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated time enroute in minutes"
    )

    remarks: str = Field(
        default="",
        description=(
            "Additional information or special instructions .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    fuel_on_board_hours: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Fuel on board expressed in hours"
    )

    fuel_on_board_minutes: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Fuel on board expressed in minutes"
    )

    alternate_airports: str = Field(
        default="",
        description=(
            'Planned alternate airport or airports .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    pilots_name_address_telephone_aircraft_home_base: str = Field(
        ...,
        description=(
            "Pilot’s full name, address, phone number, and aircraft home base .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    number_aboard: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of persons on board"
    )

    color_of_aircraft: str = Field(
        ...,
        description=(
            "Primary color or colors of the aircraft .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    close_vfr_flight_plan_with_fss_on_arrival: str = Field(
        default="",
        description=(
            "Name or identifier of FSS to close VFR flight plan with on arrival .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class MilitaryStopoverFAAUseOnly(BaseModel):
    """Military stopover flight plan segment and route table (FAA use only)"""

    military_stopover_type_ifr: BooleanLike = Field(
        default="", description="For military stopover section, check if IFR"
    )

    military_stopover_type_vfr: BooleanLike = Field(
        default="", description="For military stopover section, check if VFR"
    )

    military_stopover_aircraft_identification: str = Field(
        default="",
        description=(
            "Aircraft identification for the military stopover segment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    military_stopover_aircraft_type_special_equipment: str = Field(
        default="",
        description=(
            "Aircraft type and special equipment for the military stopover segment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    military_stopover_remarks: str = Field(
        default="",
        description=(
            "Remarks related to the military stopover .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    military_stopover_departure_point: str = Field(
        default="",
        description=(
            "Departure point for the military stopover segment .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    military_stopover_destination: str = Field(
        default="",
        description=(
            "Destination for the military stopover segment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    military_stopover_eta: str = Field(
        default="",
        description=(
            "Estimated time of arrival for the military stopover segment .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    military_stopover_route_table: List[MilitaryStopoverRouteTableRow] = Field(
        default="",
        description=(
            "Table for multiple legs of the military stopover route, including TAS, "
            "departure point, ETD, altitude, route, destination, ETE, and remarks"
        ),
    )  # List of table rows

    tas_table_column: str = Field(
        default="",
        description=(
            'Table column header for true airspeed .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    dep_pt_table_column: str = Field(
        default="",
        description=(
            "Table column header for departure point .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    etd_table_column: str = Field(
        default="",
        description=(
            "Table column header for estimated time of departure .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    altitude_table_column: str = Field(
        default="",
        description=(
            'Table column header for altitude .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    route_of_flight_table_column: str = Field(
        default="",
        description=(
            "Table column header for route of flight .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    destination_table_column: str = Field(
        default="",
        description=(
            'Table column header for destination .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    ete_table_column: str = Field(
        default="",
        description=(
            "Table column header for estimated time enroute .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    remarks_table_column: str = Field(
        default="",
        description=(
            'Table column header for remarks .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    kts_row_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="True airspeed in knots for first table row"
    )

    kts_row_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="True airspeed in knots for second table row"
    )

    kts_row_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="True airspeed in knots for third table row"
    )

    kts_row_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="True airspeed in knots for fourth table row"
    )

    remarks_final_section: str = Field(
        default="",
        description=(
            "Additional remarks for the military stopover section .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    initials: str = Field(
        default="",
        description=(
            "Initials of the person completing the military stopover section .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class UsDepartmentOfTransportationFederalAviationAdministration(BaseModel):
    """
        U.S. DEPARTMENT OF TRANSPORTATION
    FEDERAL AVIATION ADMINISTRATION

        This statement is provided pursuant to the Privacy Act of 1974, 5 USC § 552a. The authority for collecting this information is contained in 49 U.S.C. §§ 40113, 44702, 44703, 44709, and 14 C.F.R. Part 1 - Part 61, 65, or 67. The principal purpose for which the information is intended to be used is to allow you to submit your flight plan. Submission of the data is voluntary. Failure to provide all required information may result in you not being able to submit your flight plan. The information collected on this form will be included in a Privacy Act System of Records known as DOT/FAA 847, titled "Aviation Records on Individuals" and will be subject to the routine uses published in the System of Records Notice (SORN) for DOT/FAA 847 (see www.dot.gov/privacy/privacyactnotices).
    """

    form_use_only: FormUseOnly = Field(..., description="Form Use Only")
    flight_plan: FlightPlan = Field(..., description="Flight Plan")
    military_stopover_faa_use_only: MilitaryStopoverFAAUseOnly = Field(
        ..., description="Military Stopover (FAA Use Only)"
    )
