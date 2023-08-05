import logging

from google.cloud import bigquery
from google.api_core import exceptions
from kafka.errors import KafkaError

logger = logging.getLogger(__name__)


def get_bq_table(bq_client: bigquery.Client, table_name: str) -> bigquery.table.Table:
    dataset_ref = bq_client.dataset(table_name.split(".")[0])
    table_ref = dataset_ref.table(table_name.split(".")[1])
    return bq_client.get_table(table_ref)


def write_bq(
    message: dict,
    bq_client: bigquery.Client,
    bq_table: bigquery.table.Table,
):

    try:
        response = bq_client.insert_rows_json(bq_table, [message])

        if len(response) == 0:
            logger.info("New rows have been added.")
        else:
            logger.error("Encountered errors while inserting rows: {}".format(response))
    except exceptions.ClientError as error:
        logger.error("BigQuery client error!")
        logger.info(f"{error}")
        raise KafkaError()