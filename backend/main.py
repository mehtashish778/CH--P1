from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

import logging  # Import logging module
import requests
from bs4 import BeautifulSoup

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





{
  "chemical_name": "Diethyl Ether",
  "cas_number": "60-29-7",
  "storage_handling": {
    "storage": {
      "temperature": "-40°C (below flash point)",
      "conditions": "Keep container tightly closed in a dry and well-ventilated place",
      "special_monitoring": "Test for peroxide formation periodically and before distillation",
      "ignition_sources": "Keep away from heat and sources of ignition",
      "storage_class": "TRGS 510: 3 (Flammable liquids)"
    },
    "handling": {
      "workspace": "Work under hood",
      "exposure": "Do not inhale substance/mixture",
      "aerosols": "Avoid generation of vapours/aerosols",
      "hygiene": "Change contaminated clothing, wash hands after use",
      "spill_control": "Use Chemizorb® for spills"
    }
  },
  "ppe": {
    "eye_protection": {
      "type": "Safety glasses",
      "standard": "EN 166"
    },
    "hand_protection": {
      "material": "Viton®",
      "thickness": "0.7 mm",
      "breakthrough_time": "30 min"
    },
    "body_protection": "Flame retardant antistatic protective clothing",
    "respiratory": "Filter type AX recommended"
  },
  "fire_safety": {
    "suitable_extinguishers": [
      "Carbon dioxide (CO2)",
      "Foam",
      "Dry powder"
    ],
    "unsuitable_extinguishers": "No limitations specified",
    "firefighter_protection": "Self-contained breathing apparatus required",
    "special_precautions": "Remove container from danger zone and cool with water"
  },
  "chemical_properties": {
    "flammability": {
      "explosive_range": {
        "lower": "1.7%",
        "upper": "36%"
      },
      "flash_point": "-40°C",
      "storage_note": "Extremely flammable at normal storage conditions"
    },
    "stability_reactivity": {
      "stability": "Stable under standard conditions",
      "stabilizer": {
        "name": "butyl hydroxytoluene (BHT)",
        "concentration": "1 ppm"
      },
      "conditions_to_avoid": [
        "Light",
        "Heat",
        "Air",
        "Moisture"
      ],
      "incompatible_materials": [
        "Rubber",
        "Various plastics"
      ],
      "decomposition": "Forms peroxides"
    }
  },
  "emergency_response": {
    "first_aid": {
      "general": "Show safety data sheet to doctor",
      "inhalation": "Fresh air; call physician",
      "skin_contact": "Remove contaminated clothing; rinse with water",
      "eye_contact": "Rinse with plenty of water; remove contacts",
      "ingestion": "Make victim drink water (max 2 glasses); consult physician"
    },
    "toxicity": {
      "acute": {
        "lc50_inhalation": {
          "value": "97.5 mg/l",
          "species": "Mouse",
          "duration": "4h"
        },
        "ld50_oral": {
          "value": "1,211 mg/kg",
          "species": "Rat"
        },
        "ld50_dermal": {
          "value": ">20,000 mg/kg",
          "species": "Rabbit"
        }
      },
      "chronic_effects": "May cause drowsiness/dizziness; affects central nervous system"
    }
  },
  "transportation": {
    "un_number": "1155",
    "proper_shipping_name": "DIETHYL ETHER",
    "hazard_class": "3",
    "packing_group": "I",
    "special_precautions": "Tunnel restriction code (D/E)"
  }
}




app = FastAPI()

# Updated CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://10.17.18.109:8080", "http://localhost:8080"],  # Removed trailing slash
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


@app.get("/search_2")
async def search_2chemical(name_or_CAS: str = Query(None, description="Name of the chemical")):
    if not name_or_CAS:
        return JSONResponse(
            status_code=400,
            content={"error": "Please provide a chemical name or CAS number"}
        )

    url = f"https://www.fishersci.com/us/en/catalog/search/sds?selectLang=EN&store=&msdsKeyword={name_or_CAS}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)  # Added timeout
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.find_all("tr", class_="product")
        
        results = []
        for product in products:
            name_cell = product.find("td", {"data-title": "Product Name"}) or product.find("td", class_="name")
            desc_cell = product.find("td", {"data-title": "Product Description"}) or product.find("td", class_="description")
            
            product_info = {
                "name": name_cell.text.strip() if name_cell else "N/A",
                "description": desc_cell.text.strip() if desc_cell else "N/A",
                "download_links": []
            }
            
            links = product.find_all("a", class_="catalog_num_link")
            for link in links:
                href = link.get("href")
                if href:
                    full_link = f"https://www.fishersci.com{href}"
                    product_info["download_links"].append(full_link)
            
            results.append(product_info)
        
        logger.info(f"Fisher Scientific search results for '{name_or_CAS}': {len(results)} products found")
        return {"status": "success", "results": results} if results else {"status": "error", "message": "No products found"}
        
    except requests.Timeout:
        logger.error(f"Timeout while searching Fisher Scientific for '{name_or_CAS}'")
        return JSONResponse(
            status_code=504,
            content={"status": "error", "message": "Request timed out"}
        )
    except requests.RequestException as e:
        logger.error(f"Error searching Fisher Scientific: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Failed to fetch data: {str(e)}"}
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






