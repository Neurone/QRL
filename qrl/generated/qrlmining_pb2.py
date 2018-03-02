# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qrlmining.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import qrl.generated.qrl_pb2 as qrl__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='qrlmining.proto',
  package='qrl',
  syntax='proto3',
  serialized_pb=_b('\n\x0fqrlmining.proto\x12\x03qrl\x1a\tqrl.proto\"-\n\x1bGetBlockMiningCompatibleReq\x12\x0e\n\x06height\x18\x01 \x01(\x04\"\x17\n\x15GetLastBlockHeaderReq\"p\n\x1cGetBlockMiningCompatibleResp\x12%\n\x0b\x62lockheader\x18\x01 \x01(\x0b\x32\x10.qrl.BlockHeader\x12)\n\rblockmetadata\x18\x02 \x01(\x0b\x32\x12.qrl.BlockMetaData\"m\n\x16GetLastBlockHeaderResp\x12\x12\n\ndifficulty\x18\x01 \x01(\x04\x12\x0e\n\x06height\x18\x02 \x01(\x04\x12\x11\n\ttimestamp\x18\x03 \x01(\x04\x12\x0e\n\x06reward\x18\x04 \x01(\x04\x12\x0c\n\x04hash\x18\x05 \x01(\t\"+\n\x11GetBlockToMineReq\x12\x16\n\x0ewallet_address\x18\x01 \x01(\x0c\"T\n\x12GetBlockToMineResp\x12\x1a\n\x12\x62locktemplate_blob\x18\x01 \x01(\t\x12\x12\n\ndifficulty\x18\x02 \x01(\x04\x12\x0e\n\x06height\x18\x03 \x01(\x04\"#\n\x13SubmitMinedBlockReq\x12\x0c\n\x04\x62lob\x18\x01 \x01(\x0c\"\x16\n\x14SubmitMinedBlockResp2\xc7\x02\n\tMiningAPI\x12_\n\x18GetBlockMiningCompatible\x12 .qrl.GetBlockMiningCompatibleReq\x1a!.qrl.GetBlockMiningCompatibleResp\x12M\n\x12GetLastBlockHeader\x12\x1a.qrl.GetLastBlockHeaderReq\x1a\x1b.qrl.GetLastBlockHeaderResp\x12\x41\n\x0eGetBlockToMine\x12\x16.qrl.GetBlockToMineReq\x1a\x17.qrl.GetBlockToMineResp\x12G\n\x10SubmitMinedBlock\x12\x18.qrl.SubmitMinedBlockReq\x1a\x19.qrl.SubmitMinedBlockRespb\x06proto3')
  ,
  dependencies=[qrl__pb2.DESCRIPTOR,])




_GETBLOCKMININGCOMPATIBLEREQ = _descriptor.Descriptor(
  name='GetBlockMiningCompatibleReq',
  full_name='qrl.GetBlockMiningCompatibleReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='height', full_name='qrl.GetBlockMiningCompatibleReq.height', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=35,
  serialized_end=80,
)


_GETLASTBLOCKHEADERREQ = _descriptor.Descriptor(
  name='GetLastBlockHeaderReq',
  full_name='qrl.GetLastBlockHeaderReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=82,
  serialized_end=105,
)


_GETBLOCKMININGCOMPATIBLERESP = _descriptor.Descriptor(
  name='GetBlockMiningCompatibleResp',
  full_name='qrl.GetBlockMiningCompatibleResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blockheader', full_name='qrl.GetBlockMiningCompatibleResp.blockheader', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='blockmetadata', full_name='qrl.GetBlockMiningCompatibleResp.blockmetadata', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=107,
  serialized_end=219,
)


