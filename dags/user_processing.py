from airflow.sdk import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk.bases.sensor import PokeReturnValue

@dag
def user_processing():
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="postgres",
        sql="""
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY,
            firstname VARCHAR(255),
            lastname VARCHAR(255),
            email VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    @task.sensor(poke_interval=30, timeout=300)
    def is_api_available() -> PokeReturnValue:
        import requests
        try:
            response = requests.get(
                "https://raw.githubusercontent.com/marclamberti/datasets/refs/heads/main/fakeuser.json"
            )
            print("API status_code:", response.status_code)
            if response.status_code == 200:
                fake_user = response.json()
                print("Fetched fake user:", fake_user)
                condition = True
            else:
                print("Failed to fetch user, status_code:", response.status_code)
                fake_user = None
                condition = False
        except Exception as e:
            print("Exception when calling API:", str(e))
            fake_user = None
            condition = False
        return PokeReturnValue(is_done=condition, xcom_value=fake_user)


    @task
    def extract_user(fake_user):
        print("FAKE USER DATA IN extract_user:", fake_user)
        if not fake_user:
            raise ValueError("No fake_user data received from sensor.")
        return {
            "id": fake_user.get("id"),
            "firstname": fake_user.get("personalInfo", {}).get("firstName"),
            "lastname": fake_user.get("personalInfo", {}).get("lastName"),
            "email": fake_user.get("personalInfo", {}).get("email"),
        }

    @task
    def process_user(user_info):
        import csv
        if not user_info:
            raise ValueError("No user_info provided to process_user.")
        
        with open("/tmp/user_info.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=user_info.keys())
            writer.writeheader()
            writer.writerow(user_info)

    fake_user = is_api_available()
    user_info = extract_user(fake_user)
    process_user(user_info)

user_processing()
