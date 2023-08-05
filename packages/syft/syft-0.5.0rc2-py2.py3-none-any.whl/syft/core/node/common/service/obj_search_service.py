# DOs and Don's of this class:
# - Do NOT use absolute syft imports (i.e. import syft.core...) Use relative ones.
# - Do NOT put multiple imports on the same line (i.e. from <x> import a, b, c). Use separate lines
# - Do sort imports by length
# - Do group imports by where they come from

# stdlib
from typing import List
from typing import Optional
from typing import Type

# third party
from google.protobuf.reflection import GeneratedProtocolMessageType
from nacl.signing import VerifyKey
from typing_extensions import final

# syft relative
from ..... import serialize
from .....core.common.serde.serializable import bind_protobuf
from .....logger import error
from .....proto.core.node.common.service.object_search_message_pb2 import (
    ObjectSearchMessage as ObjectSearchMessage_PB,
)
from .....proto.core.node.common.service.object_search_message_pb2 import (
    ObjectSearchReplyMessage as ObjectSearchReplyMessage_PB,
)
from .....util import obj2pointer_type
from .....util import traceback_and_raise
from ....common.group import VERIFYALL
from ....common.message import ImmediateSyftMessageWithReply
from ....common.message import ImmediateSyftMessageWithoutReply
from ....common.serde.deserialize import _deserialize
from ....common.uid import UID
from ....io.address import Address
from ....pointer.pointer import Pointer
from ...abstract.node import AbstractNode
from .node_service import ImmediateNodeServiceWithReply


@bind_protobuf
@final
class ObjectSearchMessage(ImmediateSyftMessageWithReply):
    def __init__(
        self, address: Address, reply_to: Address, msg_id: Optional[UID] = None
    ):
        super().__init__(address=address, msg_id=msg_id, reply_to=reply_to)
        """By default this message just returns pointers to all the objects
        the sender is allowed to see. In the future we'll add support so that
        we can query for subsets."""

    def _object2proto(self) -> ObjectSearchMessage_PB:
        """Returns a protobuf serialization of self.

        As a requirement of all objects which inherit from Serializable,
        this method transforms the current object into the corresponding
        Protobuf object so that it can be further serialized.

        :return: returns a protobuf object
        :rtype: ObjectSearchMessage_PB

        .. note::
            This method is purely an internal method. Please use serialize(object) or one of
            the other public serialization methods if you wish to serialize an
            object.
        """
        return ObjectSearchMessage_PB(
            msg_id=serialize(self.id),
            address=serialize(self.address),
            reply_to=serialize(self.reply_to),
        )

    @staticmethod
    def _proto2object(proto: ObjectSearchMessage_PB) -> "ObjectSearchMessage":
        """Creates a ObjectSearchMessage from a protobuf

        As a requirement of all objects which inherit from Serializable,
        this method transforms a protobuf object into an instance of this class.

        :return: returns an instance of ObjectSearchMessage
        :rtype: ObjectSearchMessage

        .. note::
            This method is purely an internal method. Please use syft.deserialize()
            if you wish to deserialize an object.
        """

        return ObjectSearchMessage(
            msg_id=_deserialize(blob=proto.msg_id),
            address=_deserialize(blob=proto.address),
            reply_to=_deserialize(blob=proto.reply_to),
        )

    @staticmethod
    def get_protobuf_schema() -> GeneratedProtocolMessageType:
        """Return the type of protobuf object which stores a class of this type

        As a part of serialization and deserialization, we need the ability to
        lookup the protobuf object type directly from the object type. This
        static method allows us to do this.

        Importantly, this method is also used to create the reverse lookup ability within
        the metaclass of Serializable. In the metaclass, it calls this method and then
        it takes whatever type is returned from this method and adds an attribute to it
        with the type of this class attached to it. See the MetaSerializable class for details.

        :return: the type of protobuf object which corresponds to this class.
        :rtype: GeneratedProtocolMessageType

        """

        return ObjectSearchMessage_PB


