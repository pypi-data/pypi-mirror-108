import json
import threading
import datetime
import logging

from starlette.responses import JSONResponse
from fastapi import FastAPI
from starlette import status
from kafka import KafkaConsumer
from kafka.errors import KafkaError, NoBrokersAvailable
from google.cloud import bigquery
from google.oauth2 import service_account
from knada_kafka_consumer.bq import bigquery_writer
from knada_kafka_consumer.kafka import kafka


class ConsumerApp:

    def __init__(self, topic: str,
                 kafka_brokers: list,
                 sasl_user: str,
                 sasl_password: str,
                 kafka_ca_path: str,
                 kafka_group_id: str,
                 kafka_schema_registry: str,
                 bq_table: str,
                 google_creds: str = None
                 ):
        self._schema_cache = {}
        self._schema_registry = kafka_schema_registry
        self._topic = topic
        self._kafka_brokers = kafka_brokers
        self._sasl_user = sasl_user
        self._sasl_password = sasl_password
        self._kafka_ca_path = kafka_ca_path
        self._kafka_group_id = kafka_group_id
        self._bq_table = bq_table
        self._google_creds = google_creds
        self._app = FastAPI()
        self._is_alive = True
        self._is_ready = False
        self.add_endpoints()
        self._logger = logging.getLogger(__name__)
        threading.Thread(target=self.read_topic, daemon=True).start()

    @property
    def app(self):
        return self._app

    def read_topic(self):
        consumer = self.create_consumer()
        self._logger.info("Kafka initialized")
        bq_client = self.create_bq_client()
        bq_table = bigquery_writer.get_bq_table(bq_client=bq_client,
                                                table_name=self._bq_table)
        self._logger.info("BigQuery connection established")
        self._is_ready = True

        try:
            for mesg in consumer:
                message = self.format_message(mesg)
                bigquery_writer.write_bq(message=message,
                                         bq_client=bq_client,
                                         bq_table=bq_table)
                consumer.commit()
                self._logger.info(
                    f"Wrote message with timestamp {kafka.convert_timestamp_to_datetime(mesg.timestamp)}"
                    f"to bigquery table {bq_table.dataset_id}.{bq_table.table_id}"
                )
        except KafkaError:
            self._is_alive = False

        self._logger.info("Kafka consumer stopped. Restarting app.")
        self._is_alive = False
        raise KafkaError()

    def healthyness(self):
        if self._is_alive:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": f"ok"})
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"Status": f"Unhealthy"},
            )

    def readiness(self):
        if self._is_ready:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": f"ok"})
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"Status": f"NotReady"},
            )

    @staticmethod
    def metrics():
        return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": f"Not implemented"})

    def add_endpoints(self):
        self._app.add_api_route(path="/metrics", endpoint=self.metrics)
        self._app.add_api_route(path="/is-alive", endpoint=self.healthyness)
        self._app.add_api_route(path="/is-ready", endpoint=self.readiness)

    def create_bq_client(self) -> bigquery.Client:
        if not self._google_creds:
            client = bigquery.Client()
        else:
            creds = service_account.Credentials.from_service_account_info(json.loads(self._google_creds))
            client = bigquery.Client(creds.project_id, credentials=creds)

        return client

    def create_consumer(self) -> KafkaConsumer:
        try:
            consumer = KafkaConsumer(self._topic,
                                     bootstrap_servers=self._kafka_brokers,
                                     security_protocol='SASL_SSL',
                                     sasl_mechanism="PLAIN",
                                     sasl_plain_username=self._sasl_user,
                                     sasl_plain_password=self._sasl_password,
                                     ssl_cafile=self._kafka_ca_path,
                                     auto_offset_reset="earliest",
                                     group_id=self._kafka_group_id,
                                     enable_auto_commit=False,
                                     api_version_auto_timeout_ms=20000)
        except NoBrokersAvailable:
            self._logger.error("Kafka initialization error. Restarting app.")
            self._is_alive = False
        else:
            return consumer

    def format_message(self, message) -> dict:

        schema_res = kafka.get_schema_from_registry(schema_registry=self._schema_registry, message=message, schema_cache=self._schema_cache)
        try:
            schema = schema_res.json()["schema"]
        except KeyError:
            decoded_message = json.loads(message.value)
        else:
            decoded_message = kafka.decode_avro_message(schema, message)

        return {"kafka_offset": message.offset,
                "kafka_partition": message.partition,
                "kafka_timestamp": message.timestamp,
                "kafka_topic": self._topic,
                "message": json.dumps(decoded_message),
                "loaded": int(datetime.datetime.now().timestamp())}
