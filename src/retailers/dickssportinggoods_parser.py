from .base_parser import BaseParser

class DicksSportingGoodsParser(BaseParser):
    def parse_response(self, search_keyword, api_data):
        # Extract products from the payload
        products = api_data.get("products", [])
        if not products: 
            return {"search_term": search_keyword, "error": "No products returned."}

        llm_texts = []
        for i, product in enumerate(products):
            # Extract standard fields
            title = str(product.get('title', 'N/A')).strip() or 'N/A'
            desc = str(product.get('description', 'N/A')).strip() or 'N/A'
            
            # Extract and format additional_fields (which is a list of strings)
            add_fields_list = product.get('additional_fields', [])
            if isinstance(add_fields_list, list) and add_fields_list:
                # Joining with a pipe or newline so the LLM can distinguish attributes
                additional_fields = " | ".join(add_fields_list)
            else:
                additional_fields = 'N/A'
        
            # Construct the formatted string for the LLM
            llm_texts.append(f"""prod {i + 1}:
title: {title}
description: {desc}
additional_fields: {additional_fields}
""")
            
        return self._format_llm_output(search_keyword, llm_texts)
