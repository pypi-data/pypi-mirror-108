import datetime
from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.entry import Entry
from ..models.entry_updated_review_record_event_event_type import EntryUpdatedReviewRecordEventEventType
from ..models.event_base_schema import EventBaseSchema
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryUpdatedReviewRecordEvent")


@attr.s(auto_attribs=True)
class EntryUpdatedReviewRecordEvent:
    """  """

    entry: Union[Unset, Entry] = UNSET
    event_type: Union[Unset, EntryUpdatedReviewRecordEventEventType] = UNSET
    updates: Union[Unset, List[str]] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    deprecated: Union[Unset, bool] = UNSET
    excluded_properties: Union[Unset, List[str]] = UNSET
    id: Union[Unset, str] = UNSET
    schema: Union[Unset, None, EventBaseSchema] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.entry, Unset):
            entry = self.entry.to_dict()

        event_type: Union[Unset, int] = UNSET
        if not isinstance(self.event_type, Unset):
            event_type = self.event_type.value

        updates: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.updates, Unset):
            updates = self.updates

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
        if entry is not UNSET:
            field_dict["entry"] = entry
        if event_type is not UNSET:
            field_dict["eventType"] = event_type
        if updates is not UNSET:
            field_dict["updates"] = updates
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
        entry: Union[Unset, Entry] = UNSET
        _entry = d.pop("entry", UNSET)
        if not isinstance(_entry, Unset):
            entry = Entry.from_dict(_entry)

        event_type = None
        _event_type = d.pop("eventType", UNSET)
        if _event_type is not None and _event_type is not UNSET:
            event_type = EntryUpdatedReviewRecordEventEventType(_event_type)

        updates = cast(List[str], d.pop("updates", UNSET))

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

        entry_updated_review_record_event = cls(
            entry=entry,
            event_type=event_type,
            updates=updates,
            created_at=created_at,
            deprecated=deprecated,
            excluded_properties=excluded_properties,
            id=id,
            schema=schema,
        )

        entry_updated_review_record_event.additional_properties = d
        return entry_updated_review_record_event

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
