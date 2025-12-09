from .base_parser import BaseParser

class RootsParser(BaseParser):
    """
    A parser designed to extract product information from a 'Roots' API response payload.
    
    This parser handles the specific nested structure of the Roots data, extracting
    details from both the top-level and the nested 'attributes' dictionary.
    """
    
    def _get_attribute(self, attributes, key, default='N/A'):
        """Safely retrieves the first item from a list within the attributes dictionary."""
        # Attributes in the payload are often lists, e.g., "AGE": ["CHILD"]
        # This gets the value, provides a default list, and takes the first element.
        return attributes.get(key, [default])[0]

    def parse_response(self, search_keyword, api_data):
        """
        Parses the API response data to extract and format product information.

        Args:
            search_keyword (str): The original search term.
            api_data (dict): The JSON data returned from the API.

        Returns:
            dict: A dictionary formatted for a Large Language Model (LLM),
                  containing the structured product data or an error message.
        """
        # Assuming api_data might contain a list of products under a 'products' key
        products = api_data.get("products", [])
        
        # If the top-level object is a single product, wrap it in a list
        if not products and "prod_id" in api_data:
            products = [api_data]
            
        if not products:
            return {"search_term": search_keyword, "error": "No products returned."}

        llm_texts = []
        for i, product in enumerate(products):
            # Extract title and description from the top level
            title = product.get('title', 'N/A').strip() or 'N/A'
            desc = product.get('description', 'N/A').strip() or 'N/A'
            
            # Get the nested attributes dictionary for easier access
            attributes = product.get('attributes', {})
            
            # Extract details from the bottom/nested 'attributes' dictionary
            age = self._get_attribute(attributes, 'AGE')
            gender = self._get_attribute(attributes, 'GENDER')
            occasion = self._get_attribute(attributes, 'OCCASION')
            sleeve_type = self._get_attribute(attributes, 'SLEEVE_TYPE')
            
            # Fabric can be a list, so join its elements
            fabric_list = attributes.get('FABRIC', [])
            fabric = ", ".join(fabric_list) if fabric_list else 'N/A'
            
            # Get all available colors and join them with a slash
            colors_list = attributes.get('ALL_VARIANT_COLORS', [])
            all_colors = " / ".join(colors_list) if colors_list else 'N/A'
            
            # Format the extracted data into a single string for the LLM
            llm_texts.append(f"""prod {i + 1}:
title: {title}
description: {desc}
age: {age}
gender: {gender}
occasion: {occasion}
sleeve_type: {sleeve_type}
fabric: {fabric}
colors: {all_colors}""")
            
        return self._format_llm_output(search_keyword, llm_texts)