import psycopg2
from psycopg2 import Error
from tqdm import tqdm
from dotenv import dotenv_values
from faker import Faker


class PostgreConnector:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
            )
            print("Connection to PostgreSQL DB successful")
            return self.connection
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()

    def fetch_data(self, connection, query):
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        cursor.close()
        return record

    def close_connection(self, connection):
        if connection:
            connection.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection(self.connection)


def dummy_data(num_rows, start):
    activity_list = ["Reading", "Writing", "Coding", "Sleeping", "Eating"]
    # generate a list of peoples name
    fake = Faker()
    data = []
    for i in range(num_rows):
        user_id = start + i
        user_name = fake.name()
        user_activity = fake.random_element(activity_list)
        data.append((user_id, user_name, user_activity))
    return data


if __name__ == "__main__":
    try:
        config = dotenv_values(".env")
        user = config["POSTGRES_USER"]
        password = config["POSTGRES_PASSWORD"]
        database = config["POSTGRES_DB"]
        with PostgreConnector(
            user=user,
            password=password,
            host="localhost",
            port="5432",
            database=database,
        ) as postgre_connector:

            # if the table not created, create the table
            query = "CREATE TABLE IF NOT EXISTS users (user_id INT PRIMARY KEY, user_name VARCHAR(50), user_activity VARCHAR(50));"
            postgre_connector.execute_query(postgre_connector.connection, query)
            print("Table created successfully")

            # query the latest user_id from the table
            query = "SELECT MAX(user_id) FROM users;"
            record = postgre_connector.fetch_data(postgre_connector.connection, query)
            latest_user_id = record[0][0] if record[0][0] else 0

            # generate dummy data
            num_rows = 1000
            data = dummy_data(num_rows, latest_user_id + 1)

            # insert the data
            for user_id, user_name, user_activity in tqdm(data):
                query = f"INSERT INTO users (user_id, user_name, user_activity) VALUES ({user_id}, '{user_name}', '{user_activity}');"
                postgre_connector.execute_query(postgre_connector.connection, query)

    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
