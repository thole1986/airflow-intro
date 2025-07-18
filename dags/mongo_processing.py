from airflow.sdk import dag, task
from airflow.providers.mongo.hooks.mongo import MongoHook
import logging

logger = logging.getLogger(__name__)


@dag(schedule=None, catchup=False)
def testing_mongo_connection():
    @task
    def read_from_mongo():
        hook = MongoHook(conn_id='mongo_default')
        client = hook.get_conn()
        # ✅ Chọn database và collection
        db = client['tariff_service']
        collection = db['custom_duties']
        logger.info("Connected to Mongo and selected collection")
        docs = collection.find()
        found = False
        for doc in docs:
            logger.info(f"Document: {doc}")
            found = True

        if not found:
            logger.warning("No documents found!")

    read_from_mongo()

dag_instance = testing_mongo_connection()
