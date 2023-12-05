# define the Avro schema for RequestStreamModel
request_stream_schema = """
{
  "type": "record",
  "name": "Request",
  "fields": [
    {"name": "request_id", "type": "string"},
    {"name": "requested_datetime", "type": "string"},
    {"name": "updated_datetime", "type": "string"},
    {"name": "status_description", "type": ["string", "null"], "default": "null"},
    {"name": "agency_responsible", "type": ["string", "null"], "default": "null"},
    {"name": "service_type", "type": ["string", "null"], "default": "null"},
    {"name": "service_subtype", "type": ["string", "null"], "default": "null"},
    {"name": "address", "type": ["string", "null"], "default": "null"},
    {"name": "street", "type": ["string", "null"], "default": "null"},
    {"name": "supervisor_district", "type": ["string", "null"], "default": "null"},
    {"name": "neighborhood", "type": ["string", "null"], "default": "null"},
    {"name": "police_district", "type": ["string", "null"], "default": "null"},
    {"name": "latitude", "type": ["float", "null"], "default": 0.0},
    {"name": "longitude", "type": ["float", "null"], "default": 0.0},
    {"name": "source", "type": ["string", "null"], "default": "null"}
  ]
}
"""