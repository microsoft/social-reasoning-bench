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
    """Basic project and lead agency information"""

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
            "Name of the lead agency responsible for the environmental document .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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
            "Mailing address of the lead agency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Telephone number for the lead agency contact .If you cannot fill this, write "
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
    """Location details and nearby features"""

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

    zip_code: str = Field(default="", description="ZIP code for the project location")

    longitude_n_degrees_minutes_and_seconds: str = Field(
        default="",
        description=(
            "Latitude in degrees, minutes, and seconds (North) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    longitude_w_degrees_minutes_and_seconds: str = Field(
        default="",
        description=(
            "Longitude in degrees, minutes, and seconds (West) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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
    """Type of environmental document being filed (CEQA/NEPA/Other)"""

    nop: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Notice of Preparation (NOP)"
    )

    early_cons: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Early Consultation"
    )

    neg_dec: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Negative Declaration"
    )

    mit_neg_dec: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Mitigated Negative Declaration"
    )

    draft_eir: BooleanLike = Field(
        default="",
        description="Check if the CEQA document type is Draft Environmental Impact Report (EIR)",
    )

    supplement_subsequent_eir: BooleanLike = Field(
        default="", description="Check if the CEQA document type is a Supplement or Subsequent EIR"
    )

    prior_sch_no: str = Field(
        default="",
        description=(
            "Prior State Clearinghouse number, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_ceqa_document_type: str = Field(
        default="",
        description=(
            "Description of other CEQA document type, if not listed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    noi: BooleanLike = Field(
        default="", description="Check if the NEPA document type is Notice of Intent (NOI)"
    )

    ea: BooleanLike = Field(
        default="", description="Check if the NEPA document type is Environmental Assessment (EA)"
    )

    draft_eis: BooleanLike = Field(
        default="",
        description="Check if the NEPA document type is Draft Environmental Impact Statement (EIS)",
    )

    fonsi: BooleanLike = Field(
        default="",
        description="Check if the NEPA document type is Finding of No Significant Impact (FONSI)",
    )

    joint_document: BooleanLike = Field(
        default="", description="Check if the document is a joint CEQA/NEPA document"
    )

    final_document: BooleanLike = Field(
        default="", description="Check if the document is a final document"
    )

    other_other_document_type: str = Field(
        default="",
        description=(
            "Description of other document type, if not listed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LocalActionType(BaseModel):
    """Local planning and permitting actions associated with the project"""

    general_plan_update: BooleanLike = Field(
        default="", description="Check if the local action type includes a General Plan Update"
    )

    general_plan_amendment: BooleanLike = Field(
        default="", description="Check if the local action type includes a General Plan Amendment"
    )

    general_plan_element: BooleanLike = Field(
        default="", description="Check if the local action type includes a General Plan Element"
    )

    community_plan: BooleanLike = Field(
        default="", description="Check if the local action type includes a Community Plan"
    )

    specific_plan: BooleanLike = Field(
        default="", description="Check if the local action type includes a Specific Plan"
    )

    master_plan: BooleanLike = Field(
        default="", description="Check if the local action type includes a Master Plan"
    )

    planned_unit_development: BooleanLike = Field(
        default="", description="Check if the local action type includes a Planned Unit Development"
    )

    site_plan: BooleanLike = Field(
        default="", description="Check if the local action type includes a Site Plan"
    )

    rezone: BooleanLike = Field(
        default="", description="Check if the local action type includes a Rezone"
    )

    prezone: BooleanLike = Field(
        default="", description="Check if the local action type includes a Prezone"
    )

    use_permit: BooleanLike = Field(
        default="", description="Check if the local action type includes a Use Permit"
    )

    land_division_subdivision_etc: BooleanLike = Field(
        default="",
        description="Check if the local action type includes a land division such as a subdivision",
    )

    annexation: BooleanLike = Field(
        default="", description="Check if the local action type includes an Annexation"
    )

    redevelopment: BooleanLike = Field(
        default="", description="Check if the local action type includes Redevelopment"
    )

    coastal_permit: BooleanLike = Field(
        default="", description="Check if the local action type includes a Coastal Permit"
    )

    other_local_action_type: str = Field(
        default="",
        description=(
            "Description of other local action type, if not listed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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
        default="", description="Acreage devoted to residential uses"
    )

    office: BooleanLike = Field(
        default="", description="Check if the development type includes office uses"
    )

    office_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of office development"
    )

    office_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to office uses"
    )

    office_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with office uses"
    )

    commercial: BooleanLike = Field(
        default="", description="Check if the development type includes commercial uses"
    )

    commercial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of commercial development"
    )

    commercial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to commercial uses"
    )

    commercial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with commercial uses"
    )

    industrial: BooleanLike = Field(
        default="", description="Check if the development type includes industrial uses"
    )

    industrial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of industrial development"
    )

    industrial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to industrial uses"
    )

    industrial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with industrial uses"
    )

    educational: str = Field(
        default="",
        description=(
            "Description of educational development .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    recreational: str = Field(
        default="",
        description=(
            "Description of recreational development .If you cannot fill this, write "
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
            'Type of mineral to be extracted .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    power: BooleanLike = Field(
        default="", description="Check if the development type includes power generation facilities"
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
        default="",
        description="Check if the development type includes hazardous waste facilities or activities",
    )

    hazardous_waste_type: str = Field(
        default="",
        description=(
            "Type of hazardous waste facility or activity .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_development_type: str = Field(
        default="",
        description=(
            "Description of other development type, if not listed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectIssuesDiscussedinDocument(BaseModel):
    """Environmental issue areas addressed in the document"""

    aesthetic_visual: BooleanLike = Field(
        default="", description="Indicate if aesthetic/visual issues are discussed in the document"
    )

    agricultural_land: BooleanLike = Field(
        default="", description="Indicate if agricultural land issues are discussed in the document"
    )

    air_quality: BooleanLike = Field(
        default="", description="Indicate if air quality issues are discussed in the document"
    )

    archaeological_historical: BooleanLike = Field(
        default="",
        description=(
            "Indicate if archaeological or historical resources are discussed in the document"
        ),
    )

    biological_resources: BooleanLike = Field(
        default="", description="Indicate if biological resources are discussed in the document"
    )

    coastal_zone: BooleanLike = Field(
        default="", description="Indicate if coastal zone issues are discussed in the document"
    )

    drainage_absorption: BooleanLike = Field(
        default="",
        description="Indicate if drainage or absorption issues are discussed in the document",
    )

    economic_jobs: BooleanLike = Field(
        default="",
        description="Indicate if economic or jobs-related issues are discussed in the document",
    )

    fiscal: BooleanLike = Field(
        default="", description="Indicate if fiscal issues are discussed in the document"
    )

    flood_plain_flooding: BooleanLike = Field(
        default="",
        description="Indicate if flood plain or flooding issues are discussed in the document",
    )

    forest_land_fire_hazard: BooleanLike = Field(
        default="",
        description="Indicate if forest land or fire hazard issues are discussed in the document",
    )

    geologic_seismic: BooleanLike = Field(
        default="",
        description="Indicate if geologic or seismic issues are discussed in the document",
    )

    minerals: BooleanLike = Field(
        default="", description="Indicate if mineral resources issues are discussed in the document"
    )

    noise: BooleanLike = Field(
        default="", description="Indicate if noise issues are discussed in the document"
    )

    population_housing_balance: BooleanLike = Field(
        default="",
        description="Indicate if population or housing balance issues are discussed in the document",
    )

    public_services_facilities: BooleanLike = Field(
        default="",
        description="Indicate if public services or facilities issues are discussed in the document",
    )

    recreation_parks: BooleanLike = Field(
        default="",
        description="Indicate if recreation or parks issues are discussed in the document",
    )

    schools_universities: BooleanLike = Field(
        default="",
        description="Indicate if schools or universities issues are discussed in the document",
    )

    septic_systems: BooleanLike = Field(
        default="", description="Indicate if septic systems issues are discussed in the document"
    )

    sewer_capacity: BooleanLike = Field(
        default="", description="Indicate if sewer capacity issues are discussed in the document"
    )

    soil_erosion_compaction_grading: BooleanLike = Field(
        default="",
        description=(
            "Indicate if soil erosion, compaction, or grading issues are discussed in the document"
        ),
    )

    solid_waste: BooleanLike = Field(
        default="", description="Indicate if solid waste issues are discussed in the document"
    )

    toxic_hazardous: BooleanLike = Field(
        default="",
        description="Indicate if toxic or hazardous materials issues are discussed in the document",
    )

    traffic_circulation: BooleanLike = Field(
        default="",
        description="Indicate if traffic or circulation issues are discussed in the document",
    )

    vegetation: BooleanLike = Field(
        default="", description="Indicate if vegetation issues are discussed in the document"
    )

    water_quality: BooleanLike = Field(
        default="", description="Indicate if water quality issues are discussed in the document"
    )

    water_supply_groundwater: BooleanLike = Field(
        default="",
        description="Indicate if water supply or groundwater issues are discussed in the document",
    )

    wetland_riparian: BooleanLike = Field(
        default="",
        description="Indicate if wetland or riparian issues are discussed in the document",
    )

    growth_inducement: BooleanLike = Field(
        default="", description="Indicate if growth inducement issues are discussed in the document"
    )

    land_use: BooleanLike = Field(
        default="", description="Indicate if land use issues are discussed in the document"
    )

    cumulative_effects: BooleanLike = Field(
        default="", description="Indicate if cumulative effects are discussed in the document"
    )

    other_project_issues_discussed_in_document: str = Field(
        default="",
        description=(
            "Description of other project issues discussed in the document .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class LandUseandProjectDescription(BaseModel):
    """Existing land use designations and narrative project description"""

    present_land_use_zoning_general_plan_designation: str = Field(
        default="",
        description=(
            "Current land use, zoning, and general plan designation for the project site "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    project_description: str = Field(
        ...,
        description=(
            "Narrative description of the project; attach additional pages if necessary .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AppendixCNoticeOfCompletionEnvironmentalDocumentTransmittal(BaseModel):
    """
        Appendix C

    Notice of Completion & Environmental Document Transmittal

        Notice of Completion & Environmental Document Transmittal
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
