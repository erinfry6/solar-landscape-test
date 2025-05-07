import pandas as pd
from typing import Union

import yaml

class ProjectInfo:
    def __init__(self, file_path: str = "data/Project Information.xlsx"):
        self.file_path = file_path
        self.projects = pd.read_excel(self.file_path, sheet_name="Sheet1")

    def get_project_info(self, project_id: str) -> Union[dict, None]:
        project_info = self.projects[self.projects["Project ID Number"] == int(project_id)]
        if not project_info.empty:
            return project_info.iloc[0].to_dict()
        else:
            raise ValueError(f"Project ID {project_id} not found.")
        
    def verify_active(self, project_id: str) -> bool:
        """
        Verify if the project is active based on the Project Information sheet.
        Projects are considered active if both Project Status and Community Solar Status are "ACTIVE".
        """
        project_info = self.get_project_info(project_id)
        if project_info:
            return project_info["Project Status"] == "ACTIVE" and project_info["Community Solar Status"] == "ACTIVE"    
        return False
    

if __name__ == "__main__":
    project_info = ProjectInfo()
    project_id = "0081565"
    # info = project_info.get_project_info(project_id)
    # if info:
    #     print(f"Project Info: {info}")
    
    is_active = project_info.verify_active(project_id)
    print(f"Is Project Active: {is_active}")