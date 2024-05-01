import logging
from typing import Dict, Optional, Set, Tuple

from PIL import Image, ImageDraw, ImageChops

import pandas as pd
import RobotMap_pb2 as RobotMap
from custom_components.xiaomi_cloud_map_extractor.const import *
from google.protobuf.json_format import MessageToDict
from vacuum_map_parser_base.image_generator import ImageGenerator
from vacuum_map_parser_base.config.image_config import ImageConfig
from vacuum_map_parser_base.map_data import Area, ImageData, MapData, Obstacle, Path, Point

_LOGGER = logging.getLogger(__name__)


class IjaiImageParser(ImageGenerator):
    
    def draw_map(self, robot_map: RobotMap, width: int, height: int):
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
        image, rooms = self._draw_rooms(robot_map, image, width, height)
        import pdb; pdb.set_trace()
        cleaned_areas_layer = None
        cleaned_areas_pixels = None
        if draw_cleaned_area: # todo
            cleaned_areas_layer = Image.new('RGBA', (trimmed_width, trimmed_height))
            cleaned_areas_pixels = cleaned_areas_layer.load()
        _LOGGER.debug(f"trim_bottom = {trim_bottom}, trim_top = {trim_top}, trim_left = {trim_left}, trim_right = {trim_right}")
        return image, rooms, cleaned_areas, cleaned_areas_layer
    
    def _draw_rooms(self, robot_map: RobotMap, image: Image, width: int, height: int):
        room_chain_dicts = self._roomChain_to_df(robot_map.roomChain)
        room_images = {}
        room_coords = {}
        for room_idx in range(len(robot_map.roomDataInfo)):
            room_name = robot_map.roomDataInfo[room_idx].roomName
            color_id = robot_map.roomDataInfo[room_idx].colorId
            room_name_pos = robot_map.roomDataInfo[room_idx].roomNamePost
            room_id = robot_map.roomDataInfo[room_idx].roomId
            room_df = room_chain_dicts[room_id]
            _LOGGER.debug(f"drawing room {room_idx}: {room_name}, color_id: {color_id}, room_name_pos: {room_name_pos}")
            # room_image, room_coord = self._draw_room(room_df, room_name, color_id, width, height)  # accurate to app
            room_image, room_coord = self._draw_room(room_df, room_name, room_id, width, height)
            room_coords[room_name] = room_coord
            room_images[room_name] = room_image
            image = ImageChops.add(image, room_image, scale=1.0)
        image.save("Home.png")
        return image, room_coords

    def _draw_room(self, room_df, room_name: str, color_id: int, img_width: int, img_height: int):
        image = Image.new("RGBA", (img_width, img_height))
        draw = ImageDraw.Draw(image)
        points = [(row['x'], row['y']) for _, row in room_df.iterrows() if row['value'] is not None]
        draw.polygon(points, fill=self._palette.ROOM_COLORS[str(color_id)])
        image.save(f"room_{room_name}.png")
        return image, points
        
    def _roomChain_to_df(self, room_chains) -> Dict[str, pd.DataFrame]:
        room_chains_dict = {}
        for room_chain in room_chains:
            room_chain_dict = MessageToDict(room_chain)
            room_chains_dict[room_chain_dict["roomId"]] = pd.DataFrame(room_chain_dict["points"])
        return room_chains_dict
    