from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.entry_link import EntryLink
from ..models.entry_table import EntryTable
from ..models.table_note_part_type import TableNotePartType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TableNotePart")


@attr.s(auto_attribs=True)
class TableNotePart:
    """ A table with rows and columns of text """

    links: Union[Unset, List[EntryLink]] = UNSET
    table: Union[Unset, EntryTable] = UNSET
    text: Union[Unset, str] = UNSET
    type: Union[Unset, TableNotePartType] = UNSET
    indentation: Union[Unset, int] = 0

    def to_dict(self) -> Dict[str, Any]:
        links: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.links, Unset):
            links = []
            for links_item_data in self.links:
                links_item = links_item_data.to_dict()

                links.append(links_item)

        table: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.table, Unset):
            table = self.table.to_dict()

        text = self.text
        type: Union[Unset, int] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        indentation = self.indentation

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if links is not UNSET:
            field_dict["links"] = links
        if table is not UNSET:
            field_dict["table"] = table
        if text is not UNSET:
            field_dict["text"] = text
        if type is not UNSET:
            field_dict["type"] = type
        if indentation is not UNSET:
            field_dict["indentation"] = indentation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        links = []
        _links = d.pop("links", UNSET)
        for links_item_data in _links or []:
            links_item = EntryLink.from_dict(links_item_data)

            links.append(links_item)

        table: Union[Unset, EntryTable] = UNSET
        _table = d.pop("table", UNSET)
        if not isinstance(_table, Unset):
            table = EntryTable.from_dict(_table)

        text = d.pop("text", UNSET)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = TableNotePartType(_type)

        indentation = d.pop("indentation", UNSET)

        table_note_part = cls(
            links=links,
            table=table,
            text=text,
            type=type,
            indentation=indentation,
        )

        return table_note_part
