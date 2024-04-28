# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: RobotMap.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eRobotMap.proto\"\xa8\x18\n\x08RobotMap\x12\x0f\n\x07mapType\x18\x01 \x01(\r\x12(\n\nmapExtInfo\x18\x02 \x01(\x0b\x32\x14.RobotMap.MapExtInfo\x12&\n\x07mapHead\x18\x03 \x01(\x0b\x32\x15.RobotMap.MapHeadInfo\x12&\n\x07mapData\x18\x04 \x01(\x0b\x32\x15.RobotMap.MapDataInfo\x12%\n\x07mapInfo\x18\x05 \x03(\x0b\x32\x14.RobotMap.AllMapInfo\x12\x34\n\x0bhistoryPose\x18\x06 \x01(\x0b\x32\x1f.RobotMap.DeviceHistoryPoseInfo\x12\x33\n\rchargeStation\x18\x07 \x01(\x0b\x32\x1c.RobotMap.DevicePoseDataInfo\x12\x34\n\x0b\x63urrentPose\x18\x08 \x01(\x0b\x32\x1f.RobotMap.DeviceCurrentPoseInfo\x12\x32\n\x0cvirtualWalls\x18\t \x03(\x0b\x32\x1c.RobotMap.DeviceAreaDataInfo\x12/\n\tareasInfo\x18\n \x03(\x0b\x32\x1c.RobotMap.DeviceAreaDataInfo\x12\x41\n\x10navigationPoints\x18\x0b \x03(\x0b\x32\'.RobotMap.DeviceNavigationPointDataInfo\x12,\n\x0croomDataInfo\x18\x0c \x03(\x0b\x32\x16.RobotMap.RoomDataInfo\x12.\n\nroomMatrix\x18\r \x01(\x0b\x32\x1a.RobotMap.DeviceRoomMatrix\x12\x34\n\troomChain\x18\x0e \x03(\x0b\x32!.RobotMap.DeviceRoomChainDataInfo\x12)\n\x07objects\x18\x0f \x03(\x0b\x32\x18.RobotMap.ObjectDataInfo\x12\x32\n\rfurnitureInfo\x18\x10 \x03(\x0b\x32\x1b.RobotMap.FurnitureDataInfo\x12\'\n\nhouseInfos\x18\x11 \x03(\x0b\x32\x13.RobotMap.HouseInfo\x12\x31\n\x0b\x62\x61\x63kupAreas\x18\x12 \x03(\x0b\x32\x1c.RobotMap.DeviceAreaDataInfo\x1ar\n\tHouseInfo\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x63urMapCount\x18\x03 \x01(\r\x12\x12\n\nmaxMapSize\x18\x04 \x01(\r\x12\"\n\x04maps\x18\x05 \x03(\x0b\x32\x14.RobotMap.AllMapInfo\x1a\xa1\x01\n\x11\x46urnitureDataInfo\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0e\n\x06typeId\x18\x02 \x01(\r\x12)\n\x06points\x18\x03 \x03(\x0b\x32\x19.RobotMap.DevicePointInfo\x12\x0b\n\x03url\x18\x04 \x01(\t\x12\x0e\n\x06status\x18\x05 \x01(\r\x12(\n\x05react\x18\x06 \x03(\x0b\x32\x19.RobotMap.DevicePointInfo\x1a\x91\x01\n\x0eObjectDataInfo\x12\x10\n\x08objectId\x18\x01 \x01(\r\x12\x14\n\x0cobjectTypeId\x18\x02 \x01(\r\x12\x12\n\nobjectName\x18\x03 \x01(\t\x12\x0f\n\x07\x63onfirm\x18\x04 \x01(\r\x12\t\n\x01x\x18\x05 \x01(\x02\x12\t\n\x01y\x18\x06 \x01(\x02\x12\x0b\n\x03url\x18\x07 \x01(\t\x12\x0f\n\x07notShow\x18\x08 \x01(\r\x1a?\n\x18\x44\x65viceChainPointDataInfo\x12\t\n\x01x\x18\x01 \x01(\r\x12\t\n\x01y\x18\x02 \x01(\r\x12\r\n\x05value\x18\x03 \x01(\r\x1a]\n\x17\x44\x65viceRoomChainDataInfo\x12\x0e\n\x06roomId\x18\x01 \x01(\r\x12\x32\n\x06points\x18\x02 \x03(\x0b\x32\".RobotMap.DeviceChainPointDataInfo\x1a\"\n\x10\x44\x65viceRoomMatrix\x12\x0e\n\x06matrix\x18\x01 \x01(\x0c\x1ag\n\x17\x43leanPerferenceDataInfo\x12\x11\n\tcleanMode\x18\x01 \x01(\r\x12\x12\n\nwaterLevel\x18\x02 \x01(\r\x12\x11\n\twindPower\x18\x03 \x01(\r\x12\x12\n\ntwiceClean\x18\x04 \x01(\r\x1a\x91\x02\n\x0cRoomDataInfo\x12\x0e\n\x06roomId\x18\x01 \x01(\r\x12\x10\n\x08roomName\x18\x02 \x01(\t\x12\x12\n\nroomTypeId\x18\x03 \x01(\r\x12\x12\n\nmeterialId\x18\x04 \x01(\r\x12\x12\n\ncleanState\x18\x05 \x01(\r\x12\x11\n\troomClean\x18\x06 \x01(\r\x12\x16\n\x0eroomCleanIndex\x18\x07 \x01(\r\x12/\n\x0croomNamePost\x18\x08 \x01(\x0b\x32\x19.RobotMap.DevicePointInfo\x12\x36\n\x0b\x63leanPerfer\x18\t \x01(\x0b\x32!.RobotMap.CleanPerferenceDataInfo\x12\x0f\n\x07\x63olorId\x18\n \x01(\r\x1av\n\x1d\x44\x65viceNavigationPointDataInfo\x12\x0f\n\x07pointId\x18\x01 \x01(\r\x12\x0e\n\x06status\x18\x02 \x01(\r\x12\x11\n\tpointType\x18\x03 \x01(\r\x12\t\n\x01x\x18\x04 \x01(\x02\x12\t\n\x01y\x18\x05 \x01(\x02\x12\x0b\n\x03phi\x18\x06 \x01(\x02\x1a\'\n\x0f\x44\x65vicePointInfo\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x1ap\n\x12\x44\x65viceAreaDataInfo\x12\x0e\n\x06status\x18\x01 \x01(\r\x12\x0c\n\x04type\x18\x02 \x01(\r\x12\x11\n\tareaIndex\x18\x03 \x01(\r\x12)\n\x06points\x18\x04 \x03(\x0b\x32\x19.RobotMap.DevicePointInfo\x1aZ\n\x15\x44\x65viceCurrentPoseInfo\x12\x0e\n\x06poseId\x18\x01 \x01(\r\x12\x0e\n\x06update\x18\x02 \x01(\r\x12\t\n\x01x\x18\x03 \x01(\x02\x12\t\n\x01y\x18\x04 \x01(\x02\x12\x0b\n\x03phi\x18\x05 \x01(\x02\x1aG\n\x12\x44\x65vicePoseDataInfo\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\x0b\n\x03phi\x18\x03 \x01(\x02\x12\x0e\n\x06roomId\x18\x04 \x01(\r\x1a@\n\x18\x44\x65viceCoverPointDataInfo\x12\x0e\n\x06update\x18\x01 \x01(\r\x12\t\n\x01x\x18\x02 \x01(\x02\x12\t\n\x01y\x18\x03 \x01(\x02\x1am\n\x15\x44\x65viceHistoryPoseInfo\x12\x0e\n\x06poseId\x18\x01 \x01(\r\x12\x32\n\x06points\x18\x02 \x03(\x0b\x32\".RobotMap.DeviceCoverPointDataInfo\x12\x10\n\x08pathType\x18\x03 \x01(\r\x1a\x30\n\nAllMapInfo\x12\x11\n\tmapHeadId\x18\x01 \x01(\r\x12\x0f\n\x07mapName\x18\x02 \x01(\t\x1a\x1e\n\x0bMapDataInfo\x12\x0f\n\x07mapData\x18\x01 \x01(\x0c\x1a\x8a\x01\n\x0bMapHeadInfo\x12\x11\n\tmapHeadId\x18\x01 \x01(\r\x12\r\n\x05sizeX\x18\x02 \x01(\r\x12\r\n\x05sizeY\x18\x03 \x01(\r\x12\x0c\n\x04minX\x18\x04 \x01(\x02\x12\x0c\n\x04minY\x18\x05 \x01(\x02\x12\x0c\n\x04maxX\x18\x06 \x01(\x02\x12\x0c\n\x04maxY\x18\x07 \x01(\x02\x12\x12\n\nresolution\x18\x08 \x01(\x02\x1a-\n\x10\x43\x61rpetOffsetInfo\x12\x0b\n\x03phi\x18\x01 \x01(\x02\x12\x0c\n\x04\x64ist\x18\x02 \x01(\x02\x1a]\n\x0fMapBoundaryInfo\x12\x0e\n\x06mapMd5\x18\x01 \x01(\t\x12\r\n\x05vMinX\x18\x02 \x01(\r\x12\r\n\x05vMaxX\x18\x03 \x01(\r\x12\r\n\x05vMinY\x18\x04 \x01(\r\x12\r\n\x05vMaxY\x18\x05 \x01(\r\x1a\x8e\x02\n\nMapExtInfo\x12\x15\n\rtaskBeginDate\x18\x01 \x01(\r\x12\x15\n\rmapUploadDate\x18\x02 \x01(\r\x12\x10\n\x08mapValid\x18\x03 \x01(\r\x12\x0e\n\x06radian\x18\x04 \x01(\r\x12\r\n\x05\x66orce\x18\x05 \x01(\r\x12\x11\n\tcleanPath\x18\x06 \x01(\r\x12.\n\x0b\x62oudaryInfo\x18\x07 \x01(\x0b\x32\x19.RobotMap.MapBoundaryInfo\x12\x12\n\nmapVersion\x18\x08 \x01(\r\x12\x14\n\x0cmapValueType\x18\t \x01(\r\x12\x34\n\x10\x63\x61rpetOffsetInfo\x18\n \x01(\x0b\x32\x1a.RobotMap.CarpetOffsetInfob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'RobotMap_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ROBOTMAP']._serialized_start=19
  _globals['_ROBOTMAP']._serialized_end=3131
  _globals['_ROBOTMAP_HOUSEINFO']._serialized_start=873
  _globals['_ROBOTMAP_HOUSEINFO']._serialized_end=987
  _globals['_ROBOTMAP_FURNITUREDATAINFO']._serialized_start=990
  _globals['_ROBOTMAP_FURNITUREDATAINFO']._serialized_end=1151
  _globals['_ROBOTMAP_OBJECTDATAINFO']._serialized_start=1154
  _globals['_ROBOTMAP_OBJECTDATAINFO']._serialized_end=1299
  _globals['_ROBOTMAP_DEVICECHAINPOINTDATAINFO']._serialized_start=1301
  _globals['_ROBOTMAP_DEVICECHAINPOINTDATAINFO']._serialized_end=1364
  _globals['_ROBOTMAP_DEVICEROOMCHAINDATAINFO']._serialized_start=1366
  _globals['_ROBOTMAP_DEVICEROOMCHAINDATAINFO']._serialized_end=1459
  _globals['_ROBOTMAP_DEVICEROOMMATRIX']._serialized_start=1461
  _globals['_ROBOTMAP_DEVICEROOMMATRIX']._serialized_end=1495
  _globals['_ROBOTMAP_CLEANPERFERENCEDATAINFO']._serialized_start=1497
  _globals['_ROBOTMAP_CLEANPERFERENCEDATAINFO']._serialized_end=1600
  _globals['_ROBOTMAP_ROOMDATAINFO']._serialized_start=1603
  _globals['_ROBOTMAP_ROOMDATAINFO']._serialized_end=1876
  _globals['_ROBOTMAP_DEVICENAVIGATIONPOINTDATAINFO']._serialized_start=1878
  _globals['_ROBOTMAP_DEVICENAVIGATIONPOINTDATAINFO']._serialized_end=1996
  _globals['_ROBOTMAP_DEVICEPOINTINFO']._serialized_start=1998
  _globals['_ROBOTMAP_DEVICEPOINTINFO']._serialized_end=2037
  _globals['_ROBOTMAP_DEVICEAREADATAINFO']._serialized_start=2039
  _globals['_ROBOTMAP_DEVICEAREADATAINFO']._serialized_end=2151
  _globals['_ROBOTMAP_DEVICECURRENTPOSEINFO']._serialized_start=2153
  _globals['_ROBOTMAP_DEVICECURRENTPOSEINFO']._serialized_end=2243
  _globals['_ROBOTMAP_DEVICEPOSEDATAINFO']._serialized_start=2245
  _globals['_ROBOTMAP_DEVICEPOSEDATAINFO']._serialized_end=2316
  _globals['_ROBOTMAP_DEVICECOVERPOINTDATAINFO']._serialized_start=2318
  _globals['_ROBOTMAP_DEVICECOVERPOINTDATAINFO']._serialized_end=2382
  _globals['_ROBOTMAP_DEVICEHISTORYPOSEINFO']._serialized_start=2384
  _globals['_ROBOTMAP_DEVICEHISTORYPOSEINFO']._serialized_end=2493
  _globals['_ROBOTMAP_ALLMAPINFO']._serialized_start=2495
  _globals['_ROBOTMAP_ALLMAPINFO']._serialized_end=2543
  _globals['_ROBOTMAP_MAPDATAINFO']._serialized_start=2545
  _globals['_ROBOTMAP_MAPDATAINFO']._serialized_end=2575
  _globals['_ROBOTMAP_MAPHEADINFO']._serialized_start=2578
  _globals['_ROBOTMAP_MAPHEADINFO']._serialized_end=2716
  _globals['_ROBOTMAP_CARPETOFFSETINFO']._serialized_start=2718
  _globals['_ROBOTMAP_CARPETOFFSETINFO']._serialized_end=2763
  _globals['_ROBOTMAP_MAPBOUNDARYINFO']._serialized_start=2765
  _globals['_ROBOTMAP_MAPBOUNDARYINFO']._serialized_end=2858
  _globals['_ROBOTMAP_MAPEXTINFO']._serialized_start=2861
  _globals['_ROBOTMAP_MAPEXTINFO']._serialized_end=3131
# @@protoc_insertion_point(module_scope)