_GETLASTBLOCKHEADERRESP = _descriptor.Descriptor(
  name='GetLastBlockHeaderResp',
  full_name='qrl.GetLastBlockHeaderResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='difficulty', full_name='qrl.GetLastBlockHeaderResp.difficulty', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='height', full_name='qrl.GetLastBlockHeaderResp.height', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='qrl.GetLastBlockHeaderResp.timestamp', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reward', full_name='qrl.GetLastBlockHeaderResp.reward', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hash', full_name='qrl.GetLastBlockHeaderResp.hash', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=221,
  serialized_end=330,
)


_GETBLOCKTOMINEREQ = _descriptor.Descriptor(
  name='GetBlockToMineReq',
  full_name='qrl.GetBlockToMineReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='wallet_address', full_name='qrl.GetBlockToMineReq.wallet_address', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=332,
  serialized_end=375,
)


_GETBLOCKTOMINERESP = _descriptor.Descriptor(
  name='GetBlockToMineResp',
  full_name='qrl.GetBlockToMineResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blocktemplate_blob', full_name='qrl.GetBlockToMineResp.blocktemplate_blob', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='difficulty', full_name='qrl.GetBlockToMineResp.difficulty', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='height', full_name='qrl.GetBlockToMineResp.height', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=377,
  serialized_end=461,
)


_SUBMITMINEDBLOCKREQ = _descriptor.Descriptor(
  name='SubmitMinedBlockReq',
  full_name='qrl.SubmitMinedBlockReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blob', full_name='qrl.SubmitMinedBlockReq.blob', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=463,
  serialized_end=498,
)


_SUBMITMINEDBLOCKRESP = _descriptor.Descriptor(
  name='SubmitMinedBlockResp',
  full_name='qrl.SubmitMinedBlockResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=500,
  serialized_end=522,
)

_GETBLOCKMININGCOMPATIBLERESP.fields_by_name['blockheader'].message_type = qrl__pb2._BLOCKHEADER
_GETBLOCKMININGCOMPATIBLERESP.fields_by_name['blockmetadata'].message_type = qrl__pb2._BLOCKMETADATA
DESCRIPTOR.message_types_by_name['GetBlockMiningCompatibleReq'] = _GETBLOCKMININGCOMPATIBLEREQ
DESCRIPTOR.message_types_by_name['GetLastBlockHeaderReq'] = _GETLASTBLOCKHEADERREQ
DESCRIPTOR.message_types_by_name['GetBlockMiningCompatibleResp'] = _GETBLOCKMININGCOMPATIBLERESP
DESCRIPTOR.message_types_by_name['GetLastBlockHeaderResp'] = _GETLASTBLOCKHEADERRESP
DESCRIPTOR.message_types_by_name['GetBlockToMineReq'] = _GETBLOCKTOMINEREQ
DESCRIPTOR.message_types_by_name['GetBlockToMineResp'] = _GETBLOCKTOMINERESP
DESCRIPTOR.message_types_by_name['SubmitMinedBlockReq'] = _SUBMITMINEDBLOCKREQ
DESCRIPTOR.message_types_by_name['SubmitMinedBlockResp'] = _SUBMITMINEDBLOCKRESP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetBlockMiningCompatibleReq = _reflection.GeneratedProtocolMessageType('GetBlockMiningCompatibleReq', (_message.Message,), dict(
  DESCRIPTOR = _GETBLOCKMININGCOMPATIBLEREQ,
  __module__ = 'qrlmining_pb2'
  # @@protoc_insertion_point(class_scope:qrl.GetBlockMiningCompatibleReq)
  ))
_sym_db.RegisterMessage(GetBlockMiningCompatibleReq)

GetLastBlockHeaderReq = _reflection.GeneratedProtocolMessageType('GetLastBlockHeaderReq', (_message.Message,), dict(
  DESCRIPTOR = _GETLASTBLOCKHEADERREQ,
  __module__ = 'qrlmining_pb2'
  # @@protoc_insertion_point(class_scope:qrl.GetLastBlockHeaderReq)
  ))
_sym_db.RegisterMessage(GetLastBlockHeaderReq)

