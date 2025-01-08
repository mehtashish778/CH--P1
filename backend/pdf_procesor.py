import re
import json
from typing import Dict, Any
from PyPDF2 import PdfReader
import markdown
import os

def pdf_processor_and_parser(file_path: str) -> Dict[Any, Any]:
    """
    Process a PDF file containing safety data and convert it to structured JSON data.
    
    Args:
        file_path (str): Path to the PDF file
    
    Returns:
        dict: Structured safety information in JSON format
    """
    # Ensure the file path exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found at: {file_path}")

    # Step 1: Convert PDF to markdown
    markdown_content = pdf_to_markdown(file_path)
    
    # Step 2: Parse the markdown content to extract safety information
    safety_data = parse_safety_data(markdown_content)
    
    return safety_data

def pdf_to_markdown(file_path: str) -> str:
    """
    Convert PDF file to markdown format using PyPDF2 and markdown
    
    Args:
        file_path (str): Path to the PDF file
    
    Returns:
        str: Markdown formatted content
    """
    try:
        # Read the PDF
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n\n"

        # Convert to Markdown
        markdown_content = markdown.markdown(text)
        
        # Save markdown content to file (optional)
        markdown_filename = os.path.splitext(file_path)[0] + '.md'
        with open(markdown_filename, 'w', encoding='utf-8') as md_file:
            md_file.write(markdown_content)
        
        return markdown_content
        
    except ImportError:
        print("Please install required packages: pip install PyPDF2 markdown")
        raise
    except Exception as e:
        print(f"Error converting PDF to markdown: {str(e)}")
        raise

def parse_safety_data(markdown_content: str) -> Dict[Any, Any]:
    """
    Parse markdown content to extract safety information
    
    Args:
        markdown_content (str): Markdown formatted content
    
    Returns:
        dict: Structured safety information
    """
    # Initialize dictionary for safety data
    safety_data = {
        "chemical_name": "",
        "cas_number": "",
        "storage_handling": {
            "storage": {},
            "handling": {}
        },
        "ppe": {
            "eye_protection": {},
            "hand_protection": {},
            "body_protection": "",
            "respiratory": {}
        },
        "fire_safety": {
            "suitable_extinguishers": [],
            "unsuitable_extinguishers": "",
            "firefighter_protection": "",
            "special_precautions": ""
        },
        "chemical_properties": {
            "flammability": {
                "explosive_range": {},
                "flash_point": "",
                "storage_note": ""
            },
            "stability_reactivity": {
                "stability": "",
                "conditions_to_avoid": [],
                "incompatible_materials": [],
                "decomposition": ""
            }
        },
        "emergency_response": {
            "first_aid": {},
            "toxicity": {
                "acute": {},
                "chronic_effects": ""
            }
        },
        "transportation": {
            "un_number": "",
            "proper_shipping_name": "",
            "hazard_class": "",
            "packing_group": "",
            "environmental_hazards": False,
            "special_precautions": ""
        }
    }

    # Parse section 2 - Hazard Identification
    section2_pattern = r"2[\.\s].*?HAZARDS?\s+IDENTIFICATION.*?(?=3[\.\s]|$)"
    section2_match = re.search(section2_pattern, markdown_content, re.IGNORECASE | re.DOTALL)
    
    if section2_match:
        section2_text = section2_match.group(0)
        
        # Extract chemical name
        chemical_name_pattern = r"Chemical\s+name.*?[:]\s*(.*?)(?:\n|$)"
        if chemical_name_match := re.search(chemical_name_pattern, section2_text, re.IGNORECASE):
            safety_data["chemical_name"] = chemical_name_match.group(1).strip()
        
        # Extract CAS number
        cas_pattern = r"CAS.*?(?:No|Number).*?[:]\s*([\d\-]+)"
        if cas_match := re.search(cas_pattern, section2_text, re.IGNORECASE):
            safety_data["cas_number"] = cas_match.group(1).strip()
        
        # Extract hazard information
        hazard_pattern = r"Hazard.*?(?:statement|classification).*?[:]\s*(.*?)(?:\n|$)"
        if hazard_match := re.search(hazard_pattern, section2_text, re.IGNORECASE):
            safety_data["hazard_classification"] = hazard_match.group(1).strip()

    section

    return safety_data

def save_safety_data(safety_data: Dict[Any, Any], output_path: str) -> None:
    """
    Save the extracted safety data to a JSON file
    
    Args:
        safety_data (dict): Structured safety information
        output_path (str): Path to save the JSON file
    """
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(safety_data, json_file, indent=2)

# Example usage:
if __name__ == "__main__":
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct absolute paths
    pdf_path = os.path.join(current_dir, "asset", "pdf_file", "DMF_MSDS.pdf")
    output_path = os.path.join(current_dir, "asset", "pdf_file", "safety_data.json")
    
    try:
        # Process PDF file
        safety_data = pdf_processor_and_parser(pdf_path)
        
        # Save extracted data
        save_safety_data(safety_data, output_path)
        print(f"Successfully processed PDF and saved data to {output_path}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure the PDF file exists in the correct location:")
        print(f"Expected path: {pdf_path}")
    except Exception as e:
        print(f"An error occurred: {e}")