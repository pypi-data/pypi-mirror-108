"""
Module to handle datasets IO
"""
import json
import logging
from datetime import datetime
from typing import List, Dict, AnyStr

from azure.core.exceptions import HttpResponseError
from azure.storage.filedatalake import DataLakeFileClient as DataLakeFileClientSync

from ..core.enums import TimeResolution
from ..core.azure_client_authorization import AzureCredential
from ..core.io import get_file_path_with_respect_to_time_resolution

logger = logging.getLogger(__name__)


class DataSets:
    """
    Class to handle datasets IO
    """
    # pylint: disable=too-many-arguments
    def __init__(self,
                 account_url: str,
                 filesystem_name: str,
                 source: str,
                 destination: str,
                 credential: AzureCredential,
                 time_resolution: TimeResolution,):

        self.account_url = account_url
        self.filesystem_name = filesystem_name

        self.source = source
        self.destination = destination

        self.credential = credential
        self.time_resolution = time_resolution

    def read_events_from_destination(self, date: datetime) -> List:
        """
        Read events from destination corresponding a given date
        """

        sub_file_path = get_file_path_with_respect_to_time_resolution(date, self.time_resolution, "data.json")
        file_path = f'{self.destination}/{sub_file_path}'

        with DataLakeFileClientSync(self.account_url,
                                    self.filesystem_name, file_path,
                                    credential=self.credential) as file_client:

            file_content = file_client.download_file().readall()
            return json.loads(file_content)

    def upload_events_to_destination_json(self, date: datetime, events: List[Dict]):
        """
        Uploads events to destination based on the given date
        """
        sub_file_path = get_file_path_with_respect_to_time_resolution(date, self.time_resolution, "data.json")
        file_path = f'{self.destination}/{sub_file_path}'

        data = json.dumps(events)
        with DataLakeFileClientSync(self.account_url,
                                    self.filesystem_name,
                                    file_path,
                                    credential=self.credential) as file_client:
            try:
                file_client.upload_data(data, overwrite=True)
            except HttpResponseError as error:
                message = f'({type(error).__name__}) Problems uploading data file: {error}'
                logger.error(message)
                raise Exception(message) from error

    def upload_data_to_destination(self, date: datetime, data: AnyStr, filename: str):
        """
        Uploads arbitrary `AnyStr` data to destination based on the given date
        """
        sub_file_path = get_file_path_with_respect_to_time_resolution(date, self.time_resolution, filename)
        file_path = f'{self.destination}/{sub_file_path}'

        with DataLakeFileClientSync(self.account_url,
                                    self.filesystem_name,
                                    file_path,
                                    credential=self.credential) as file_client:
            try:
                file_client.upload_data(data, overwrite=True)
            except HttpResponseError as error:
                message = f'({type(error).__name__}) Problems uploading data file: {error}'
                logger.error(message)
                raise Exception(message) from error
