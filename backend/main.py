from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

import logging  # Import logging module
import requests
from bs4 import BeautifulSoup
import socket
import uvicorn
import json
from pathlib import Path
from fishersci_search import fishersci_search

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
    },
    
    {
        "Chemical Name": "Diethyl ether",
        "CAS Number": "60-29-7",
        "Synonyms": ["Ether" ,"Ethyl ether","DEE"],
        
        "Storage": {
            "Flash Point": "-40 °C",
            "Storage Conditions": "Keep the container tightly closed in a dry and well-ventilated place.",
            "Source of Ignition Precautions": "Keep away from heat and sources of ignition.",
            "Precautions": "Test for peroxide formation periodically and before distillation.",
            "Stability": "The product is chemically stable under standard ambient conditions (room temperature)."
        },
        "Handling": {
            "Safe Handling": "Work under a hood. Do not inhale the substance/mixture. Avoid generating vapors/aerosols.",
            "Hygiene Measures": "Change contaminated clothing. Preventive skin protection is recommended. Wash hands after working with the substance.",
            "Precautions": [
            "Keep away from heat, hot surfaces, sparks, open flames, and other ignition sources. No smoking.",
            "Keep the container tightly closed.",
            "Ground and bond container and receiving equipment.",
            "Use explosion-proof electrical/ventilating/lighting equipment."
            ],
            "Spill Protection": "Use liquid-absorbent material such as Chemizorb® to manage spills.",
            "Protection Against Fire and Explosion": "Keep away from open flames, hot surfaces, and sources of ignition. Take precautionary measures against static discharge."
        },
        "Personal Protective Equipment": {
            "Eye/Face Protection": "Use safety glasses tested and approved under appropriate standards such as NIOSH (US) or EN 166 (EU).",
            "Skin Protection": {
            "Material": "Viton®",
            "Minimum Layer Thickness": "0.7 mm"
            },
            "Body Protection": "Flame-retardant antistatic protective clothing.",
            "Respiratory Protection": "Filter type AX is recommended when vapors or aerosols are generated."
        },
        "Fire Extinguisher": {
            "Fire Extinguisher to be Used": ["Carbon dioxide (CO₂)", "Foam", "Dry powder"],
            "Precautions for Firefighters": "In the event of a fire, wear self-contained breathing apparatus.",
            "Specific Precautions": "Remove the container from the danger zone and cool with water. Prevent fire extinguishing water from contaminating surface water or the groundwater system.",
            "Fire Extinguisher Never to be Used": "No limitations on extinguishing agents are specified for this substance."
        },
        "Flammability": {
            "Flammable/Explosive Concentration": "The chemical is flammable/explosive in the concentration 1.7% (LFL) to 36% (UFL).",
            "Flash Point and Flammability": {
            "Flash Point": "-40 °C",
            "Flammability at Storage Temperature": "If the given storage temperature is above -40 °C (as storage typically occurs at room temperature or above), the chemical is flammable under these conditions."
            }
        },
        "Reactivity and Stability": {
            "Stability": "The product is chemically stable under standard ambient conditions (room temperature). Contains stabilizer(s): butyl hydroxytoluene (BHT) at 1 ppm.",
            "Reactivity": "Formation of peroxides is possible. Vapors may form explosive mixtures with air.",
            "Conditions to Avoid": ["Light", "Heat", "Air", "Warming", "Moisture"],
            "Incompatible Materials": [
            "Rubber",
            "Various plastics",
            "Strong oxidizing agents",
            "Halogens",
            "Peroxides",
            "Azides",
            "Perchloric acid"
            ],
            "Decomposition Products": "Peroxides are formed as decomposition products. In the event of fire, carbon oxides may also form."
        },
        "First Aid Measures": {
            "General": "Show the material safety data sheet to the doctor in attendance.",
            "Inhalation": "Move the person to fresh air and call a physician.",
            "Skin Contact": "Remove all contaminated clothing immediately. Rinse skin with water or take a shower.",
            "Eye Contact": "Rinse the affected eyes with plenty of water. Remove contact lenses if present.",
            "Ingestion": "Immediately make the victim drink water (two glasses at most) and consult a physician."
        },
        "Toxic Release Measures": {
            "Acute Toxicity": {
            "LC50": {
                "Value": "97.5 mg/L",
                "Method": "Inhalation",
                "Species": "Mouse",
                "Duration": "4 hours"
            },
            "LC50 Matrix Assessment": "Moderate to high acute toxicity.",
            "LD50": {
                "Value": "1,211 mg/kg",
                "Method": "Oral",
                "Species": "Rat"
            },
            "LD50 Matrix Assessment": "Moderate acute toxicity."
            },
            "Chronic Toxicity": {
            "Germ Cell Mutagenicity": "Negative results were observed in micronucleus tests and mammalian cell gene mutation tests, indicating no mutagenic potential.",
            "Carcinogenicity": "No data available.",
            "Reproductive Toxicity": "No data available.",
            "Specific Target Organ Toxicity (Repeated Exposure)": "Data on repeated exposure toxicity is not conclusive; however, no chronic toxicity effects were emphasized."
            },
            "Possible Medical Effects": {
            "Acute Effects": "May cause drowsiness, dizziness, and irritation to the respiratory tract. Prolonged or repeated skin exposure may lead to dermatitis.",
            "Chronic Effects": "Long-term exposure data is limited, but no significant effects on germ cells or reproduction have been identified."
            }
        }
    }
]




