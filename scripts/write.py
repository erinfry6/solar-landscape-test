import sqlite3
import pandas as pd


class Database:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Create tables if they don't exist
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProjectInfo (
            project_id INTEGER NOT NULL,
            project_name TEXT NOT NULL,
            project_status TEXT,
            community_solar_status TEXT,
            maximum_kwh_production DECIMAL,
            report_run_date TEXT NOT NULL,
            period_start_date TEXT,
            period_end_date TEXT,
            account_id INTEGER,
            account_name TEXT,
            electric_choice_id INTEGER,
            bge_csegs_pilot_project_id INTEGER,
            notes TEXT,
            some_other_field TEXT,
            UNIQUE(project_id, report_run_date)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS EnergyData (
            project_id INTEGER NOT NULL,
            report_run_date TEXT NOT NULL,
            subscriber_choice_id DECIMAL,
            multiple_cseg_allocations TEXT,
            allocation_percentage DECIMAL,
            actual_kwh_allocated DECIMAL,
            initial_balance_kwh DECIMAL,
            kwh_allocated_from_all_subscriptions DECIMAL,
            subscriber_billed_usage DECIMAL,
            adjustment_kwh DECIMAL,
            final_balance_kwh DECIMAL,
            community_solar_adjustment DECIMAL,
            tou_usage_on_peak_kwh DECIMAL,
            tou_usage_intermediate_peak_kwh DECIMAL,
            tou_usage_off_peak_kwh DECIMAL,
            FOREIGN KEY (project_id) REFERENCES ProjectInfo (project_id),
            FOREIGN KEY (report_run_date) REFERENCES ProjectInfo (report_run_date),
            UNIQUE(project_id, report_run_date, subscriber_choice_id)
        )
        ''')

    def _process_SQLiteError(self, e, table_name: str):
        if 'UNIQUE' in str(e):
            raise ValueError(f"You've already uploaded data into {table_name} - {e}")
        elif 'NOT NULL' in str(e):
            raise ValueError(f"Error inserting {table_name} - the following field is required: {e}")
        else:
            raise ValueError(f"IntegrityError: {e}")
    
    def insert_project_info(self, project_info: dict):
        
        df = pd.DataFrame([project_info])
        try:
            df.to_sql('ProjectInfo', self.conn, if_exists='append', index=False, method='multi')
        except sqlite3.IntegrityError as e:
            self._process_SQLiteError(e, 'ProjectInfo')


    def insert_energy_data(self, energy_data: pd.DataFrame):
        # Ensure the DataFrame has the minimal required columns
        required_columns = [
            'project_id', 'report_run_date', 'subscriber_choice_id', 
            'allocation_percentage', 'actual_kwh_allocated', 
            'kwh_allocated_from_all_subscriptions', 'subscriber_billed_usage',
            'adjustment_kwh', 'final_balance_kwh', 'community_solar_adjustment'
        ]
        
        if not all(col in energy_data.columns for col in required_columns):
            raise ValueError(f"Energy data is missing required column: {', '.join([col for col in required_columns if col not in energy_data.columns])}")

        try:
            energy_data.to_sql('EnergyData', self.conn, if_exists='append', index=False, method='multi')
        except sqlite3.IntegrityError as e:
            self._process_SQLiteError(e, 'EnergyData')


    def close(self):
        self.conn.commit()
        self.conn.close()