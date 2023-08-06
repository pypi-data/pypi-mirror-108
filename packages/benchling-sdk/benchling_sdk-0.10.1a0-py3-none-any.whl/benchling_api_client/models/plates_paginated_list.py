from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.plate import Plate
from ..types import UNSET, Unset

T = TypeVar("T", bound="PlatesPaginatedList")


@attr.s(auto_attribs=True)
class PlatesPaginatedList:
    """  """

    next_token: Union[Unset, str] = UNSET
    plates: Union[Unset, List[Plate]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        plates: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.plates, Unset):
            plates = []
            for plates_item_data in self.plates:
                plates_item = plates_item_data.to_dict()

                plates.append(plates_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token
        if plates is not UNSET:
            field_dict["plates"] = plates

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken", UNSET)

        plates = []
        _plates = d.pop("plates", UNSET)
        for plates_item_data in _plates or []:
            plates_item = Plate.from_dict(plates_item_data)

            plates.append(plates_item)

        plates_paginated_list = cls(
            next_token=next_token,
            plates=plates,
        )

        return plates_paginated_list
