from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DropdownOptionsUnarchive")


@attr.s(auto_attribs=True)
class DropdownOptionsUnarchive:
    """  """

    dropdown_option_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        dropdown_option_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.dropdown_option_ids, Unset):
            dropdown_option_ids = self.dropdown_option_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if dropdown_option_ids is not UNSET:
            field_dict["dropdownOptionIds"] = dropdown_option_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dropdown_option_ids = cast(List[str], d.pop("dropdownOptionIds", UNSET))

        dropdown_options_unarchive = cls(
            dropdown_option_ids=dropdown_option_ids,
        )

        return dropdown_options_unarchive
