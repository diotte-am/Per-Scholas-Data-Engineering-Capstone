import json
import os

class JSON_util():
    def __init__(self):
        pass

    def parse_JSON(self, name):
        branch_list = []
        with open(name) as f:
            data = json.load(f)
        for i in data:
            branch_list.append(i)
        f.close()
        return branch_list

    def extract(self):
        """
        Returns a dictionary of JSON file names within the given directory

        Parameters: 
            directoryName (str): the name of a directory containing only JSON files

        Returns:
            parsed_list (list[str]): list of file names within the directory
        """
        parsed_dict = {}
        # iterate thru every json in the directory
        for filename in os.listdir("json"):
            f = os.path.join("json", filename)
            if os.path.isfile(f):
                table_name = filename.split(".")[0].upper()
                # extract each JSON object in the given file
                parsed_dict[table_name] = self.parse_JSON(f)
            else:
                print("Unable to find", f)
        return parsed_dict