app = FastAPI()

# Updated CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Removed trailing slash
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(
    # CORSMiddleware,
    # allow_origins=["*"],  # Allow all origins (development only!)
    # allow_credentials=True,
    # allow_methods=["*"],
    # allow_headers=["*"],
# )

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


# Load the JSON data
def load_products():
    json_path = Path(__file__).parent / "db" / "all_products.json"
    with open(json_path, 'r') as f:
        return json.load(f)

@app.get("/search_2")
async def search_2chemical(name_or_CAS: str = Query(None, description="Name of the chemical")):
    if not name_or_CAS:
        return JSONResponse(
            status_code=400,
            content={"error": "Please provide a chemical name or CAS number"}
        )
    
    try:
        products = load_products()
        matching_products = []
        search_term = name_or_CAS.lower()
        
        for product in products:
            product_name = product.get("Product Name", "").lower()
            product_desc = product.get("Product Description", "").lower()
            
            if search_term in product_name or search_term in product_desc:
                matching_products.append({
                    "name": product.get("Product Name"),
                    "description": product.get("Product Description"),
                    "download_links": product.get("Download Links", [])
                })
        
        if matching_products:
            logger.info(f"Found {len(matching_products)} products matching '{name_or_CAS}'")
            return {"status": "success", "results": matching_products}
        else:
            logger.info(f"No products found matching '{name_or_CAS}'")
            return {"status": "error", "message": "No products found matching the criteria"}
            
    except Exception as e:
        logger.error(f"Error searching products: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Failed to search products: {str(e)}"}
        )

    
@app.get("/search_3")
async def search_3chemical(name_or_CAS: str = Query(None, description="Name of the chemical")):
    if not name_or_CAS:
        return JSONResponse(
            status_code=400,
            content={"error": "Please provide a chemical name or CAS number"}
        )
    
    try:
        # Add debug logging
        logger.info(f"Attempting to search Fisher Scientific for: {name_or_CAS}")
        
        results = fishersci_search(querry=name_or_CAS)
        
        # Add debug logging for results
        logger.info(f"Search results: {results}")
        
        # Check if results is None or empty
        if not results:
            logger.warning(f"No results found for query: {name_or_CAS}")
            return JSONResponse(
                status_code=200,  # Changed from 404 to 200 since empty results is not an error
                content={
                    "status": "success",
                    "results": [],
                    "message": f"No products found for '{name_or_CAS}'"
                }
            )
            
        logger.info(f"Found {len(results)} products from Fisher Scientific matching '{name_or_CAS}'")
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "results": results
            }
        )
    except Exception as e:
        logger.error(f"Error searching Fisher Scientific: {str(e)}", exc_info=True)  # Added exc_info for full traceback
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Failed to search Fisher Scientific: {str(e)}"
            }
        )




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



if __name__=="__main__":
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    port = 8000

    print(f"Server is running at:")
    print(f"- Local: http://localhost:{port}")
    print(f"- Network: http://{local_ip}:{port}")

    uvicorn.run(app, host="0.0.0.0", port=port)





