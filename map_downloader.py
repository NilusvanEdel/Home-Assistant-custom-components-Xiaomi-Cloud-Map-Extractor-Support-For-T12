from custom_components.xiaomi_cloud_map_extractor.vacuum_platforms.xiaomi_cloud_connector import *

# pip install git+https://github.com/rytilahti/python-miio.git
from miio.miot_device import MiotDevice

# Note: you will need Microsoft C++ Build Tools to install this

import logging

from typing import Optional
from map_decrypter import unGzipCommon
import requests
import zlib
import yaml
import os
import base64
import PIL
import PIL.Image
import RobotMap_pb2 as RobotMap


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


def save_map(inflated_map: bytes, map_name: str, logger: logging.Logger):
    # Save routines
    try:
        mapsdir = os.path.join(".", "maps")
        if not os.path.exists(mapsdir):
            os.makedirs(mapsdir)
        base_map_name = os.path.join(mapsdir, f"{map_name}.decrypted.map")
        # with open(base_map_name, 'wb') as file:
        #     file.write(deflated_map)
        with open(base_map_name + ".decompressed", "wb") as file:
            file.write(inflated_map)

        robot_map = RobotMap.RobotMap()
        robot_map.ParseFromString(inflated_map)

        imageBytes = robot_map.mapData.mapData
        imageWidth = robot_map.mapHead.sizeX
        imageHeight = robot_map.mapHead.sizeY
        PIL.Image.frombytes("L", (imageWidth, imageHeight), imageBytes).save(
            os.path.join(mapsdir, f"{map_name}.decrypted.map.bmp"), "bmp"
        )
        logger.info("Done, saved")
    except:
        logger.error("Save failed")


def main():
    account_info = yaml.safe_load(open("camera.yaml", "r"))[0]
    map_name = "0"  # index of map, where 0 is current selected map in Mi Home

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    connector = XiaomiCloudConnector(account_info["username"], account_info["password"])
    if connector.login():
        country, user_id, device_id, model, mac = connector.get_device_details(
            account_info["token"], account_info["country"]
        )

        wifi_info_sn = None
        device = MiotDevice(account_info["host"], account_info["token"])

        # property 7, 45 (sweep -> multi-prop-vacuum) https://home.miot-spec.com/spec/xiaomi.vacuum.b106eu and it also on https://home.miot-spec.com/spec/xiaomi.vacuum.c103
        got_from_vacuum = device.get_property_by(7, 45)

        for prop in got_from_vacuum[0]["value"].split(","):
            cleaned_prop = str(prop).replace('"', "")

            if str(user_id) in cleaned_prop:
                wifi_info_sn = cleaned_prop.split(";")[0]
            elif (
                len(cleaned_prop) == 18
                and cleaned_prop.isalnum()
                and cleaned_prop.isupper()
            ):
                wifi_info_sn = cleaned_prop

        if wifi_info_sn == None:
            raise Exception("Get wifi_info_sn failed")
        logger.info("wifi_info_sn: %s", wifi_info_sn)

        url = get_map_url(
            connector, account_info["country"], str(user_id), device_id, map_name
        )
        req = requests.get(url)

        # Decrypt routine

        try:
            hexstr = unGzipCommon(
                req.content, wifi_info_sn, str(user_id), device_id, model, mac
            )
            deflated_map = bytes.fromhex(hexstr)  # Deflated means compressed
        except Exception as e:
            logger.critical("Decryption failed: %s" % e)
            # exit(1)

        # Save routines
        try:
            if not os.path.exists("maps"):
                os.makedirs("maps")
            base_encryptedmap_name = os.path.join(
                ".", "maps", f"{map_name}.encrypted.map"
            )
            base_b64decoded_encryptedmap_name = os.path.join(
                ".", "maps", f"{map_name}.b64decoded.encrypted.map"
            )
            base_decryptedmap_name = os.path.join(
                ".", "maps", f"{map_name}.decrypted.map"
            )

            with open(base_encryptedmap_name, "wb") as file:
                file.write(req.content)
            with open(base_b64decoded_encryptedmap_name, "wb") as file:
                file.write(base64.b64decode(req.content))
            with open(base_decryptedmap_name, "wb") as file:
                file.write(deflated_map)

            inflated_map = zlib.decompress(deflated_map)
            with open(base_decryptedmap_name + ".decompressed", "wb") as file:
                file.write(inflated_map)
            save_map(inflated_map, map_name, logger)

            logger.info("Done, saved")
        except:
            logger.error("Save failed")
    else:
        logger.error("Login failed :(")


if __name__ == "__main__":
    main()
