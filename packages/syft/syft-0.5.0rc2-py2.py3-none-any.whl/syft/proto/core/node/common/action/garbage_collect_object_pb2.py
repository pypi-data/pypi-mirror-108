# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/core/node/common/action/garbage_collect_object.proto
"""Generated protocol buffer code."""
# third party
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


# syft absolute
from syft.proto.core.common import (
    common_object_pb2 as proto_dot_core_dot_common_dot_common__object__pb2,
)
from syft.proto.core.io import address_pb2 as proto_dot_core_dot_io_dot_address__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="proto/core/node/common/action/garbage_collect_object.proto",
    package="syft.core.node.common.action",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n:proto/core/node/common/action/garbage_collect_object.proto\x12\x1csyft.core.node.common.action\x1a%proto/core/common/common_object.proto\x1a\x1bproto/core/io/address.proto"s\n\x1aGarbageCollectObjectAction\x12-\n\x0eid_at_location\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Addressb\x06proto3',
    dependencies=[
        proto_dot_core_dot_common_dot_common__object__pb2.DESCRIPTOR,
        proto_dot_core_dot_io_dot_address__pb2.DESCRIPTOR,
    ],
)


_GARBAGECOLLECTOBJECTACTION = _descriptor.Descriptor(
    name="GarbageCollectObjectAction",
    full_name="syft.core.node.common.action.GarbageCollectObjectAction",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="id_at_location",
            full_name="syft.core.node.common.action.GarbageCollectObjectAction.id_at_location",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="address",
            full_name="syft.core.node.common.action.GarbageCollectObjectAction.address",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=160,
    serialized_end=275,
)

_GARBAGECOLLECTOBJECTACTION.fields_by_name[
    "id_at_location"
].message_type = proto_dot_core_dot_common_dot_common__object__pb2._UID
_GARBAGECOLLECTOBJECTACTION.fields_by_name[
    "address"
].message_type = proto_dot_core_dot_io_dot_address__pb2._ADDRESS
DESCRIPTOR.message_types_by_name[
    "GarbageCollectObjectAction"
] = _GARBAGECOLLECTOBJECTACTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GarbageCollectObjectAction = _reflection.GeneratedProtocolMessageType(
    "GarbageCollectObjectAction",
    (_message.Message,),
    {
        "DESCRIPTOR": _GARBAGECOLLECTOBJECTACTION,
        "__module__": "proto.core.node.common.action.garbage_collect_object_pb2"
        # @@protoc_insertion_point(class_scope:syft.core.node.common.action.GarbageCollectObjectAction)
    },
)
_sym_db.RegisterMessage(GarbageCollectObjectAction)


# @@protoc_insertion_point(module_scope)
