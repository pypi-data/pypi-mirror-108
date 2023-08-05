from knada_kafka_consumer.consumer.consumer import ConsumerApp


def get_consumer_app(topic: str,
                     kafka_brokers: list,
                     sasl_user: str,
                     sasl_password: str,
                     kafka_ca_path: str,
                     kafka_group_id: str,
                     kafka_schema_registry: str,
                     bq_table: str,
                     google_creds: str = None):

    app = ConsumerApp(topic=topic,
                      kafka_brokers=kafka_brokers,
                      sasl_user=sasl_user,
                      sasl_password=sasl_password,
                      kafka_ca_path=kafka_ca_path,
                      kafka_group_id=kafka_group_id,
                      kafka_schema_registry=kafka_schema_registry,
                      bq_table=bq_table,
                      google_creds=google_creds)

    return app.app
