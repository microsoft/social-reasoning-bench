from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectLeadAgencyInformation(BaseModel):
    """Basic project identification and lead agency contact details"""

    sch_number: str = Field(
        default="",
        description=(
            "State Clearinghouse identification number, if already assigned .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    project_title: str = Field(
        ...,
        description=(
            'Official title of the project .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    lead_agency: str = Field(
        ...,
        description=(
            "Name of the lead agency responsible for the project .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_person: str = Field(
        ...,
        description=(
            "Primary contact person at the lead agency .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            'Mailing address of the lead agency .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Telephone number for the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City of the lead agency mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    zip: str = Field(..., description="ZIP code of the lead agency mailing address")

    county: str = Field(
        ...,
        description=(
            "County of the lead agency mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectLocation(BaseModel):
    """Geographic location and nearby features"""

    project_location_county: str = Field(
        ...,
        description=(
            'County where the project is located .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    project_location_city_nearest_community: str = Field(
        ...,
        description=(
            "City or nearest community to the project location .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cross_streets: str = Field(
        default="",
        description=(
            "Major cross streets near the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    project_location_zip_code: str = Field(
        default="", description="ZIP code of the project location"
    )

    longitude_n_degrees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Latitude degrees (north) of the project location"
    )

    longitude_n_minutes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Latitude minutes (north) of the project location"
    )

    longitude_n_seconds: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Latitude seconds (north) of the project location"
    )

    longitude_w_degrees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Longitude degrees (west) of the project location"
    )

    longitude_w_minutes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Longitude minutes (west) of the project location"
    )

    longitude_w_seconds: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Longitude seconds (west) of the project location"
    )

    total_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total acreage of the project site"
    )

    assessors_parcel_no: str = Field(
        default="",
        description=(
            "Assessor’s parcel number(s) for the project site .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    section: str = Field(
        default="",
        description=(
            "Survey section for the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    twp: str = Field(
        default="",
        description=(
            "Township designation for the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    range: str = Field(
        default="",
        description=(
            "Range designation for the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    base: str = Field(
        default="",
        description=(
            "Base meridian for the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_state_hwy_number: str = Field(
        default="",
        description=(
            "State highway numbers within 2 miles of the project .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_waterways: str = Field(
        default="",
        description=(
            "Waterways within 2 miles of the project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_airports: str = Field(
        default="",
        description=(
            "Airports within 2 miles of the project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_railways: str = Field(
        default="",
        description=(
            "Railways within 2 miles of the project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_schools: str = Field(
        default="",
        description=(
            'Schools within 2 miles of the project .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class DocumentType(BaseModel):
    """Type of environmental document under CEQA/NEPA and related options"""

    ceqa_nop: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Notice of Preparation (NOP)"
    )

    ceqa_early_cons: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Early Consultation"
    )

    ceqa_neg_dec: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Negative Declaration"
    )

    ceqa_mit_neg_dec: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Mitigated Negative Declaration"
    )

    ceqa_draft_eir: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Draft EIR"
    )

    ceqa_supplement_subsequent_eir: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Supplement or Subsequent EIR"
    )

    ceqa_prior_sch_no: str = Field(
        default="",
        description=(
            "Prior State Clearinghouse number for related CEQA documents .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    ceqa_other: str = Field(
        default="",
        description=(
            "Description if CEQA document type is other than listed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    nepa_noi: BooleanLike = Field(
        default="", description="Check if the NEPA document type is Notice of Intent (NOI)"
    )

    nepa_ea: BooleanLike = Field(
        default="", description="Check if the NEPA document type is Environmental Assessment (EA)"
    )

    nepa_draft_eis: BooleanLike = Field(
        default="",
        description=(
            "Check if the NEPA document type is Draft Environmental Impact Statement (Draft EIS)"
        ),
    )

    nepa_fonsi: BooleanLike = Field(
        default="",
        description="Check if the NEPA document type is Finding of No Significant Impact (FONSI)",
    )

    other_joint_document: BooleanLike = Field(
        default="", description="Check if this is a joint CEQA/NEPA or similar combined document"
    )

    other_final_document: BooleanLike = Field(
        default="", description="Check if this is a final environmental document"
    )

    other_other: str = Field(
        default="",
        description=(
            "Description if the document type is another category .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LocalActionType(BaseModel):
    """Local planning and permitting actions associated with the project"""

    local_action_general_plan_update: BooleanLike = Field(
        default="", description="Check if the local action includes a General Plan Update"
    )

    local_action_general_plan_amendment: BooleanLike = Field(
        default="", description="Check if the local action includes a General Plan Amendment"
    )

    local_action_general_plan_element: BooleanLike = Field(
        default="", description="Check if the local action includes a General Plan Element"
    )

    local_action_community_plan: BooleanLike = Field(
        default="", description="Check if the local action includes a Community Plan"
    )

    local_action_specific_plan: BooleanLike = Field(
        default="", description="Check if the local action includes a Specific Plan"
    )

    local_action_master_plan: BooleanLike = Field(
        default="", description="Check if the local action includes a Master Plan"
    )

    local_action_planned_unit_development: BooleanLike = Field(
        default="", description="Check if the local action includes a Planned Unit Development"
    )

    local_action_site_plan: BooleanLike = Field(
        default="", description="Check if the local action includes a Site Plan"
    )

    local_action_rezone: BooleanLike = Field(
        default="", description="Check if the local action includes a Rezone"
    )

    local_action_prezone: BooleanLike = Field(
        default="", description="Check if the local action includes a Prezone"
    )

    local_action_use_permit: BooleanLike = Field(
        default="", description="Check if the local action includes a Use Permit"
    )

    local_action_land_division: BooleanLike = Field(
        default="",
        description="Check if the local action includes a land division such as a subdivision",
    )

    local_action_annexation: BooleanLike = Field(
        default="", description="Check if the local action includes an Annexation"
    )

    local_action_redevelopment: BooleanLike = Field(
        default="", description="Check if the local action includes Redevelopment"
    )

    local_action_coastal_permit: BooleanLike = Field(
        default="", description="Check if the local action includes a Coastal Permit"
    )

    local_action_other: str = Field(
        default="",
        description=(
            "Description if the local action type is other than listed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class DevelopmentType(BaseModel):
    """Nature and scale of proposed development"""

    development_residential: BooleanLike = Field(
        default="", description="Check if the project includes residential development"
    )

    residential_units: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of residential units proposed"
    )

    residential_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of residential development"
    )

    development_office: BooleanLike = Field(
        default="", description="Check if the project includes office development"
    )

    office_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of office space"
    )

    office_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of office development"
    )

    office_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with office development"
    )

    development_commercial: BooleanLike = Field(
        default="", description="Check if the project includes commercial development"
    )

    commercial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of commercial space"
    )

    commercial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of commercial development"
    )

    commercial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with commercial development"
    )

    development_industrial: BooleanLike = Field(
        default="", description="Check if the project includes industrial development"
    )

    industrial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of industrial space"
    )

    industrial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of industrial development"
    )

    industrial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with industrial development"
    )

    development_educational: BooleanLike = Field(
        default="", description="Check if the project includes educational facilities"
    )

    educational_description: str = Field(
        default="",
        description=(
            "Description of educational facilities included in the project .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    development_recreational: BooleanLike = Field(
        default="", description="Check if the project includes recreational facilities"
    )

    recreational_description: str = Field(
        default="",
        description=(
            "Description of recreational facilities included in the project .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    development_water_facilities: BooleanLike = Field(
        default="", description="Check if the project includes water facilities"
    )

    water_facilities_type: str = Field(
        default="",
        description=(
            "Type of water facilities included in the project .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    water_facilities_mgd: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Capacity of water facilities in million gallons per day (MGD)"
    )

    development_transportation: BooleanLike = Field(
        default="",
        description="Check if the project includes transportation facilities or improvements",
    )

    transportation_type: str = Field(
        default="",
        description=(
            "Type of transportation facilities or improvements .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    development_mining: BooleanLike = Field(
        default="", description="Check if the project includes mining activities"
    )

    mining_mineral: str = Field(
        default="",
        description=(
            'Type of mineral to be mined .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    development_power: BooleanLike = Field(
        default="", description="Check if the project includes power generation facilities"
    )

    power_type: str = Field(
        default="",
        description=(
            "Type of power generation (e.g., solar, wind, gas) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    power_mw: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Power generation capacity in megawatts (MW)"
    )

    development_waste_treatment: BooleanLike = Field(
        default="", description="Check if the project includes waste treatment facilities"
    )

    waste_treatment_type: str = Field(
        default="",
        description=(
            'Type of waste treatment facility .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    waste_treatment_mgd: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Capacity of waste treatment facilities in million gallons per day (MGD)",
    )

    development_hazardous_waste: BooleanLike = Field(
        default="",
        description="Check if the project includes hazardous waste facilities or activities",
    )

    hazardous_waste_type: str = Field(
        default="",
        description=(
            "Type of hazardous waste facility or activity .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    development_other: BooleanLike = Field(
        default="",
        description="Check if the project includes other types of development not listed",
    )

    other_development_description: str = Field(
        default="",
        description=(
            "Description of other development types included in the project .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ProjectIssuesDiscussedinDocument(BaseModel):
    """Environmental topics and issues addressed in the document"""

    project_issues_aesthetic_visual: BooleanLike = Field(
        default="", description="Indicate if aesthetic/visual impacts are discussed in the document"
    )

    project_issues_agricultural_land: BooleanLike = Field(
        default="", description="Indicate if agricultural land impacts are discussed"
    )

    project_issues_air_quality: BooleanLike = Field(
        default="", description="Indicate if air quality impacts are discussed"
    )

    project_issues_archeological_historical: BooleanLike = Field(
        default="",
        description="Indicate if archeological or historical resources impacts are discussed",
    )

    project_issues_biological_resources: BooleanLike = Field(
        default="", description="Indicate if biological resources impacts are discussed"
    )

    project_issues_coastal_zone: BooleanLike = Field(
        default="", description="Indicate if coastal zone impacts are discussed"
    )

    project_issues_drainage_absorption: BooleanLike = Field(
        default="", description="Indicate if drainage or absorption impacts are discussed"
    )

    project_issues_economic_jobs: BooleanLike = Field(
        default="", description="Indicate if economic or jobs impacts are discussed"
    )

    project_issues_fiscal: BooleanLike = Field(
        default="", description="Indicate if fiscal impacts are discussed"
    )

    project_issues_flood_plain_flooding: BooleanLike = Field(
        default="", description="Indicate if flood plain or flooding impacts are discussed"
    )

    project_issues_forest_land_fire_hazard: BooleanLike = Field(
        default="", description="Indicate if forest land or fire hazard impacts are discussed"
    )

    project_issues_geologic_seismic: BooleanLike = Field(
        default="", description="Indicate if geologic or seismic impacts are discussed"
    )

    project_issues_minerals: BooleanLike = Field(
        default="", description="Indicate if mineral resources impacts are discussed"
    )

    project_issues_noise: BooleanLike = Field(
        default="", description="Indicate if noise impacts are discussed"
    )

    project_issues_population_housing_balance: BooleanLike = Field(
        default="", description="Indicate if population or housing balance impacts are discussed"
    )

    project_issues_public_services_facilities: BooleanLike = Field(
        default="", description="Indicate if public services or facilities impacts are discussed"
    )

    project_issues_recreation_parks: BooleanLike = Field(
        default="", description="Indicate if recreation or parks impacts are discussed"
    )

    project_issues_schools_universities: BooleanLike = Field(
        default="", description="Indicate if schools or universities impacts are discussed"
    )

    project_issues_septic_systems: BooleanLike = Field(
        default="", description="Indicate if septic systems impacts are discussed"
    )

    project_issues_sewer_capacity: BooleanLike = Field(
        default="", description="Indicate if sewer capacity impacts are discussed"
    )

    project_issues_soil_erosion_compaction_grading: BooleanLike = Field(
        default="",
        description="Indicate if soil erosion, compaction, or grading impacts are discussed",
    )

    project_issues_solid_waste: BooleanLike = Field(
        default="", description="Indicate if solid waste impacts are discussed"
    )

    project_issues_toxic_hazardous: BooleanLike = Field(
        default="", description="Indicate if toxic or hazardous materials impacts are discussed"
    )

    project_issues_traffic_circulation: BooleanLike = Field(
        default="", description="Indicate if traffic or circulation impacts are discussed"
    )

    project_issues_vegetation: BooleanLike = Field(
        default="", description="Indicate if vegetation impacts are discussed"
    )

    project_issues_water_quality: BooleanLike = Field(
        default="", description="Indicate if water quality impacts are discussed"
    )

    project_issues_water_supply_groundwater: BooleanLike = Field(
        default="", description="Indicate if water supply or groundwater impacts are discussed"
    )

    project_issues_wetland_riparian: BooleanLike = Field(
        default="", description="Indicate if wetland or riparian impacts are discussed"
    )

    project_issues_growth_inducement: BooleanLike = Field(
        default="", description="Indicate if growth inducement impacts are discussed"
    )

    project_issues_land_use: BooleanLike = Field(
        default="", description="Indicate if land use impacts are discussed"
    )

    project_issues_cumulative_effects: BooleanLike = Field(
        default="", description="Indicate if cumulative effects are discussed"
    )

    project_issues_other: str = Field(
        default="",
        description=(
            "Description of other project issues discussed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class LandUseProjectDescription(BaseModel):
    """Existing land use designations and narrative project description"""

    present_land_use_zoning_general_plan_designation: str = Field(
        default="",
        description=(
            "Description of existing land use, zoning, and general plan designation for the "
            'project site .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    project_description: str = Field(
        ...,
        description=(
            "Detailed description of the proposed project; attach additional pages if "
            'necessary .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class NoticeOfCompletionEnvironmentalDocumentTransmittal(BaseModel):
    """
    Notice of Completion & Environmental Document Transmittal

    ''
    """

    project__lead_agency_information: ProjectLeadAgencyInformation = Field(
        ..., description="Project & Lead Agency Information"
    )
    project_location: ProjectLocation = Field(..., description="Project Location")
    document_type: DocumentType = Field(..., description="Document Type")
    local_action_type: LocalActionType = Field(..., description="Local Action Type")
    development_type: DevelopmentType = Field(..., description="Development Type")
    project_issues_discussed_in_document: ProjectIssuesDiscussedinDocument = Field(
        ..., description="Project Issues Discussed in Document"
    )
    land_use__project_description: LandUseProjectDescription = Field(
        ..., description="Land Use & Project Description"
    )
