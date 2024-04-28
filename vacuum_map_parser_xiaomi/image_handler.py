import logging
from typing import Dict, Optional, Set, Tuple

from PIL import Image
from PIL.Image import Image as ImageType

from custom_components.xiaomi_cloud_map_extractor.const import *
from vacuum_map_parser_base.config.color import Color
from vacuum_map_parser_base.image_generator import ImageGenerator
from vacuum_map_parser_base.config.image_config import ImageConfig
from vacuum_map_parser_base.map_data import Area, ImageData, MapData, Obstacle, Path, Point
from .parsing_buffer import ParsingBuffer

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
    
    def draw_map(self, map_data: MapData) \
            -> Tuple[ImageType, Dict[int, Tuple[int, int, int, int]], Set[int], Optional[ImageType]]:
        palette = {\
                    IjaiImageParser.MAP_OUTSIDE: self._get_color(COLOR_MAP_OUTSIDE),\
                    IjaiImageParser.MAP_WALL: self._get_color(COLOR_MAP_WALL_V2),\
                    IjaiImageParser.MAP_SCAN: self._get_color(COLOR_SCAN),\
                    IjaiImageParser.MAP_NEW_DISCOVERED_AREA: self._get_color(COLOR_NEW_DISCOVERED_AREA)}
        rooms = {}
        cleaned_areas = set()
        scale = self.image_config[CONF_SCALE]
        trim_left = int(self.image_config[CONF_TRIM][CONF_LEFT] * width / 100)
        trim_right = int(self.image_config[CONF_TRIM][CONF_RIGHT] * width / 100)
        trim_top = int(self.image_config[CONF_TRIM][CONF_TOP] * height / 100)
        trim_bottom = int(self.image_config[CONF_TRIM][CONF_BOTTOM] * height / 100)
        trimmed_height = height - trim_top - trim_bottom
        trimmed_width = width - trim_left - trim_right
        if trimmed_width == 0 or trimmed_height == 0:
            return self.create_empty_map_image(colors), rooms, cleaned_areas, None
        image = Image.new('RGBA', (trimmed_width, trimmed_height))
        pixels = image.load()
        cleaned_areas_layer = None
        cleaned_areas_pixels = None
        if draw_cleaned_area:
            cleaned_areas_layer = Image.new('RGBA', (trimmed_width, trimmed_height))
            cleaned_areas_pixels = cleaned_areas_layer.load()
        _LOGGER.debug(f"trim_bottom = {trim_bottom}, trim_top = {trim_top}, trim_left = {trim_left}, trim_right = {trim_right}")
        buf.skip('trim_bottom', trim_bottom * width)
        unknown_pixels = set()
        _LOGGER.debug(f"buffer: [{buf._offs:#x}] = {buf.peek_uint32("some_int32")}")
        for img_y in range(trimmed_height):
            buf.skip('trim_left', trim_left)
            for img_x in range(trimmed_width):
                pixel_type = buf.get_uint8('pixel')
                x = img_x
                y = trimmed_height - 1 - img_y
                if pixel_type in palette.keys():
                    pixels[x, y] = palette[pixel_type]
                elif IjaiImageParser.MAP_ROOM_MIN <= pixel_type <= IjaiImageParser.MAP_SELECTED_ROOM_MAX:
                    room_x = img_x + trim_left
                    room_y = img_y + trim_bottom
                    if pixel_type < IjaiImageParser.MAP_SELECTED_ROOM_MIN:
                        room_number = pixel_type
                    else:
                        room_number = pixel_type - IjaiImageParser.MAP_SELECTED_ROOM_MIN + IjaiImageParser.MAP_ROOM_MIN
                        cleaned_areas.add(room_number)
                        if draw_cleaned_area:
                            cleaned_areas_pixels[x, y] = ImageHandler.__get_color__(COLOR_CLEANED_AREA, colors)
                    if room_number not in rooms:
                        rooms[room_number] = (room_x, room_y, room_x, room_y)
                    else:
                        rooms[room_number] = (min(rooms[room_number][0], room_x),
                                              min(rooms[room_number][1], room_y),
                                              max(rooms[room_number][2], room_x),
                                              max(rooms[room_number][3], room_y))
                    default = ImageHandler.ROOM_COLORS[room_number % len(ImageHandler.ROOM_COLORS)]
                    pixels[x, y] = ImageHandler.__get_color__(f"{COLOR_ROOM_PREFIX}{room_number}", colors, default)
                else:
                    pixels[x, y] = ImageHandler.__get_color__(COLOR_UNKNOWN, colors)
                    unknown_pixels.add(pixel_type)
                    _LOGGER.debug(f"unknown pixel [{x},{y}] = {pixel_type}")
            buf.skip('trim_right', trim_right)
        buf.skip('trim_top', trim_top * width)
        if self.image_config["scale"] != 1 and trimmed_width != 0 and trimmed_height != 0:
            image = image.resize((int(trimmed_width * scale), int(trimmed_height * scale)), resample=Image.NEAREST)
            if draw_cleaned_area:
                cleaned_areas_layer = cleaned_areas_layer.resize(
                    (int(trimmed_width * scale), int(trimmed_height * scale)), resample=Image.NEAREST)
        if len(unknown_pixels) > 0:
            _LOGGER.warning('unknown pixel_types: %s', unknown_pixels)
        return image, rooms, cleaned_areas, cleaned_areas_layer