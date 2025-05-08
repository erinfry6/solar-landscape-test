# Erin Fry - Solar Landscape Work Sample

## Requirements
- Docker
- Python 3.9+
- sqlite

## Assumptions
1. `Report Run Date` is unique and when combined with project_id can uniquely identify energy reports.
2. `Project Information.xlsx` schema will not change, only the solar project data sheets, which are configured in `config/project`.
3. `config/project` configuration files must follow the established format. Metadata `ProjectInfo` is designated by cell under `metadata:values:` and EnergyData columns to be included in the database are listed and mapped to SQL column names in `energy_data:column_mapping:`.

## Setup Instructions
0. Place `Project Information.xlsx` and sample data files in `data/`.

1. Build and run the Docker image:
   ```sh
   docker build -t project-energy .
   docker run -p 8000:8000 -v ./:/app/ project-energy

   ```

2. View inserted data from local commandline, saved to `./data/project_energy.db`:
   ```
   sqlite3 data/project_energy.db

   SELECT * FROM ProjectInfo;
   SELECT * FROM EnergyData;
   ```

3. To run again, you'll need to delete the .db database locally.