GetBlockMiningCompatibleResp = _reflection.GeneratedProtocolMessageType('GetBlockMiningCompatibleResp', (_message.Message,), dict(
  DESCRIPTOR = _GETBLOCKMININGCOMPATIBLERESP,
  __module__ = 'qrlmining_pb2'
  # @@protoc_insertion_point(class_scope:qrl.GetBlockMiningCompatibleResp)
  ))
_sym_db.RegisterMessage(GetBlockMiningCompatibleResp)

GetLastBlockHeaderResp = _reflection.GeneratedProtocolMessageType('GetLastBlockHeaderResp', (_message.Message,), dict(
  DESCRIPTOR = _GETLASTBLOCKHEADERRESP,
  __module__ = 'qrlmining_pb2'
  # @@protoc_insertion_point(class_scope:qrl.GetLastBlockHeaderResp)
  ))
_sym_db.RegisterMessage(GetLastBlockHeaderResp)

GetBlockToMineReq = _reflection.GeneratedProtocolMessageType('GetBlockToMineReq', (_message.Message,), dict(
  DESCRIPTOR = _GETBLOCKTOMINEREQ,
  __module__ = 'qrlmining_pb2'
  # @@protoc_insertion_point(class_scope:qrl.GetBlockToMineReq)
  ))
_sym_db.RegisterMessage(GetBlockToMineReq)

GetBlockToMineResp = _reflection.GeneratedProtocolMessageType('GetBlockToMineResp', (_message.Message,), dict(
  DESCRIPTOR = _GETBLOCKTOMINERESP,
  __module__ = 'qrlmining_pb2'
  # @@protoc_insertion_point(class_scope:qrl.GetBlockToMineResp)
  ))
_sym_db.RegisterMessage(GetBlockToMineResp)

SubmitMinedBlockReq = _reflection.GeneratedProtocolMessageType('SubmitMinedBlockReq', (_message.Message,), dict(
  DESCRIPTOR = _SUBMITMINEDBLOCKREQ,
  __module__ = 'qrlmining_pb2'
  # @@protoc_insertion_point(class_scope:qrl.SubmitMinedBlockReq)
  ))
_sym_db.RegisterMessage(SubmitMinedBlockReq)

SubmitMinedBlockResp = _reflection.GeneratedProtocolMessageType('SubmitMinedBlockResp', (_message.Message,), dict(
  DESCRIPTOR = _SUBMITMINEDBLOCKRESP,
  __module__ = 'qrlmining_pb2'
  # @@protoc_insertion_point(class_scope:qrl.SubmitMinedBlockResp)
  ))
_sym_db.RegisterMessage(SubmitMinedBlockResp)



_MININGAPI = _descriptor.ServiceDescriptor(
  name='MiningAPI',
  full_name='qrl.MiningAPI',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=525,
  serialized_end=852,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetBlockMiningCompatible',
    full_name='qrl.MiningAPI.GetBlockMiningCompatible',
    index=0,
    containing_service=None,
    input_type=_GETBLOCKMININGCOMPATIBLEREQ,
    output_type=_GETBLOCKMININGCOMPATIBLERESP,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetLastBlockHeader',
    full_name='qrl.MiningAPI.GetLastBlockHeader',
    index=1,
    containing_service=None,
    input_type=_GETLASTBLOCKHEADERREQ,
    output_type=_GETLASTBLOCKHEADERRESP,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetBlockToMine',
    full_name='qrl.MiningAPI.GetBlockToMine',
    index=2,
    containing_service=None,
    input_type=_GETBLOCKTOMINEREQ,
    output_type=_GETBLOCKTOMINERESP,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SubmitMinedBlock',
    full_name='qrl.MiningAPI.SubmitMinedBlock',
    index=3,
    containing_service=None,
    input_type=_SUBMITMINEDBLOCKREQ,
    output_type=_SUBMITMINEDBLOCKRESP,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MININGAPI)

DESCRIPTOR.services_by_name['MiningAPI'] = _MININGAPI

# @@protoc_insertion_point(module_scope)
