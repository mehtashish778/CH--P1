import requests
from bs4 import BeautifulSoup

def fishersci_search(querry: str):
    """
    Search Fisher Scientific for a chemical by name or CAS number and return product details.
    
    Args:
        querry (str): Chemical name or CAS number to search for
        
    Returns:
        list: List of dictionaries containing product details
    """
    # Base URL with placeholder for the search term
    base_url = "https://www.fishersci.com/us/en/catalog/search/sds?storeId=10652&langId=-1&msdsKeyword={}&offset={}&nav=0&selectLang=EN"
    
    # Headers to mimic a browser visit
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    
    product_list = []
    page_number = 1
    
    while True:
        # Construct the URL for the current page
        url = base_url.format(querry, page_number)
        
        # Send GET request
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to fetch the webpage. Status code: {response.status_code}")
            break
            
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all rows with product details
        products = soup.find_all("tr", class_="product")
        
        # If no products are found, exit the loop
        if not products:
            break
            
        # Loop through products
        for product in products:
            # Extract product name
            name_cell = product.find("td", {"data-title": "Product Name"})
            name = name_cell.text.strip() if name_cell else "N/A"
            
            # Clean up the product name
            name = name.replace("\n", "").replace("\r", "").replace("Close", "").replace("\t", "").strip()
            
            # Extract product description
            desc_cell = product.find("td", {"data-title": "Product Description"})
            description = desc_cell.text.strip() if desc_cell else "N/A"
            
            # Extract download links
            download_links = []
            links = product.find_all("a", class_="catalog_num_link")
            for link in links:
                href = link.get("href")
                if href:
                    full_link = f"https://www.fishersci.com{href}"
                    download_links.append(full_link)
            
            # Append product details if name is not "N/A"
            if name != "N/A":
                product_list.append({
                    "Product Name": name,
                    "Product Description": description,
                    "Download Links": download_links
                })
        
        # Move to the next page
        page_number += 1
    
    return product_list





    