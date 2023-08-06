from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.assay_run_note_part_type import AssayRunNotePartType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRunNotePart")


@attr.s(auto_attribs=True)
class AssayRunNotePart:
    """  """

    assay_run_id: Union[Unset, None, str] = UNSET
    assay_run_schema_id: Union[Unset, str] = UNSET
    type: Union[Unset, AssayRunNotePartType] = UNSET
    indentation: Union[Unset, int] = 0

    def to_dict(self) -> Dict[str, Any]:
        assay_run_id = self.assay_run_id
        assay_run_schema_id = self.assay_run_schema_id
        type: Union[Unset, int] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        indentation = self.indentation

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if assay_run_id is not UNSET:
            field_dict["assayRunId"] = assay_run_id
        if assay_run_schema_id is not UNSET:
            field_dict["assayRunSchemaId"] = assay_run_schema_id
        if type is not UNSET:
            field_dict["type"] = type
        if indentation is not UNSET:
            field_dict["indentation"] = indentation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_run_id = d.pop("assayRunId", UNSET)

        assay_run_schema_id = d.pop("assayRunSchemaId", UNSET)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = AssayRunNotePartType(_type)

        indentation = d.pop("indentation", UNSET)

        assay_run_note_part = cls(
            assay_run_id=assay_run_id,
            assay_run_schema_id=assay_run_schema_id,
            type=type,
            indentation=indentation,
        )

        return assay_run_note_part
