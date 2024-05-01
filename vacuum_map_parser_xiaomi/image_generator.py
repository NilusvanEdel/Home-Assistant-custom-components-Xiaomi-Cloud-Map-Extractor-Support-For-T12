import logging
from typing import Dict, Optional, Set, Tuple

from PIL import Image
from PIL.Image import Image as ImageType

import RobotMap_pb2 as RobotMap
from custom_components.xiaomi_cloud_map_extractor.const import *
from google.protobuf.json_format import MessageToDict
from vacuum_map_parser_base.image_generator import ImageGenerator
from vacuum_map_parser_base.config.image_config import ImageConfig
from vacuum_map_parser_base.map_data import Area, ImageData, MapData, Obstacle, Path, Point

_LOGGER = logging.getLogger(__name__)


class IjaiImageParser(ImageGenerator):
    MAP_OUTSIDE = 0x00
    MAP_WALL = 0xff
    MAP_SCAN = 0x01
    MAP_NEW_DISCOVERED_AREA = 0x02
    MAP_ROOM_MIN = 10
    MAP_ROOM_MAX = 59
    MAP_SELECTED_ROOM_MIN = 60
    MAP_SELECTED_ROOM_MAX = 109
    
    def draw_map(self, robot_map: RobotMap, width: int, height: int) -> Tuple[ImageType, Dict[int, Tuple[int, int, int, int]], Set[int], Optional[ImageType]]:
        fields = robot_map.DESCRIPTOR.fields_by_name.keys()  # todo: del later
        draw_cleaned_area: bool = DRAWABLE_CLEANED_AREA in self._drawables
        rooms = {}
        cleaned_areas = set()
        scale = self._image_config[CONF_SCALE]
        trim_left = int(self._image_config[CONF_TRIM][CONF_LEFT] * width / 100)
        trim_right = int(self._image_config[CONF_TRIM][CONF_RIGHT] * width / 100)
        trim_top = int(self._image_config[CONF_TRIM][CONF_TOP] * height / 100)
        trim_bottom = int(self._image_config[CONF_TRIM][CONF_BOTTOM] * height / 100)
        trimmed_height = height - trim_top - trim_bottom
        trimmed_width = width - trim_left - trim_right
        if trimmed_width == 0 or trimmed_height == 0:
            return self.create_empty_map_image(), rooms, cleaned_areas, None
        image = Image.frombytes("L", (trimmed_width, trimmed_height), robot_map.mapData.mapData).convert("RGBA")
        pixels = image.load()
        cleaned_areas_layer = None
        cleaned_areas_pixels = None
        if draw_cleaned_area: # todo
            cleaned_areas_layer = Image.new('RGBA', (trimmed_width, trimmed_height))
            cleaned_areas_pixels = cleaned_areas_layer.load()
        _LOGGER.debug(f"trim_bottom = {trim_bottom}, trim_top = {trim_top}, trim_left = {trim_left}, trim_right = {trim_right}")
        import pdb; pdb.set_trace()
        return image, rooms, cleaned_areas, cleaned_areas_layer
    
    def _draw_rooms(self, robot_map: RobotMap):
        room_chain_dicts = [MessageToDict(item) for item in robot_map.roomChain]
        for room_idx in len(robot_map.roomDataInfo):
            room_name = robot_map.roomDataInfo[room_idx].get("roomName", "Unknown")
            color_id = robot_map.roomDataInfo[room_idx].get("colorID", 0)
            room_name_pos = robot_map.roomDataInfo[room_idx].get("roomNamePost", None)
            room_chain = robot_map.roomChain[0]
            _LOGGER.debug(f"drawing room {room_idx}: {room_name}, color_id: {color_id}, room_name_pos: {room_name_pos}, room_chain: {room_chain}")

    def _draw_room():