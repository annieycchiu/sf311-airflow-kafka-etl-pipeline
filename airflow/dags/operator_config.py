# Standard library imports
from datetime import date, timedelta

# set retrieved data date
yesterday = date.today() - timedelta(days=1)

# set directories for raw data and processed data
raw_data_dir = "<your raw data directory path>"
processed_data_dir = "<your processed data directory path>"

# Socrata API
sf_data_url = "data.sfgov.org"
sf_data_sub_uri = "vw6y-z8j6" 
sf_data_app_token = "<your Socrata API token>"
data_limit = 1000

# threshold to stop the Kafka consumer
thresh = 100