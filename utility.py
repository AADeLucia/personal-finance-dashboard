import base64
import io
import pandas as pd 


class Utility:
    def __init__(self):
        return

    
    def parse_content(self, contents, filename):
        """
        Copied from Dash upload page
        """
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
        except Exception as e:
            print(e)
        return df
    
    