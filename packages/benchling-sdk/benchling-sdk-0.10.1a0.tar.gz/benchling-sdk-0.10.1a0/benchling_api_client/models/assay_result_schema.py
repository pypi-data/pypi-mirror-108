from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.archive_record import ArchiveRecord
from ..models.base_assay_schema_organization import BaseAssaySchemaOrganization
from ..models.dropdown_field_definition import DropdownFieldDefinition
from ..models.float_field_definition import FloatFieldDefinition
from ..models.integer_field_definition import IntegerFieldDefinition
from ..models.schema_link_field_definition import SchemaLinkFieldDefinition
from ..models.simple_field_definition import SimpleFieldDefinition
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayResultSchema")


@attr.s(auto_attribs=True)
class AssayResultSchema:
    """  """

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
    type: str
    derived_from: Union[Unset, None, str] = UNSET
    organization: Union[Unset, BaseAssaySchemaOrganization] = UNSET
    system_name: Union[Unset, str] = UNSET
    archive_record: Union[Unset, None, ArchiveRecord] = UNSET

    def to_dict(self) -> Dict[str, Any]:
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
        type = self.type
        derived_from = self.derived_from
        organization: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.organization, Unset):
            organization = self.organization.to_dict()

        system_name = self.system_name
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fieldDefinitions": field_definitions,
                "id": id,
                "name": name,
                "type": type,
            }
        )
        if derived_from is not UNSET:
            field_dict["derivedFrom"] = derived_from
        if organization is not UNSET:
            field_dict["organization"] = organization
        if system_name is not UNSET:
            field_dict["systemName"] = system_name
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
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

        type = d.pop("type")

        derived_from = d.pop("derivedFrom", UNSET)

        organization: Union[Unset, BaseAssaySchemaOrganization] = UNSET
        _organization = d.pop("organization", UNSET)
        if not isinstance(_organization, Unset):
            organization = BaseAssaySchemaOrganization.from_dict(_organization)

        system_name = d.pop("systemName", UNSET)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = ArchiveRecord.from_dict(_archive_record)

        assay_result_schema = cls(
            field_definitions=field_definitions,
            id=id,
            name=name,
            type=type,
            derived_from=derived_from,
            organization=organization,
            system_name=system_name,
            archive_record=archive_record,
        )

        return assay_result_schema
