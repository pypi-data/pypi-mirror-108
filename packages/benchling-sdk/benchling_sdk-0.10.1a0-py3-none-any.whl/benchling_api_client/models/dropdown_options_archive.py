from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..models.dropdown_options_archive_reason import DropdownOptionsArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="DropdownOptionsArchive")


@attr.s(auto_attribs=True)
class DropdownOptionsArchive:
    """  """

    dropdown_option_ids: Union[Unset, List[str]] = UNSET
    reason: Union[Unset, DropdownOptionsArchiveReason] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        dropdown_option_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.dropdown_option_ids, Unset):
            dropdown_option_ids = self.dropdown_option_ids

        reason: Union[Unset, int] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if dropdown_option_ids is not UNSET:
            field_dict["dropdownOptionIds"] = dropdown_option_ids
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dropdown_option_ids = cast(List[str], d.pop("dropdownOptionIds", UNSET))

        reason = None
        _reason = d.pop("reason", UNSET)
        if _reason is not None and _reason is not UNSET:
            reason = DropdownOptionsArchiveReason(_reason)

        dropdown_options_archive = cls(
            dropdown_option_ids=dropdown_option_ids,
            reason=reason,
        )

        return dropdown_options_archive
