import pandas as pd
from typing import Union

import yaml

from utils import read_excel_cells

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
    
class CommunitySolar:
    def __init__(self, config_path: str = "config/project/BGE Community Solar Pilot Program.yaml"):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.project_id = self.config['project_id']
        self.metadata_config = self.config['metadata']
        self.data_config = self.config['energy_data']

    def read_metadata(self):
        """
        Load metadata from the specified Excel file and sheet.
        """
        metadata_cells = self.metadata_config['values']
        return read_excel_cells(self.metadata_config['path'], self.metadata_config['sheet'], metadata_cells)

    def process_metadata(self):
        metadata = self.read_metadata()

        # append project info to metadata
        project_info = ProjectInfo().get_project_info(self.project_id)
        metadata.update(project_info)
        return metadata

    
    def get_energy_data(self):
        """
        Load energy data from the specified Excel file and sheet.
        """
        energy_data = pd.read_excel(self.data_config['path'], sheet_name=self.data_config['sheet'], header=self.data_config['header_row'])
        rename_columns = self.data_config['column_mapping']
        if rename_columns:
            energy_data.rename(columns=rename_columns, inplace=True)
        
        return energy_data

if __name__ == "__main__":
    solar_data = CommunitySolar()
    print(solar_data.get_energy_data().columns)