@bind_protobuf
@final
class ObjectSearchReplyMessage(ImmediateSyftMessageWithoutReply):
    def __init__(
        self,
        results: List[Pointer],
        address: Address,
        msg_id: Optional[UID] = None,
    ):
        super().__init__(address=address, msg_id=msg_id)
        """By default this message just returns pointers to all the objects
        the sender is allowed to see. In the future we'll add support so that
        we can query for subsets."""
        self.results = results

    def _object2proto(self) -> ObjectSearchReplyMessage_PB:
        """Returns a protobuf serialization of self.

        As a requirement of all objects which inherit from Serializable,
        this method transforms the current object into the corresponding
        Protobuf object so that it can be further serialized.

        :return: returns a protobuf object
        :rtype: ObjectSearchReplyMessage_PB

        .. note::
            This method is purely an internal method. Please use serialize(object) or one of
            the other public serialization methods if you wish to serialize an
            object.
        """
        return ObjectSearchReplyMessage_PB(
            msg_id=serialize(self.id),
            address=serialize(self.address),
            results=list(map(lambda x: serialize(x), self.results)),
        )

    @staticmethod
    def _proto2object(proto: ObjectSearchReplyMessage_PB) -> "ObjectSearchReplyMessage":
        """Creates a ObjectSearchReplyMessage from a protobuf

        As a requirement of all objects which inherit from Serializable,
        this method transforms a protobuf object into an instance of this class.

        :return: returns an instance of ObjectSearchReplyMessage
        :rtype: ObjectSearchReplyMessage

        .. note::
            This method is purely an internal method. Please use syft.deserialize()
            if you wish to deserialize an object.
        """

        return ObjectSearchReplyMessage(
            msg_id=_deserialize(blob=proto.msg_id),
            address=_deserialize(blob=proto.address),
            results=[_deserialize(blob=x) for x in proto.results],
        )

    @staticmethod
    def get_protobuf_schema() -> GeneratedProtocolMessageType:
        """Return the type of protobuf object which stores a class of this type

        As a part of serialization and deserialization, we need the ability to
        lookup the protobuf object type directly from the object type. This
        static method allows us to do this.

        Importantly, this method is also used to create the reverse lookup ability within
        the metaclass of Serializable. In the metaclass, it calls this method and then
        it takes whatever type is returned from this method and adds an attribute to it
        with the type of this class attached to it. See the MetaSerializable class for details.

        :return: the type of protobuf object which corresponds to this class.
        :rtype: GeneratedProtocolMessageType

        """

        return ObjectSearchReplyMessage_PB


class ImmediateObjectSearchService(ImmediateNodeServiceWithReply):
    @staticmethod
    def process(
        node: AbstractNode,
        msg: ObjectSearchMessage,
        verify_key: Optional[VerifyKey] = None,
    ) -> ObjectSearchReplyMessage:
        results: List[Pointer] = list()

        if verify_key is None:
            traceback_and_raise(
                "Can't process an ImmediateObjectSearchService with no "
                "verification key."
            )

        try:
            for obj in node.store.get_objects_of_type(obj_type=object):
                # if this tensor allows anyone to search for it, then one of its keys
                # has a VERIFYALL in it.
                contains_all_in_permissions = any(
                    key is VERIFYALL for key in obj.search_permissions.keys()
                )
                if (
                    verify_key in obj.search_permissions.keys()
                    or verify_key == node.root_verify_key
                    or contains_all_in_permissions
                ):
                    ptr_type = obj2pointer_type(obj=obj.data)
                    ptr = ptr_type(
                        client=node,
                        id_at_location=obj.id,
                        object_type=obj.object_type,
                        tags=obj.tags,
                        description=obj.description,
                    )
                    results.append(ptr)
        except Exception as e:
            error(f"Error searching store. {e}")

        return ObjectSearchReplyMessage(address=msg.reply_to, results=results)

    @staticmethod
    def message_handler_types() -> List[Type[ObjectSearchMessage]]:
        return [ObjectSearchMessage]
