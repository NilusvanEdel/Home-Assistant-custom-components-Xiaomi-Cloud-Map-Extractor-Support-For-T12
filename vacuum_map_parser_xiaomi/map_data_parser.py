import logging
import math
from typing import Dict, List, Optional, Set, Tuple


import RobotMap_pb2 as RobotMap
from vacuum_map_parser_base.map_data import Area, ImageData, MapData, Path, Point, Room, Wall, Zone
from vacuum_map_parser_base.map_data_parser import MapDataParser
from custom_components.xiaomi_cloud_map_extractor.const import *
from vacuum_map_parser_base.config.color import ColorsPalette
from vacuum_map_parser_base.config.color import Color
from vacuum_map_parser_base.config.drawable import Drawable
from vacuum_map_parser_base.config.image_config import ImageConfig
from vacuum_map_parser_base.config.size import Size, Sizes
from vacuum_map_parser_base.config.text import Text
from .image_generator import IjaiImageParser

_LOGGER = logging.getLogger(__name__)


class MapDataParserIjai(MapDataParser):
    FEATURE_ROBOT_STATUS = 0x00000001
    FEATURE_IMAGE = 0x00000002
    FEATURE_HISTORY = 0x00000004
    FEATURE_CHARGE_STATION = 0x00000008
    FEATURE_RESTRICTED_AREAS = 0x00000010
    FEATURE_CLEANING_AREAS = 0x00000020
    FEATURE_NAVIGATE = 0x00000040
    FEATURE_REALTIME = 0x00000080
    FEATURE_ROOMS = 0x00001000

    POSITION_UNKNOWN = 1100

    def __init__(
        self,
        palette: ColorsPalette,
        sizes: Sizes,
        drawables: list[Drawable],
        image_config: ImageConfig,
        texts: list[Text],
    ):
        super().__init__(palette, sizes, drawables, image_config, texts)
        self._image_parser = IjaiImageParser(palette, sizes, drawables, image_config, texts)

    def parse(self, raw: bytes, *args, **kwargs) -> MapData:
        map_data = MapData(0, 1)
        robot_map = RobotMap.RobotMap()
        robot_map.ParseFromString(raw)
        fields = robot_map.DESCRIPTOR.fields_by_name.keys()

        feature_flags = MapDataParserIjai.FEATURE_IMAGE
        if feature_flags & MapDataParserIjai.FEATURE_IMAGE != 0:
            mHead = robot_map.mapHead
            image = self._image_parser.draw_map(robot_map, mHead.sizeX, mHead.sizeX)
            cleaned_areas_layer = None # todo
            map_data.image = ImageData(size=mHead.sizeX * mHead.sizeY,
                                       top=0,  # This is a placeholder. Replace with your actual value.
                                       left=0,  # This is a placeholder. Replace with your actual value.
                                       height=mHead.sizeY,
                                       width=mHead.sizeX,
                                       image_config=self._image_config,
                                       data=data,
                                       img_transformation=img_transformation,
                                       additional_layers={DRAWABLE_CLEANED_AREA: cleaned_areas_layer}  # This is a placeholder. Replace with your actual value if any.
                            )
            # map_data.rooms, map_data.cleaned_rooms

        if feature_flags & MapDataParserIjai.FEATURE_HISTORY != 0:
            MapDataParserIjai.parse_section(buf, 'history', map_id)
            map_data.path = MapDataParserIjai.parse_history(buf)

        if feature_flags & MapDataParserIjai.FEATURE_CHARGE_STATION != 0:
            MapDataParserIjai.parse_section(buf, 'charge_station', map_id)
            map_data.charger = MapDataParserIjai.parse_position(buf, 'pos', with_angle=True)
            _LOGGER.debug('pos: %s', map_data.charger)

        if feature_flags & MapDataParserIjai.FEATURE_RESTRICTED_AREAS != 0:
            MapDataParserIjai.parse_section(buf, 'restricted_areas', map_id)
            map_data.walls, map_data.no_go_areas = MapDataParserIjai.parse_restricted_areas(buf)

        if feature_flags & MapDataParserIjai.FEATURE_CLEANING_AREAS != 0:
            MapDataParserIjai.parse_section(buf, 'cleaning_areas', map_id)
            map_data.zones = MapDataParserIjai.parse_cleaning_areas(buf)

        if feature_flags & MapDataParserIjai.FEATURE_NAVIGATE != 0:
            MapDataParserIjai.parse_section(buf, 'navigate', map_id)
            buf.skip('unknown1', 4)
            map_data.goto = MapDataParserIjai.parse_position(buf, 'pos')
            foo = buf.get_float32('foo')
            _LOGGER.debug('pos: %s, foo: %f', map_data.goto, foo)

        if feature_flags & MapDataParserIjai.FEATURE_REALTIME != 0:
            MapDataParserIjai.parse_section(buf, 'realtime', map_id)
            buf.skip('unknown1', 5)
            map_data.vacuum_position = MapDataParserIjai.parse_position(buf, 'pos', with_angle=True)
            _LOGGER.debug('pos: %s', map_data.vacuum_position)

        if feature_flags & 0x00000800 != 0:
            MapDataParserIjai.parse_section(buf, 'unknown1', map_id)
            MapDataParserIjai.parse_unknown_section(buf)

        if feature_flags & MapDataParserIjai.FEATURE_ROOMS != 0:
            MapDataParserIjai.parse_section(buf, 'rooms', map_id)
            MapDataParserIjai.parse_rooms(buf, map_data.rooms)

        if feature_flags & 0x00002000 != 0:
            MapDataParserIjai.parse_section(buf, 'unknown2', map_id)
            MapDataParserIjai.parse_unknown_section(buf)

        if feature_flags & 0x00004000 != 0:
            MapDataParserIjai.parse_section(buf, 'room_outlines', map_id)
            MapDataParserIjai.parse_room_outlines(buf)


    def unpack_map(*args, **kwargs):  # todo: move map_decrypt here
        pass