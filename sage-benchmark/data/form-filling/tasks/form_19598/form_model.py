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
            "Mailing address of the lead agency or contact person .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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

    zip: str = Field(..., description="ZIP code for the lead agency mailing address")

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

    zip_code: str = Field(default="", description="ZIP code for the project location")

    longitude_n_degrees_minutes_seconds: str = Field(
        default="",
        description=(
            "Latitude in degrees, minutes, and seconds (North) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    longitude_w_degrees_minutes_seconds: str = Field(
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
            "Section number for the project location (public land survey) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
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
    """Type of environmental document being submitted (CEQA/NEPA/Other)"""

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
        default="", description="Check if the CEQA document type is a Supplement or Subsequent EIR"
    )

    neg_dec_prior_sch_no: BooleanLike = Field(
        default="",
        description=(
            "Check if the CEQA document type is a Negative Declaration with a prior SCH number"
        ),
    )

    mit_neg_dec: BooleanLike = Field(
        default="",
        description="Check if the CEQA document type is a Mitigated Negative Declaration",
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

    ea: BooleanLike = Field(
        default="", description="Check if the NEPA document type is Environmental Assessment (EA)"
    )

    draft_eis: BooleanLike = Field(
        default="",
        description=(
            "Check if the NEPA document type is Draft Environmental Impact Statement (Draft EIS)"
        ),
    )

    fonsi: BooleanLike = Field(
        default="",
        description="Check if the NEPA document type is Finding of No Significant Impact (FONSI)",
    )

    joint_document: BooleanLike = Field(
        default="", description="Check if the document is a joint CEQA/NEPA document"
    )

    final_document: BooleanLike = Field(
        default="", description="Check if this is the final version of the environmental document"
    )

    other_document_type: str = Field(
        default="",
        description=(
            "Specify other document type if not listed .If you cannot fill this, write "
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
        default="", description="Check if the local action type involves a General Plan Element"
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
            "Specify other local action type if not listed .If you cannot fill this, write "
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

    transportation: BooleanLike = Field(
        default="", description="Check if the development type includes transportation facilities"
    )

    transportation_type: str = Field(
        default="",
        description=(
            "Type of transportation facility (e.g., road, rail, transit) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
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

    power: BooleanLike = Field(
        default="", description="Check if the development type includes power generation facilities"
    )

    power_type: str = Field(
        default="",
        description=(
            "Type of power facility (e.g., solar, wind, gas) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    power_mw: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Power generation capacity in megawatts (MW)"
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

    educational: BooleanLike = Field(
        default="", description="Check if the development type includes educational facilities"
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

    recreational: BooleanLike = Field(
        default="", description="Check if the development type includes recreational facilities"
    )

    other_development_type: str = Field(
        default="",
        description=(
            "Specify other development type if not listed .If you cannot fill this, write "
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


class ProjectIssuesDiscussedinDocument(BaseModel):
    """Environmental topics and issues addressed in the document"""

    aesthetic_visual: BooleanLike = Field(
        default="", description="Indicate if aesthetic/visual impacts are discussed in the document"
    )

    fiscal: BooleanLike = Field(
        default="", description="Indicate if fiscal impacts are discussed in the document"
    )

    recreation_parks: BooleanLike = Field(
        default="", description="Indicate if recreation/parks impacts are discussed in the document"
    )

    vegetation: BooleanLike = Field(
        default="", description="Indicate if vegetation impacts are discussed in the document"
    )

    agricultural_land: BooleanLike = Field(
        default="",
        description="Indicate if agricultural land impacts are discussed in the document",
    )

    flood_plain_flooding: BooleanLike = Field(
        default="",
        description="Indicate if flood plain or flooding impacts are discussed in the document",
    )

    schools_universities: BooleanLike = Field(
        default="", description="Indicate if impacts to schools or universities are discussed"
    )

    water_quality: BooleanLike = Field(
        default="", description="Indicate if water quality impacts are discussed in the document"
    )

    air_quality: BooleanLike = Field(
        default="", description="Indicate if air quality impacts are discussed in the document"
    )

    forest_land_fire_hazard: BooleanLike = Field(
        default="", description="Indicate if forest land or fire hazard impacts are discussed"
    )

    septic_systems: BooleanLike = Field(
        default="", description="Indicate if septic system impacts are discussed in the document"
    )

    water_supply_groundwater: BooleanLike = Field(
        default="", description="Indicate if water supply or groundwater impacts are discussed"
    )

    archeological_historical: BooleanLike = Field(
        default="",
        description="Indicate if archeological or historical resource impacts are discussed",
    )

    geologic_seismic: BooleanLike = Field(
        default="", description="Indicate if geologic or seismic impacts are discussed"
    )

    sewer_capacity: BooleanLike = Field(
        default="", description="Indicate if sewer capacity impacts are discussed"
    )

    wetland_riparian: BooleanLike = Field(
        default="", description="Indicate if wetland or riparian impacts are discussed"
    )

    biological_resources: BooleanLike = Field(
        default="", description="Indicate if biological resource impacts are discussed"
    )

    minerals: BooleanLike = Field(
        default="", description="Indicate if mineral resource impacts are discussed"
    )

    soil_erosion_compaction_grading: BooleanLike = Field(
        default="",
        description="Indicate if soil erosion, compaction, or grading impacts are discussed",
    )

    growth_inducement: BooleanLike = Field(
        default="", description="Indicate if growth-inducing impacts are discussed"
    )

    coastal_zone: BooleanLike = Field(
        default="", description="Indicate if coastal zone impacts are discussed"
    )

    noise: BooleanLike = Field(default="", description="Indicate if noise impacts are discussed")

    solid_waste: BooleanLike = Field(
        default="", description="Indicate if solid waste impacts are discussed"
    )

    land_use: BooleanLike = Field(
        default="", description="Indicate if land use impacts are discussed"
    )

    drainage_absorption: BooleanLike = Field(
        default="", description="Indicate if drainage or absorption impacts are discussed"
    )

    population_housing_balance: BooleanLike = Field(
        default="", description="Indicate if population/housing balance impacts are discussed"
    )

    toxic_hazardous: BooleanLike = Field(
        default="", description="Indicate if toxic or hazardous materials impacts are discussed"
    )

    cumulative_effects: BooleanLike = Field(
        default="", description="Indicate if cumulative impacts are discussed"
    )

    economic_jobs: BooleanLike = Field(
        default="", description="Indicate if economic or jobs-related impacts are discussed"
    )

    public_services_facilities: BooleanLike = Field(
        default="", description="Indicate if public services or facilities impacts are discussed"
    )

    traffic_circulation: BooleanLike = Field(
        default="", description="Indicate if traffic or circulation impacts are discussed"
    )

    other_project_issues: str = Field(
        default="",
        description=(
            "Specify any other project issues discussed in the document .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ExistingLandUseProjectDescription(BaseModel):
    """Current land use designations and narrative description of the project"""

    present_land_use_zoning_general_plan_designation: str = Field(
        default="",
        description=(
            "Current land use, zoning, and general plan designation of the project site .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    project_description: str = Field(
        ...,
        description=(
            "Narrative description of the proposed project; use additional pages if "
            'necessary .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class AppendixCNoticeOfCompletionEnvironmentalDocumentTransmittal(BaseModel):
    """
        Appendix C

    Notice of Completion & Environmental Document Transmittal

        Mail to: State Clearinghouse, P.O. Box 3044, Sacramento, CA 95812-3044 (916) 445-0613 For Hand Delivery/Street Address: 1400 Tenth Street, Sacramento, CA 95814
        Note: The State Clearinghouse will assign identification numbers for all new projects. If a SCH number already exists for a project (e.g. Notice of Preparation or previous draft document) please fill it in.
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
    existing_land_use__project_description: ExistingLandUseProjectDescription = Field(
        ..., description="Existing Land Use & Project Description"
    )
