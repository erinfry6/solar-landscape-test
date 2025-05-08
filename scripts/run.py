import os
from process import CommunitySolar
from write import Database

if __name__ == "__main__":
    # for each .yaml in config/project, run the process and write scripts
    for config_file in os.listdir("config/project"):
        if config_file.endswith(".yaml"):
            config_path = os.path.join("config/project", config_file)
            
            # Initialize the CommunitySolar class with the current config
            solar_data = CommunitySolar(config_path=config_path)
            
            # Process metadata and energy data
            project_info = solar_data.process_metadata()
            energy_data = solar_data.process_energy_data(solar_data.project_id, report_run_date=project_info['report_run_date'])
            
            # Write to database
            db = Database("data/project_energy.db")
            db.create_tables()
            db.insert_project_info(project_info)
            try:
                db.insert_energy_data(energy_data)
                print(f"Data for {config_file} uploaded successfully.")
            except Exception as e:
                db.delete_project_info(project_info['project_id'], project_info['report_run_date'])
                db.close()
                raise Exception(f"Failed to upload energy data: {e}")
            else:
                db.close()