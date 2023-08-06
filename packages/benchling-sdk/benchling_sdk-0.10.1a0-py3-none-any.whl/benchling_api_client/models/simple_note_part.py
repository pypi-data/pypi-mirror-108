from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.entry_link import EntryLink
from ..models.simple_note_part_type import SimpleNotePartType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SimpleNotePart")


@attr.s(auto_attribs=True)
class SimpleNotePart:
    """Simple note parts include the following types: - 'text': plain text - 'code': preformatted code block - 'list_bullet': one "line" of a bulleted list - 'list_number': one "line" of a numbered list"""

    links: Union[Unset, List[EntryLink]] = UNSET
    text: Union[Unset, str] = UNSET
    type: Union[Unset, SimpleNotePartType] = UNSET
    indentation: Union[Unset, int] = 0

    def to_dict(self) -> Dict[str, Any]:
        links: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.links, Unset):
            links = []
            for links_item_data in self.links:
                links_item = links_item_data.to_dict()

                links.append(links_item)

        text = self.text
        type: Union[Unset, int] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        indentation = self.indentation

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if links is not UNSET:
            field_dict["links"] = links
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

        text = d.pop("text", UNSET)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = SimpleNotePartType(_type)

        indentation = d.pop("indentation", UNSET)

        simple_note_part = cls(
            links=links,
            text=text,
            type=type,
            indentation=indentation,
        )

        return simple_note_part
