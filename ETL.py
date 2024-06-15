import typing
import os
import json
class ETL:
    def __init__(self, filetype: str):
        self.filetype = filetype

    

    def extract_from_directory(self) -> list[str]:
        """
        Returns a list of JSON file names within the given directory

        Parameters: 
            directoryName (str): the name of a directory containing only JSON files

        Returns:
            parsed_list (list[str]): list of file names within the directory
        """
        parsed_list = {}
        print(os.listdir(self.filetype))
        for filename in os.listdir(self.filetype):
            
            f = os.path.join(self.filetype, filename)
            if os.path.isfile(f):
                table_name = filename.split(".")[0].upper()
                parsed_list[table_name] = self.parse_JSON_list(f)
            else:
                print("Unable to find", f)
        return parsed_list
    
    def parse_JSON_list(filename: str) -> list[str]:
        """
        Returns all JSON objects in file appended to a single list

        Parameters:
            filename (str): The name of the file containing the JSON objects
        
        Returns:
            branch_list (list[str]): The list of json obects
        
        """
        branch_list = []

        with open(filename) as f:
            data = json.load(f)

        for i in data:
            branch_list.append(i)

        f.close()

        return branch_list
