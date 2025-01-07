from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

import logging  # Import logging module

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chemicals = [
    {
        "Chemical Name": "N,N-Dimethylformamide",
        "CAS Number": "68-12-2",
        "Synonyms": ["Methylformamide", "Formyldimethylamine", "Dimethylformamide","DMF"],
        "Flammability Instruction": {
            "Category": "3",
            "Hazard Statements": ["H226: Flammable liquid and vapor"],
            "Precautions": ["Keep away from heat, hot surfaces, sparks, open flames, and other ignition sources. No smoking."]
        },
        "Toxicity Instruction": {
            "Acute Toxicity": ["H312: Harmful in contact with skin", "H332: Harmful if inhaled"],
            "Eye Irritation": ["H319: Causes serious eye irritation"],
            "Reproductive Toxicity": ["H360D: May damage the unborn child"]
        },
        "Handling Instruction": [
            "Work under a hood.",
            "Avoid inhaling the substance/mixture or generating vapors/aerosols.",
            "Wash hands and face after handling.",
            "Change contaminated clothing immediately."
        ],
        "Storage Instruction": [
            "Store in a tightly closed container in a dry and well-ventilated place.",
            "Keep away from heat and ignition sources.",
            "Store under inert gas and restrict access to authorized personnel."
        ],
        "PPE Instruction": {
            "Eye Protection": "Safety glasses approved under NIOSH (US) or EN 166 (EU)",
            "Skin Protection": "Use butyl-rubber gloves for full contact (breakthrough time: 480 min)",
            "Respiratory Protection": "Filter type A-(P2)",
            "Body Protection": "Wear flame-retardant, antistatic protective clothing"
        },
        "Fire Extinguisher Instruction": [
            "Suitable extinguishing media: Water, foam, carbon dioxide (CO2), dry powder.",
            "Use self-contained breathing apparatus in danger zones.",
            "Remove containers from danger and cool with water spray."
        ]
    },
    {
        "Chemical Name": "Dimethyl Ether",
        "CAS Number": "115-10-6",
        "Synonyms": ["Methyl Ether", "Wood Ether", "Methoxymethane","DME"],
        "Flammability Instruction": {
            "Category": "1A",
            "Hazard Statements": ["H220: Extremely flammable gas"],
            "Precautions": [
                "Keep away from heat, hot surfaces, sparks, open flames, and other ignition sources. No smoking.",
                "P377: Leaking gas fire: Do not extinguish unless the leak can be stopped safely.",
                "P381: In case of leakage, eliminate all ignition sources."
            ]
        },
        "Toxicity Instruction": {
            "Hazards": ["May displace oxygen and cause rapid suffocation."],
            "Behavioral Effects": ["Ataxia", "Coma", "General anesthesia at high inhalation levels"]
        },
        "Handling Instruction": [
            "Avoid breathing gas.",
            "Work in well-ventilated areas.",
            "Change contaminated clothing and wash hands after handling."
        ],
        "Storage Instruction": [
            "Store in tightly closed containers away from combustible materials and sources of ignition.",
            "Protect from sunlight and store in a well-ventilated place."
        ],
        "PPE Instruction": {
            "Eye Protection": "Safety glasses tested under standards such as NIOSH (US) or EN 166(EU)",
            "Skin Protection": "Use nitrile rubber gloves with a minimum thickness of 0.4 mm",
            "Respiratory Protection": "Use a Filter Type ABEK for vapors/mists",
            "Body Protection": "Wear flame-retardant, antistatic protective clothing"
        },
        "Fire Extinguisher Instruction": [
            "Suitable extinguishing media: Carbon dioxide (CO2), foam, or dry powder.",
            "Wear self-contained breathing apparatus during firefighting.",
            "Remove the container from the danger zone and cool with water."
        ]
    }
]




app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://10.42.241.137:8081","http://192.168.124.61:8081","http://localhost:8081"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}



# Search Chemical API
@app.get("/search")
async def search_chemical(name_or_CAS: str = Query(None, description="Name of the chemical")):
    results = []
    for chemical in chemicals:
        if (name_or_CAS and name_or_CAS.lower() in chemical["Chemical Name"].lower()) or (name_or_CAS == chemical["CAS Number"]  or (name_or_CAS in chemical["Synonyms"])):
            results.append({
                "Chemical Name": chemical["Chemical Name"],
                "CAS Number": chemical["CAS Number"],
                "Common Names": chemical["Synonyms"]
            })
    logger.info(f"Search results for '{name_or_CAS}': {results}")  # Log the search results
    return results if results else {"error": "No chemical found matching the criteria"}
  



# Chemical Profile API
@app.get("/chemical")
async def get_chemical_details(CAS_number: str = Query(..., description="Name of the chemical")):
    # Find and return the chemical details directly
    for chemical in chemicals:
        if chemical["CAS Number"] == CAS_number:
            logger.info(f"Details retrieved for CAS number '{CAS_number}': {chemical}")  # Log the chemical details
            return JSONResponse(content=chemical)  # Return the details of the matching chemical as JSON
    logger.warning(f"Chemical not found for CAS number '{CAS_number}'")  # Log warning if not found
    return JSONResponse(content={"error": "Chemical not found"})  # Return an error message as JSON if not found






