from googleapiclient import discovery
from google.oauth2 import service_account


def init_dataflow_service(GCP_SERVICE_ACCOUNT: str):
    credentials = service_account.Credentials.from_service_account_file(
        GCP_SERVICE_ACCOUNT,
        scopes=['https://www.googleapis.com/auth/cloud-platform', 'https://www.googleapis.com/auth/compute'])
    dataflow_service = discovery.build('dataflow', 'v1b3', credentials=credentials)
    return dataflow_service
