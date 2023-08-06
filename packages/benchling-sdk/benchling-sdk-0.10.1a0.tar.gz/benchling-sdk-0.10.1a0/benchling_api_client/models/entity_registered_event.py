import datetime
from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.entity import Entity
from ..models.entity_registered_event_event_type import EntityRegisteredEventEventType
from ..models.event_base_schema import EventBaseSchema
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntityRegisteredEvent")


@attr.s(auto_attribs=True)
class EntityRegisteredEvent:
    """  """

    entity: Union[Unset, Entity] = UNSET
    event_type: Union[Unset, EntityRegisteredEventEventType] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    deprecated: Union[Unset, bool] = UNSET
    excluded_properties: Union[Unset, List[str]] = UNSET
    id: Union[Unset, str] = UNSET
    schema: Union[Unset, None, EventBaseSchema] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.entity, Unset):
            entity = self.entity.to_dict()

        event_type: Union[Unset, int] = UNSET
        if not isinstance(self.event_type, Unset):
            event_type = self.event_type.value

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        deprecated = self.deprecated
        excluded_properties: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.excluded_properties, Unset):
            excluded_properties = self.excluded_properties

        id = self.id
        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict() if self.schema else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if entity is not UNSET:
            field_dict["entity"] = entity
        if event_type is not UNSET:
            field_dict["eventType"] = event_type
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated
        if excluded_properties is not UNSET:
            field_dict["excludedProperties"] = excluded_properties
        if id is not UNSET:
            field_dict["id"] = id
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity: Union[Unset, Entity] = UNSET
        _entity = d.pop("entity", UNSET)
        if not isinstance(_entity, Unset):
            entity = Entity.from_dict(_entity)

        event_type = None
        _event_type = d.pop("eventType", UNSET)
        if _event_type is not None and _event_type is not UNSET:
            event_type = EntityRegisteredEventEventType(_event_type)

        created_at = None
        _created_at = d.pop("createdAt", UNSET)
        if _created_at is not None:
            created_at = isoparse(cast(str, _created_at))

        deprecated = d.pop("deprecated", UNSET)

        excluded_properties = cast(List[str], d.pop("excludedProperties", UNSET))

        id = d.pop("id", UNSET)

        schema = None
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = EventBaseSchema.from_dict(_schema)

        entity_registered_event = cls(
            entity=entity,
            event_type=event_type,
            created_at=created_at,
            deprecated=deprecated,
            excluded_properties=excluded_properties,
            id=id,
            schema=schema,
        )

        entity_registered_event.additional_properties = d
        return entity_registered_event

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
