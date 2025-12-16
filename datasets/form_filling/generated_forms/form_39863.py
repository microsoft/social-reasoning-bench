from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectIdentification(BaseModel):
    """Basic identifying information for the project and lead agency"""

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
            "Telephone number for the contact person or lead agency .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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
            "Major cross streets near the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    project_location_zip_code: str = Field(
        default="", description="ZIP code for the project location"
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
            "Section designation for the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    twp: str = Field(
        default="",
        description=(
            "Township (Twp.) designation for the project location .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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
            "Base meridian reference for the project location .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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

    within_2_miles_schools: str = Field(
        default="",
        description=(
            'Schools within 2 miles of the project .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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


class DocumentType(BaseModel):
    """Type of CEQA/NEPA environmental document being filed"""

    nop: BooleanLike = Field(
        default="",
        description="Check if the document type is Notice of Preparation (NOP) under CEQA",
    )

    draft_eir: BooleanLike = Field(
        default="",
        description="Check if the document type is Draft Environmental Impact Report (Draft EIR)",
    )

    noi: BooleanLike = Field(
        default="", description="Check if the document type is Notice of Intent (NOI) under NEPA"
    )

    other_nepa_document_type: str = Field(
        default="",
        description=(
            "Specify other NEPA document type if not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    early_cons: BooleanLike = Field(
        default="", description="Check if the document type is Early Consultation"
    )

    supplement_subsequent_eir: BooleanLike = Field(
        default="", description="Check if the document type is a Supplement or Subsequent EIR"
    )

    ea: BooleanLike = Field(
        default="",
        description="Check if the document type is Environmental Assessment (EA) under NEPA",
    )

    joint_document: BooleanLike = Field(
        default="", description="Check if the document is a joint CEQA/NEPA document"
    )

    neg_dec: BooleanLike = Field(
        default="", description="Check if the document type is Negative Declaration (Neg Dec)"
    )

    prior_sch_no_for_neg_dec: str = Field(
        default="",
        description=(
            "Prior SCH number associated with the Negative Declaration, if any .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    draft_eis: BooleanLike = Field(
        default="",
        description="Check if the document type is Draft Environmental Impact Statement (Draft EIS)",
    )

    final_document: BooleanLike = Field(
        default="", description="Check if the document is a final CEQA/NEPA document"
    )

    mit_neg_dec: BooleanLike = Field(
        default="",
        description="Check if the document type is Mitigated Negative Declaration (Mit Neg Dec)",
    )

    other_ceqa_document_type: str = Field(
        default="",
        description=(
            "Specify other CEQA document type if not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    fonsi: BooleanLike = Field(
        default="",
        description="Check if the NEPA document is a Finding of No Significant Impact (FONSI)",
    )

    other_nepa_other: str = Field(
        default="",
        description=(
            "Specify any other NEPA-related document type .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class LocalActionType(BaseModel):
    """Local planning and permitting actions associated with the project"""

    general_plan_update: BooleanLike = Field(
        default="", description="Indicate if the project involves a General Plan Update"
    )

    specific_plan: BooleanLike = Field(
        default="", description="Indicate if the project involves a Specific Plan"
    )

    rezone: BooleanLike = Field(default="", description="Indicate if the project involves a rezone")

    annexation: BooleanLike = Field(
        default="", description="Indicate if the project involves annexation"
    )

    general_plan_amendment: BooleanLike = Field(
        default="", description="Indicate if the project involves a General Plan Amendment"
    )

    master_plan: BooleanLike = Field(
        default="", description="Indicate if the project involves a Master Plan"
    )

    prezone: BooleanLike = Field(
        default="", description="Indicate if the project involves prezoning"
    )

    redevelopment: BooleanLike = Field(
        default="", description="Indicate if the project involves redevelopment"
    )

    general_plan_element: BooleanLike = Field(
        default="", description="Indicate if the project involves a General Plan Element"
    )

    planned_unit_development: BooleanLike = Field(
        default="", description="Indicate if the project is a Planned Unit Development"
    )

    use_permit: BooleanLike = Field(
        default="", description="Indicate if the project requires a Use Permit"
    )

    coastal_permit: BooleanLike = Field(
        default="", description="Indicate if the project requires a Coastal Permit"
    )

    community_plan: BooleanLike = Field(
        default="", description="Indicate if the project involves a Community Plan"
    )

    site_plan: BooleanLike = Field(
        default="", description="Indicate if the project involves a Site Plan"
    )

    land_division_subdivision_etc: BooleanLike = Field(
        default="", description="Indicate if the project involves land division or subdivision"
    )

    other_local_action_type: str = Field(
        default="",
        description=(
            "Describe any other local action type related to the project .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class DevelopmentType(BaseModel):
    """Type and scale of physical development proposed"""

    residential: BooleanLike = Field(
        default="", description="Check if the development type includes residential uses"
    )

    residential_units: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of residential units proposed"
    )

    residential_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to residential development"
    )

    office: BooleanLike = Field(
        default="", description="Check if the development type includes office uses"
    )

    office_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of office space"
    )

    office_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to office development"
    )

    office_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with office uses"
    )

    commercial: BooleanLike = Field(
        default="", description="Check if the development type includes commercial uses"
    )

    commercial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of commercial space"
    )

    commercial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to commercial development"
    )

    commercial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with commercial uses"
    )

    industrial: BooleanLike = Field(
        default="", description="Check if the development type includes industrial uses"
    )

    industrial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of industrial space"
    )

    industrial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to industrial development"
    )

    industrial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with industrial uses"
    )

    educational: BooleanLike = Field(
        default="", description="Check if the development type includes educational uses"
    )

    recreational: BooleanLike = Field(
        default="", description="Check if the development type includes recreational uses"
    )

    water_facilities: BooleanLike = Field(
        default="", description="Check if the development type includes water facilities"
    )

    water_facilities_type: str = Field(
        default="",
        description=(
            'Type of water facilities proposed .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    water_facilities_mgd: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Capacity of water facilities in million gallons per day (MGD)"
    )

    transportation: BooleanLike = Field(
        default="", description="Check if the development type includes transportation facilities"
    )

    transportation_type: str = Field(
        default="",
        description=(
            "Type of transportation facilities proposed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mining: BooleanLike = Field(
        default="", description="Check if the development type includes mining"
    )

    mining_mineral: str = Field(
        default="",
        description=(
            'Type of mineral to be mined .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    power: BooleanLike = Field(
        default="", description="Check if the development type includes power generation"
    )

    power_type: str = Field(
        default="",
        description=(
            'Type of power generation facility .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    power_mw: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Power generation capacity in megawatts (MW)"
    )

    waste_treatment: BooleanLike = Field(
        default="", description="Check if the development type includes waste treatment facilities"
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
        description="Capacity of waste treatment facility in million gallons per day (MGD)",
    )

    hazardous_waste: BooleanLike = Field(
        default="", description="Check if the development type includes hazardous waste facilities"
    )

    hazardous_waste_type: str = Field(
        default="",
        description=(
            "Type of hazardous waste facility or waste handled .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_development_type: str = Field(
        default="",
        description=(
            "Describe any other type of development not listed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectIssuesDiscussedinDocument(BaseModel):
    """Environmental issue areas addressed in the document"""

    aesthetic_visual: BooleanLike = Field(
        default="", description="Indicate if aesthetic/visual issues are discussed in the document"
    )

    fiscal: BooleanLike = Field(
        default="", description="Indicate if fiscal issues are discussed in the document"
    )

    recreation_parks: BooleanLike = Field(
        default="", description="Indicate if recreation/parks issues are discussed in the document"
    )

    vegetation: BooleanLike = Field(
        default="", description="Indicate if vegetation issues are discussed in the document"
    )

    agricultural_land: BooleanLike = Field(
        default="", description="Indicate if agricultural land issues are discussed in the document"
    )

    flood_plain_flooding: BooleanLike = Field(
        default="", description="Indicate if flood plain or flooding issues are discussed"
    )

    schools_universities: BooleanLike = Field(
        default="", description="Indicate if schools/universities issues are discussed"
    )

    water_quality: BooleanLike = Field(
        default="", description="Indicate if water quality issues are discussed"
    )

    air_quality: BooleanLike = Field(
        default="", description="Indicate if air quality issues are discussed"
    )

    forest_land_fire_hazard: BooleanLike = Field(
        default="", description="Indicate if forest land or fire hazard issues are discussed"
    )

    septic_systems: BooleanLike = Field(
        default="", description="Indicate if septic system issues are discussed"
    )

    water_supply_groundwater: BooleanLike = Field(
        default="", description="Indicate if water supply or groundwater issues are discussed"
    )

    archeological_historical: BooleanLike = Field(
        default="",
        description="Indicate if archeological or historical resource issues are discussed",
    )

    geologic_seismic: BooleanLike = Field(
        default="", description="Indicate if geologic or seismic issues are discussed"
    )

    sewer_capacity: BooleanLike = Field(
        default="", description="Indicate if sewer capacity issues are discussed"
    )

    wetland_riparian: BooleanLike = Field(
        default="", description="Indicate if wetland or riparian issues are discussed"
    )

    biological_resources: BooleanLike = Field(
        default="", description="Indicate if biological resource issues are discussed"
    )

    minerals: BooleanLike = Field(
        default="", description="Indicate if mineral resource issues are discussed"
    )

    soil_erosion_compaction_grading: BooleanLike = Field(
        default="",
        description="Indicate if soil erosion, compaction, or grading issues are discussed",
    )

    growth_inducement: BooleanLike = Field(
        default="", description="Indicate if growth inducement issues are discussed"
    )

    coastal_zone: BooleanLike = Field(
        default="", description="Indicate if coastal zone issues are discussed"
    )

    noise: BooleanLike = Field(default="", description="Indicate if noise issues are discussed")

    solid_waste: BooleanLike = Field(
        default="", description="Indicate if solid waste issues are discussed"
    )

    land_use: BooleanLike = Field(
        default="", description="Indicate if land use issues are discussed"
    )

    drainage_absorption: BooleanLike = Field(
        default="", description="Indicate if drainage or absorption issues are discussed"
    )

    population_housing_balance: BooleanLike = Field(
        default="", description="Indicate if population/housing balance issues are discussed"
    )

    toxic_hazardous: BooleanLike = Field(
        default="", description="Indicate if toxic or hazardous materials issues are discussed"
    )

    cumulative_effects: BooleanLike = Field(
        default="", description="Indicate if cumulative effects issues are discussed"
    )

    economic_jobs: BooleanLike = Field(
        default="", description="Indicate if economic or jobs-related issues are discussed"
    )

    public_services_facilities: BooleanLike = Field(
        default="", description="Indicate if public services or facilities issues are discussed"
    )

    traffic_circulation: BooleanLike = Field(
        default="", description="Indicate if traffic or circulation issues are discussed"
    )

    other_project_issues: str = Field(
        default="",
        description=(
            "Describe any other project issues discussed in the document .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class LandUseandProjectDescription(BaseModel):
    """Existing land use designations and narrative description of the project"""

    present_land_use_zoning_general_plan_designation: str = Field(
        default="",
        description=(
            "Describe the current land use, zoning, and general plan designation of the "
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

    project_identification: ProjectIdentification = Field(..., description="Project Identification")
    project_location: ProjectLocation = Field(..., description="Project Location")
    document_type: DocumentType = Field(..., description="Document Type")
    local_action_type: LocalActionType = Field(..., description="Local Action Type")
    development_type: DevelopmentType = Field(..., description="Development Type")
    project_issues_discussed_in_document: ProjectIssuesDiscussedinDocument = Field(
        ..., description="Project Issues Discussed in Document"
    )
    land_use_and_project_description: LandUseandProjectDescription = Field(
        ..., description="Land Use and Project Description"
    )
