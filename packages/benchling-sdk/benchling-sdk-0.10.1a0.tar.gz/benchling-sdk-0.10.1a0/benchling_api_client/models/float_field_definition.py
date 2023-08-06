from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.archive_record import ArchiveRecord
from ..models.float_field_definition_type import FloatFieldDefinitionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="FloatFieldDefinition")


@attr.s(auto_attribs=True)
class FloatFieldDefinition:
    """  """

    id: str
    is_required: bool
    name: str
    decimal_precision: Union[Unset, None, float] = UNSET
    legal_text_dropdown_id: Union[Unset, None, str] = UNSET
    numeric_max: Union[Unset, None, float] = UNSET
    numeric_min: Union[Unset, None, float] = UNSET
    type: Union[Unset, FloatFieldDefinitionType] = UNSET
    archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    is_multi: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        is_required = self.is_required
        name = self.name
        decimal_precision = self.decimal_precision
        legal_text_dropdown_id = self.legal_text_dropdown_id
        numeric_max = self.numeric_max
        numeric_min = self.numeric_min
        type: Union[Unset, int] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        is_multi = self.is_multi

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "isRequired": is_required,
                "name": name,
            }
        )
        if decimal_precision is not UNSET:
            field_dict["decimalPrecision"] = decimal_precision
        if legal_text_dropdown_id is not UNSET:
            field_dict["legalTextDropdownId"] = legal_text_dropdown_id
        if numeric_max is not UNSET:
            field_dict["numericMax"] = numeric_max
        if numeric_min is not UNSET:
            field_dict["numericMin"] = numeric_min
        if type is not UNSET:
            field_dict["type"] = type
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if is_multi is not UNSET:
            field_dict["isMulti"] = is_multi

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        is_required = d.pop("isRequired")

        name = d.pop("name")

        decimal_precision = d.pop("decimalPrecision", UNSET)

        legal_text_dropdown_id = d.pop("legalTextDropdownId", UNSET)

        numeric_max = d.pop("numericMax", UNSET)

        numeric_min = d.pop("numericMin", UNSET)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = FloatFieldDefinitionType(_type)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = ArchiveRecord.from_dict(_archive_record)

        is_multi = d.pop("isMulti", UNSET)

        float_field_definition = cls(
            id=id,
            is_required=is_required,
            name=name,
            decimal_precision=decimal_precision,
            legal_text_dropdown_id=legal_text_dropdown_id,
            numeric_max=numeric_max,
            numeric_min=numeric_min,
            type=type,
            archive_record=archive_record,
            is_multi=is_multi,
        )

        return float_field_definition
