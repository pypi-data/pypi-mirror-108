import io
import logging

import avro
import avro.schema
import avro.io
import struct
import requests

from datetime import datetime

logger = logging.getLogger(__name__)


def get_schema_from_registry(schema_registry, message, schema_cache):
    schema_id = struct.unpack(">L", message.value[1:5])[0]
    if schema_id in schema_cache:
        return schema_cache[schema_id]
    else:
        schema = requests.get(schema_registry + '/schemas/ids/' + str(schema_id))
        schema_cache[schema_id] = schema
        return schema


def decode_avro_message(schema, message):
    schema = avro.schema.Parse(schema)
    bytes_reader = io.BytesIO(message.value[5:])
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(schema)
    return reader.read(decoder)


def convert_timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
