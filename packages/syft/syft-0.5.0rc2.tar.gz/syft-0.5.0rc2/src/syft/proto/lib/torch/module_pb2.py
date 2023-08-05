# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/lib/torch/module.proto
"""Generated protocol buffer code."""
# third party
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


# syft absolute
from syft.proto.core.plan import plan_pb2 as proto_dot_core_dot_plan_dot_plan__pb2
from syft.proto.lib.python.collections import (
    ordered_dict_pb2 as proto_dot_lib_dot_python_dot_collections_dot_ordered__dict__pb2,
)

DESCRIPTOR = _descriptor.FileDescriptor(
    name="proto/lib/torch/module.proto",
    package="syft.lib.torch",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\x1cproto/lib/torch/module.proto\x12\x0esyft.lib.torch\x1a/proto/lib/python/collections/ordered_dict.proto\x1a\x1aproto/core/plan/plan.proto"\xf5\x02\n\x06Module\x12\x13\n\x0bmodule_type\x18\x01 \x01(\t\x12\x13\n\x0bmodule_name\x18\x02 \x01(\t\x12\x13\n\x0bmodule_repr\x18\x03 \x01(\t\x12(\n\x08\x63hildren\x18\x04 \x03(\x0b\x32\x16.syft.lib.torch.Module\x12<\n\nstate_dict\x18\x05 \x01(\x0b\x32(.syft.lib.python.collections.OrderedDict\x12<\n\nparameters\x18\x06 \x01(\x0b\x32(.syft.lib.python.collections.OrderedDict\x12*\n\x07\x66orward\x18\x07 \x01(\x0b\x32\x14.syft.core.plan.PlanH\x00\x88\x01\x01\x12@\n\t_uid2attr\x18\x08 \x01(\x0b\x32(.syft.lib.python.collections.OrderedDictH\x01\x88\x01\x01\x42\n\n\x08_forwardB\x0c\n\nX_uid2attrb\x06proto3',
    dependencies=[
        proto_dot_lib_dot_python_dot_collections_dot_ordered__dict__pb2.DESCRIPTOR,
        proto_dot_core_dot_plan_dot_plan__pb2.DESCRIPTOR,
    ],
)


_MODULE = _descriptor.Descriptor(
    name="Module",
    full_name="syft.lib.torch.Module",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="module_type",
            full_name="syft.lib.torch.Module.module_type",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
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
            name="module_name",
            full_name="syft.lib.torch.Module.module_name",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
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
            name="module_repr",
            full_name="syft.lib.torch.Module.module_repr",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
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
            name="children",
            full_name="syft.lib.torch.Module.children",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
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
            name="state_dict",
            full_name="syft.lib.torch.Module.state_dict",
            index=4,
            number=5,
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
            name="parameters",
            full_name="syft.lib.torch.Module.parameters",
            index=5,
            number=6,
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
            name="forward",
            full_name="syft.lib.torch.Module.forward",
            index=6,
            number=7,
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
            name="_uid2attr",
            full_name="syft.lib.torch.Module._uid2attr",
            index=7,
            number=8,
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
    oneofs=[
        _descriptor.OneofDescriptor(
            name="_forward",
            full_name="syft.lib.torch.Module._forward",
            index=0,
            containing_type=None,
            create_key=_descriptor._internal_create_key,
            fields=[],
        ),
        _descriptor.OneofDescriptor(
            name="X_uid2attr",
            full_name="syft.lib.torch.Module.X_uid2attr",
            index=1,
            containing_type=None,
            create_key=_descriptor._internal_create_key,
            fields=[],
        ),
    ],
    serialized_start=126,
    serialized_end=499,
)

_MODULE.fields_by_name["children"].message_type = _MODULE
_MODULE.fields_by_name[
    "state_dict"
].message_type = (
    proto_dot_lib_dot_python_dot_collections_dot_ordered__dict__pb2._ORDEREDDICT
)
_MODULE.fields_by_name[
    "parameters"
].message_type = (
    proto_dot_lib_dot_python_dot_collections_dot_ordered__dict__pb2._ORDEREDDICT
)
_MODULE.fields_by_name[
    "forward"
].message_type = proto_dot_core_dot_plan_dot_plan__pb2._PLAN
_MODULE.fields_by_name[
    "_uid2attr"
].message_type = (
    proto_dot_lib_dot_python_dot_collections_dot_ordered__dict__pb2._ORDEREDDICT
)
_MODULE.oneofs_by_name["_forward"].fields.append(_MODULE.fields_by_name["forward"])
_MODULE.fields_by_name["forward"].containing_oneof = _MODULE.oneofs_by_name["_forward"]
_MODULE.oneofs_by_name["X_uid2attr"].fields.append(_MODULE.fields_by_name["_uid2attr"])
_MODULE.fields_by_name["_uid2attr"].containing_oneof = _MODULE.oneofs_by_name[
    "X_uid2attr"
]
DESCRIPTOR.message_types_by_name["Module"] = _MODULE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Module = _reflection.GeneratedProtocolMessageType(
    "Module",
    (_message.Message,),
    {
        "DESCRIPTOR": _MODULE,
        "__module__": "proto.lib.torch.module_pb2"
        # @@protoc_insertion_point(class_scope:syft.lib.torch.Module)
    },
)
_sym_db.RegisterMessage(Module)


# @@protoc_insertion_point(module_scope)
