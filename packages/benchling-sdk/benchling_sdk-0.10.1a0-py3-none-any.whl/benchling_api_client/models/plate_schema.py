from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.archive_record import ArchiveRecord
from ..models.box_schema_container_schema import BoxSchemaContainerSchema
from ..models.dropdown_field_definition import DropdownFieldDefinition
from ..models.float_field_definition import FloatFieldDefinition
from ..models.integer_field_definition import IntegerFieldDefinition
from ..models.schema_link_field_definition import SchemaLinkFieldDefinition
from ..models.simple_field_definition import SimpleFieldDefinition
from ..types import UNSET, Unset

T = TypeVar("T", bound="PlateSchema")


@attr.s(auto_attribs=True)
class PlateSchema:
    """  """

    type: str
    field_definitions: List[
        Union[
            SimpleFieldDefinition,
            IntegerFieldDefinition,
            FloatFieldDefinition,
            DropdownFieldDefinition,
            SchemaLinkFieldDefinition,
        ]
    ]
    id: str
    name: str
    plate_type: Union[Unset, str] = UNSET
    container_schema: Union[Unset, None, BoxSchemaContainerSchema] = UNSET
    height: Union[Unset, float] = UNSET
    width: Union[Unset, float] = UNSET
    prefix: Union[Unset, str] = UNSET
    registry_id: Union[Unset, str] = UNSET
    archive_record: Union[Unset, None, ArchiveRecord] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        field_definitions = []
        for field_definitions_item_data in self.field_definitions:
            if isinstance(field_definitions_item_data, SimpleFieldDefinition):
                field_definitions_item = field_definitions_item_data.to_dict()

            elif isinstance(field_definitions_item_data, IntegerFieldDefinition):
                field_definitions_item = field_definitions_item_data.to_dict()

            elif isinstance(field_definitions_item_data, FloatFieldDefinition):
                field_definitions_item = field_definitions_item_data.to_dict()

            elif isinstance(field_definitions_item_data, DropdownFieldDefinition):
                field_definitions_item = field_definitions_item_data.to_dict()

            else:
                field_definitions_item = field_definitions_item_data.to_dict()

            field_definitions.append(field_definitions_item)

        id = self.id
        name = self.name
        plate_type = self.plate_type
        container_schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.container_schema, Unset):
            container_schema = self.container_schema.to_dict() if self.container_schema else None

        height = self.height
        width = self.width
        prefix = self.prefix
        registry_id = self.registry_id
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type,
                "fieldDefinitions": field_definitions,
                "id": id,
                "name": name,
            }
        )
        if plate_type is not UNSET:
            field_dict["plateType"] = plate_type
        if container_schema is not UNSET:
            field_dict["containerSchema"] = container_schema
        if height is not UNSET:
            field_dict["height"] = height
        if width is not UNSET:
            field_dict["width"] = width
        if prefix is not UNSET:
            field_dict["prefix"] = prefix
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        field_definitions = []
        _field_definitions = d.pop("fieldDefinitions")
        for field_definitions_item_data in _field_definitions:

            def _parse_field_definitions_item(
                data: Union[Dict[str, Any]]
            ) -> Union[
                SimpleFieldDefinition,
                IntegerFieldDefinition,
                FloatFieldDefinition,
                DropdownFieldDefinition,
                SchemaLinkFieldDefinition,
            ]:
                field_definitions_item: Union[
                    SimpleFieldDefinition,
                    IntegerFieldDefinition,
                    FloatFieldDefinition,
                    DropdownFieldDefinition,
                    SchemaLinkFieldDefinition,
                ]
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    field_definitions_item = SimpleFieldDefinition.from_dict(data)

                    return field_definitions_item
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    field_definitions_item = IntegerFieldDefinition.from_dict(data)

                    return field_definitions_item
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    field_definitions_item = FloatFieldDefinition.from_dict(data)

                    return field_definitions_item
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    field_definitions_item = DropdownFieldDefinition.from_dict(data)

                    return field_definitions_item
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                field_definitions_item = SchemaLinkFieldDefinition.from_dict(data)

                return field_definitions_item

            field_definitions_item = _parse_field_definitions_item(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        id = d.pop("id")

        name = d.pop("name")

        plate_type = d.pop("plateType", UNSET)

        container_schema = None
        _container_schema = d.pop("containerSchema", UNSET)
        if _container_schema is not None and not isinstance(_container_schema, Unset):
            container_schema = BoxSchemaContainerSchema.from_dict(_container_schema)

        height = d.pop("height", UNSET)

        width = d.pop("width", UNSET)

        prefix = d.pop("prefix", UNSET)

        registry_id = d.pop("registryId", UNSET)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = ArchiveRecord.from_dict(_archive_record)

        plate_schema = cls(
            type=type,
            field_definitions=field_definitions,
            id=id,
            name=name,
            plate_type=plate_type,
            container_schema=container_schema,
            height=height,
            width=width,
            prefix=prefix,
            registry_id=registry_id,
            archive_record=archive_record,
        )

        return plate_schema
