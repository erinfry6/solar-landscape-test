import pandas as pd
from typing import Union

import yaml

from utils import read_excel_cells, trim_dataframe_at_string

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
        self.project_name = self.config['project']
        self.metadata_config = self.config['metadata']
        self.data_config = self.config['energy_data']

    def read_metadata(self) -> dict:
        """
        Load metadata from the specified Excel file and sheet.
        """
        metadata_cells = self.metadata_config['values']
        return read_excel_cells(self.metadata_config['path'], self.metadata_config['sheet'], metadata_cells)

    def process_metadata(self) -> dict:
        print(f"Processing metadata for project {self.project_name}...")
        metadata = self.read_metadata()

        # append project info to metadata
        project_info = ProjectInfo().get_project_info(self.project_id)

        # rename project_info keys
        rename_keys = {
            "Project ID Number": "project_id",
            "Project Status": "project_status",
            "Community Solar Status": "community_solar_status",
            "Maximum Monthyl kWh Production": "maximum_kwh_production",
        }
        project_info = {rename_keys.get(k, k): v for k, v in project_info.items()}
        metadata.update(project_info)
        metadata['project_name'] = self.project_name
        return metadata

    
    def get_energy_data(self) -> pd.DataFrame:
        """
        Load energy data from the specified Excel file and sheet.
        """
        energy_data = pd.read_excel(self.data_config['path'], sheet_name=self.data_config['sheet'], header=self.data_config['header_row'])
        select_columns = self.data_config['column_mapping']

        # return only selected columns and rename them
        energy_data = energy_data[select_columns.keys()]
        rename_columns = {col: select_columns[col] for col in energy_data.columns if col in select_columns}
        energy_data = energy_data.rename(columns=rename_columns)
        
        return energy_data
    
    def process_energy_data(self, project_id: int, report_run_date: str) -> pd.DataFrame:
        energy_data = self.get_energy_data()
        trimmed_data = trim_dataframe_at_string(energy_data)
        
        trimmed_data['project_id'] = project_id
        trimmed_data['report_run_date'] = report_run_date

        # assert allocation_percentages > 0
        allocation_percentages = trimmed_data['allocation_percentage'].apply(lambda x: True if x > 0 else False)
        #fill na with 0
        allocation_percentages = allocation_percentages.fillna(0)
        assert allocation_percentages.apply(lambda x: True if x >= 0 else False).all(), "Allocation percentages must be greater than 0"
        
        return trimmed_data