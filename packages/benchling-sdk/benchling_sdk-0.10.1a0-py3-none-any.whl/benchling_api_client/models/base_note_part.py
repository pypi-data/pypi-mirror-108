from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseNotePart")


@attr.s(auto_attribs=True)
class BaseNotePart:
    """  """

    indentation: Union[Unset, int] = 0
    type: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        indentation = self.indentation
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if indentation is not UNSET:
            field_dict["indentation"] = indentation
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        indentation = d.pop("indentation", UNSET)

        type = d.pop("type", UNSET)

        base_note_part = cls(
            indentation=indentation,
            type=type,
        )

        return base_note_part
