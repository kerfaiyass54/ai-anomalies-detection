from ...schemas.configuration import ConfigurationSettings

DEFAULT_SETTINGS = ConfigurationSettings()


def render_configuration(settings: ConfigurationSettings) -> str:
    """Render the supported file input and Elasticsearch output settings."""
    return f'''input {{
  file {{
    path => "{settings.input_path}"
    start_position => "{settings.start_position}"
    sincedb_path => "/usr/share/logstash/data/containers.sincedb"
  }}
}}

output {{
  elasticsearch {{
    hosts => ["http://elasticsearch:9200"]
    index => "{settings.elasticsearch_index}"
  }}
}}
'''
