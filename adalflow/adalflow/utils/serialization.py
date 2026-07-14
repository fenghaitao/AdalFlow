import json
import logging

from typing import Mapping, Any, Dict, Union
import enum
import inspect

from adalflow.utils.registry import EntityMapping


log = logging.getLogger(__name__)


class ObjectTypes(enum.Enum):
    CLASS = 1
    INSTANCE = 2
    TYPE = 3


def check_object(obj) -> ObjectTypes:
    if inspect.isclass(obj):
        return ObjectTypes.CLASS

    elif isinstance(obj, type):
        return ObjectTypes.TYPE
    else:
        return ObjectTypes.INSTANCE


def default(o: Any) -> Union[Dict[str, Any], str]:
    r"""Customized JSON serializer.

    (1) Support internal dataclasses and components instance serialization by calling to_dict() method.
    (2) Support internal dataclasses class serialization by calling to_dict_class() method.

    (3) Any external instance if it has to_dict() method, it will be serialized.
    (4) All other objects will be serialized as {"type": type(o).__name__, "data": str(o)}
    """
    seralized_obj = {}

    # 1. Handle the case like Component, DataClass where we have to_dict and to_dict_class
    obj_type = check_object(o)
    if obj_type == ObjectTypes.CLASS:
        log.debug(f"Object {o} is a class with name {o.__name__}")
        if hasattr(o, "to_dict_class") and callable(getattr(o, "to_dict_class")):
            try:
                seralized_obj = o.to_dict_class()
                return seralized_obj
            except Exception as e:
                log.error(f"Error serializing object {o}: {e}")
                pass
    elif obj_type == ObjectTypes.INSTANCE:
        log.debug(f"Object {o} is an instance of {o.__class__.__name__}")
        if hasattr(o, "to_dict") and callable(getattr(o, "to_dict")):
            try:
                seralized_obj = o.to_dict()
                return seralized_obj
            except Exception as e:
                log.error(f"Error serializing object {o}: {e}")
                pass

        # handle set
        if isinstance(o, set):
            return {"type": type(o).__name__, "data": list(o)}
        else:
            return {"type": type(o).__name__, "data": str(o)}
            # raise NotImplementedError(
            #     f"Object of type {o.__class__.__name__} is not JSON serializable: {o}"
            # )
    elif obj_type == ObjectTypes.TYPE:
        log.debug(f"Object {o} is a type of {o.__name__}")
        try:
            return {"type": type(o).__name__, "data": str(o)}
        except Exception as e:
            log.error(
                f"Object of type {o.__class__.__name__} is not JSON serializable: {str(e)}"
            )
            pass

    log.debug("Fallback to serializing attributes who come from external libraries")

    # (2) Fallback to serializing attributes who come from external libraries
    try:
        return {"type": type(o).__name__, "data": str(o)}
    except Exception as e:
        raise TypeError(
            f"Object of type {o.__class__.__name__} is not JSON serializable: {str(e)}"
        )


def serialize(obj: Mapping[str, Any]) -> str:
    """Serialize the object to a json string.

    Args:
        obj (Mapping[str, Any]): The object to be serialized.

    Returns:
        str: The serialized object in json format.
    """

    return json.dumps(obj, indent=4, default=default)


def deserialize(data: str) -> Any:
    """Deserialize the JSON string back to an object."""
    return json.loads(data, object_hook=_deserialize_object_hook)


def _deserialize_object_hook(d: Dict[str, Any]) -> Any:
    """Hook to deserialize objects based on their type."""
    if "type" in d and "data" in d:
        class_name = d["type"]
        if class_name == "set":
            return set(d["data"])

        # deseralize customized types
        # TODO: all customized data types need to be saved
        class_type = EntityMapping.get(class_name)
        try:
            if class_type:
                return class_type.from_dict(d)
        except Exception as e:
            # default to the original object
            log.error(f"Error deserializing object {d}: {e}")
            pass
    return d


def to_dict(obj: Any) -> Any:
    """Convert the object to a dictionary by direct recursive conversion.

    This is a performance optimization over `json.loads(serialize(obj))`.

    Args:
        obj (Any): The object to be converted.

    Returns:
        Any: The dictionary representation of the object.
    """
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    if isinstance(obj, dict):
        return {str(k): to_dict(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_dict(v) for v in obj]
    if isinstance(obj, set):
        return {"type": "set", "data": [to_dict(v) for v in obj]}
    if isinstance(obj, enum.Enum):
        return {"type": type(obj).__name__, "data": str(obj)}
    if hasattr(obj, "to_dict") and callable(obj.to_dict):
        return to_dict(obj.to_dict())
    if hasattr(obj, "to_dict_class") and callable(obj.to_dict_class):
        return to_dict(obj.to_dict_class())

    # Fallback to default() for other types (handles dataclasses and others)
    try:
        res = default(obj)
        # If default returns a primitive or a dict/list that we can handle,
        # we still need to recursively process it to handle nested custom types.
        if isinstance(res, dict) and "type" in res:
            return res
        return to_dict(res)
    except Exception:
        return str(obj)
