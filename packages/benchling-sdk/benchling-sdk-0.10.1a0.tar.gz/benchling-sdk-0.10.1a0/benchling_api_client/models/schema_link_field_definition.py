from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.archive_record import ArchiveRecord
from ..models.schema_link_field_definition_type import SchemaLinkFieldDefinitionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SchemaLinkFieldDefinition")


@attr.s(auto_attribs=True)
class SchemaLinkFieldDefinition:
    """  """

    id: str
    is_required: bool
    name: str
    schema_id: Union[Unset, None, str] = UNSET
    type: Union[Unset, SchemaLinkFieldDefinitionType] = UNSET
    archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    is_multi: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        is_required = self.is_required
        name = self.name
        schema_id = self.schema_id
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
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id
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

        schema_id = d.pop("schemaId", UNSET)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = SchemaLinkFieldDefinitionType(_type)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = ArchiveRecord.from_dict(_archive_record)

        is_multi = d.pop("isMulti", UNSET)

        schema_link_field_definition = cls(
            id=id,
            is_required=is_required,
            name=name,
            schema_id=schema_id,
            type=type,
            archive_record=archive_record,
            is_multi=is_multi,
        )

        return schema_link_field_definition
