from typing import Optional

from custom_components.xiaomi_cloud_map_extractor.vacuum_platforms.xiaomi_cloud_connector import (
    XiaomiCloudConnector,
)
from vacuum_map_parser_xiaomi.map_data_parser import MapDataParserIjai
from vacuum_map_parser_xiaomi.map_decrypter import unGzipCommon

from .vacuum_base import VacuumConfig
from .vacuum_v2 import XiaomiCloudVacuumV2


class ViomiCloudVacuum(XiaomiCloudVacuumV2):

    def __init__(self, vacuum_config: VacuumConfig):
        super().__init__(vacuum_config)
        self._viomi_map_data_parser = MapDataParserIjai(
            vacuum_config.palette,
            vacuum_config.sizes,
            vacuum_config.drawables,
            vacuum_config.image_config,
            vacuum_config.texts,
        )

    @property
    def map_archive_extension(self) -> str:
        return "b64"

    @property
    def map_data_parser(self) -> MapDataParserIjai:
        return self._viomi_map_data_parser

    def get_map_url(
        connector: XiaomiCloudConnector,
        country: str,
        _user_id: str,
        _device_id: str,
        map_name: str,
    ) -> Optional[str]:
        url = connector.get_api_url(country) + "/v2/home/get_interim_file_url_pro"
        params = {"data": f'{{"obj_name":"{_user_id}/{_device_id}/{map_name}"}}'}
        api_response = connector.execute_api_call_encrypted(url, params)
        if (
            api_response is None
            or "result" not in api_response
            or "url" not in api_response["result"]
        ):
            return None
        return api_response["result"]["url"]

    def decode_and_parse(self, data):
        self.decrypt_map(
            self,
            data=data,
            wifi_info_sn=self._wifi_info_sn,
            user_id=self._user_id,
            device_id=self._user_id,
            model=self.model,
            mac=self._mac,
        )

    def decrypt_map(
        self,
        data: bytes,
        wifi_info_sn: str,
        user_id: str,
        device_id: str,
        model: str,
        mac: str,
    ):
        return unGzipCommon(
            data=data,
            wifi_info_sn=wifi_info_sn,
            owner_id=str(user_id),
            device_id=device_id,
            model=model,
            device_mac=mac,
        )
