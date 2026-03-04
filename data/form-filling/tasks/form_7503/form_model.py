from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectAgencyInformation(BaseModel):
    """Basic identifying information about the project and lead agency"""

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
            "Phone number for the contact person or lead agency .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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

    project_location_zip_code: str = Field(
        default="", description="ZIP code of the project location"
    )

    cross_streets: str = Field(
        default="",
        description=(
            "Major cross streets near the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    latitude_dms: str = Field(
        default="",
        description=(
            "Latitude of the project site in degrees, minutes, and seconds (N) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    longitude_dms: str = Field(
        default="",
        description=(
            "Longitude of the project site in degrees, minutes, and seconds (W) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
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
            "Land survey section for the project location .If you cannot fill this, write "
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
            "Base meridian for the land survey description .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_state_hwy_number: str = Field(
        default="",
        description=(
            "State highway numbers within 2 miles of the project site .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_waterways: str = Field(
        default="",
        description=(
            "Waterways within 2 miles of the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_airports: str = Field(
        default="",
        description=(
            "Airports within 2 miles of the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_railways: str = Field(
        default="",
        description=(
            "Railways within 2 miles of the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_schools: str = Field(
        default="",
        description=(
            "Schools within 2 miles of the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class DocumentType(BaseModel):
    """Type of CEQA/NEPA environmental document being filed"""

    nop: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Notice of Preparation (NOP)"
    )

    draft_eir: BooleanLike = Field(
        default="",
        description=(
            "Check if the CEQA document type is Draft Environmental Impact Report (Draft EIR)"
        ),
    )

    early_cons: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Early Consultation"
    )

    supplement_subsequent_eir: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Supplement or Subsequent EIR"
    )

    neg_dec: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Negative Declaration"
    )

    prior_sch_no: str = Field(
        default="",
        description=(
            "Prior State Clearinghouse number, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mit_neg_dec: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Mitigated Negative Declaration"
    )

    other_ceqa_document_type: str = Field(
        default="",
        description=(
            "Specify other CEQA document type if not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    noi: BooleanLike = Field(
        default="", description="Check if the NEPA document type is Notice of Intent (NOI)"
    )

    other_nepa_document_type: str = Field(
        default="",
        description=(
            "Specify other NEPA document type if not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ea: BooleanLike = Field(
        default="", description="Check if the NEPA document type is Environmental Assessment (EA)"
    )

    joint_document: BooleanLike = Field(
        default="", description="Check if the document is a joint CEQA/NEPA document"
    )

    draft_eis: BooleanLike = Field(
        default="",
        description=(
            "Check if the NEPA document type is Draft Environmental Impact Statement (Draft EIS)"
        ),
    )

    final_document: BooleanLike = Field(
        default="", description="Check if the NEPA document is a final document"
    )

    fonsi: BooleanLike = Field(
        default="",
        description="Check if the NEPA document type is Finding of No Significant Impact (FONSI)",
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
    """Local planning or permitting actions associated with the project"""

    general_plan_update: BooleanLike = Field(
        default="", description="Check if the local action type includes a General Plan Update"
    )

    specific_plan: BooleanLike = Field(
        default="", description="Check if the local action type includes a Specific Plan"
    )

    rezone: BooleanLike = Field(
        default="", description="Check if the local action type includes a Rezone"
    )

    annexation: BooleanLike = Field(
        default="", description="Check if the local action type includes an Annexation"
    )

    general_plan_amendment: BooleanLike = Field(
        default="", description="Check if the local action type includes a General Plan Amendment"
    )

    master_plan: BooleanLike = Field(
        default="", description="Check if the local action type includes a Master Plan"
    )

    prezone: BooleanLike = Field(
        default="", description="Check if the local action type includes a Prezone"
    )

    redevelopment: BooleanLike = Field(
        default="", description="Check if the local action type includes Redevelopment"
    )

    general_plan_element: BooleanLike = Field(
        default="", description="Check if the local action type includes a General Plan Element"
    )

    planned_unit_development: BooleanLike = Field(
        default="", description="Check if the local action type includes a Planned Unit Development"
    )

    use_permit: BooleanLike = Field(
        default="", description="Check if the local action type includes a Use Permit"
    )

    coastal_permit: BooleanLike = Field(
        default="", description="Check if the local action type includes a Coastal Permit"
    )

    community_plan: BooleanLike = Field(
        default="", description="Check if the local action type includes a Community Plan"
    )

    site_plan: BooleanLike = Field(
        default="", description="Check if the local action type includes a Site Plan"
    )

    land_division_subdivision_etc: BooleanLike = Field(
        default="",
        description="Check if the local action type includes Land Division or Subdivision",
    )

    other_local_action_type: str = Field(
        default="",
        description=(
            "Specify any other local action type not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
        default="", description="Total square footage of office space"
    )

    office_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to office development"
    )

    office_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with office uses"
    )

    transportation: BooleanLike = Field(
        default="",
        description="Check if the development type includes transportation facilities or services",
    )

    transportation_type: str = Field(
        default="",
        description=(
            "Type of transportation development (e.g., road, rail, transit) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    commercial: BooleanLike = Field(
        default="", description="Check if the development type includes commercial uses"
    )

    commercial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total square footage of commercial space"
    )

    commercial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to commercial development"
    )

    commercial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with commercial uses"
    )

    mining: BooleanLike = Field(
        default="", description="Check if the development type includes mining activities"
    )

    mining_mineral: str = Field(
        default="",
        description=(
            'Type of mineral to be extracted .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    industrial: BooleanLike = Field(
        default="", description="Check if the development type includes industrial uses"
    )

    industrial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total square footage of industrial space"
    )

    industrial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to industrial development"
    )

    industrial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with industrial uses"
    )

    power: BooleanLike = Field(
        default="", description="Check if the development type includes power generation facilities"
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

    educational: BooleanLike = Field(
        default="", description="Check if the development type includes educational facilities"
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
        default="", description="Waste treatment capacity in million gallons per day (MGD)"
    )

    recreational: BooleanLike = Field(
        default="", description="Check if the development type includes recreational facilities"
    )

    hazardous_waste: BooleanLike = Field(
        default="", description="Check if the development type includes hazardous waste facilities"
    )

    hazardous_waste_type: str = Field(
        default="",
        description=(
            "Type of hazardous waste facility or activity .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    water_facilities: BooleanLike = Field(
        default="", description="Check if the development type includes water facilities"
    )

    water_facilities_type: str = Field(
        default="",
        description=(
            "Type of water facility (e.g., treatment plant, pipeline) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    water_facilities_mgd: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Water facility capacity in million gallons per day (MGD)"
    )

    other_development_type: str = Field(
        default="",
        description=(
            "Specify any other development type not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
        default="",
        description="Indicate if recreation or parks issues are discussed in the document",
    )

    vegetation: BooleanLike = Field(
        default="", description="Indicate if vegetation issues are discussed in the document"
    )

    agricultural_land: BooleanLike = Field(
        default="", description="Indicate if agricultural land issues are discussed in the document"
    )

    flood_plain_flooding: BooleanLike = Field(
        default="",
        description="Indicate if flood plain or flooding issues are discussed in the document",
    )

    schools_universities: BooleanLike = Field(
        default="",
        description="Indicate if schools or universities issues are discussed in the document",
    )

    water_quality: BooleanLike = Field(
        default="", description="Indicate if water quality issues are discussed in the document"
    )

    air_quality: BooleanLike = Field(
        default="", description="Indicate if air quality issues are discussed in the document"
    )

    forest_land_fire_hazard: BooleanLike = Field(
        default="",
        description="Indicate if forest land or fire hazard issues are discussed in the document",
    )

    septic_systems: BooleanLike = Field(
        default="", description="Indicate if septic system issues are discussed in the document"
    )

    water_supply_groundwater: BooleanLike = Field(
        default="",
        description="Indicate if water supply or groundwater issues are discussed in the document",
    )

    archaeological_historical: BooleanLike = Field(
        default="",
        description="Indicate if archaeological or historical issues are discussed in the document",
    )

    geologic_seismic: BooleanLike = Field(
        default="",
        description="Indicate if geologic or seismic issues are discussed in the document",
    )

    sewer_capacity: BooleanLike = Field(
        default="", description="Indicate if sewer capacity issues are discussed in the document"
    )

    wetland_riparian: BooleanLike = Field(
        default="",
        description="Indicate if wetland or riparian issues are discussed in the document",
    )

    biological_resources: BooleanLike = Field(
        default="",
        description="Indicate if biological resources issues are discussed in the document",
    )

    minerals_issue: BooleanLike = Field(
        default="", description="Indicate if mineral resources issues are discussed in the document"
    )

    soil_erosion_compaction_grading: BooleanLike = Field(
        default="",
        description=(
            "Indicate if soil erosion, compaction, or grading issues are discussed in the document"
        ),
    )

    growth_inducement: BooleanLike = Field(
        default="", description="Indicate if growth inducement issues are discussed in the document"
    )

    coastal_zone: BooleanLike = Field(
        default="", description="Indicate if coastal zone issues are discussed in the document"
    )

    noise: BooleanLike = Field(
        default="", description="Indicate if noise issues are discussed in the document"
    )

    solid_waste: BooleanLike = Field(
        default="", description="Indicate if solid waste issues are discussed in the document"
    )

    land_use: BooleanLike = Field(
        default="", description="Indicate if land use issues are discussed in the document"
    )

    drainage_absorption: BooleanLike = Field(
        default="",
        description="Indicate if drainage or absorption issues are discussed in the document",
    )

    population_housing_balance: BooleanLike = Field(
        default="",
        description="Indicate if population or housing balance issues are discussed in the document",
    )

    toxic_hazardous: BooleanLike = Field(
        default="",
        description="Indicate if toxic or hazardous materials issues are discussed in the document",
    )

    cumulative_effects: BooleanLike = Field(
        default="", description="Indicate if cumulative effects are discussed in the document"
    )

    economic_jobs: BooleanLike = Field(
        default="", description="Indicate if economic or jobs issues are discussed in the document"
    )

    public_services_facilities: BooleanLike = Field(
        default="",
        description="Indicate if public services or facilities issues are discussed in the document",
    )

    traffic_circulation: BooleanLike = Field(
        default="",
        description="Indicate if traffic or circulation issues are discussed in the document",
    )

    other_project_issues_discussed_in_document: str = Field(
        default="",
        description=(
            "Specify any other project issues discussed in the document .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LandUseProjectDescription(BaseModel):
    """Existing land use designations and narrative project description"""

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


class AppendixCNoticeOfCompletionEnvironmentalDocumentTransmittal(BaseModel):
    """
        Appendix C

    Notice of Completion & Environmental Document Transmittal

        ''
    """

    project__agency_information: ProjectAgencyInformation = Field(
        ..., description="Project & Agency Information"
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
