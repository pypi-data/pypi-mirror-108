from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.assay_fields_create import AssayFieldsCreate
from ..models.assay_run_validation_status import AssayRunValidationStatus
from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRunCreate")


@attr.s(auto_attribs=True)
class AssayRunCreate:
    """  """

    fields: Union[Fields, AssayFieldsCreate]
    schema_id: str
    id: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    validation_comment: Union[Unset, str] = UNSET
    validation_status: Union[Unset, AssayRunValidationStatus] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        if isinstance(self.fields, Fields):
            fields = self.fields.to_dict()

        else:
            fields = self.fields.to_dict()

        schema_id = self.schema_id
        id = self.id
        project_id = self.project_id
        validation_comment = self.validation_comment
        validation_status: Union[Unset, int] = UNSET
        if not isinstance(self.validation_status, Unset):
            validation_status = self.validation_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fields": fields,
                "schemaId": schema_id,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if validation_comment is not UNSET:
            field_dict["validationComment"] = validation_comment
        if validation_status is not UNSET:
            field_dict["validationStatus"] = validation_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_fields(data: Union[Dict[str, Any]]) -> Union[Fields, AssayFieldsCreate]:
            fields: Union[Fields, AssayFieldsCreate]
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                fields = Fields.from_dict(data)

                return fields
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            fields = AssayFieldsCreate.from_dict(data)

            return fields

        fields = _parse_fields(d.pop("fields"))

        schema_id = d.pop("schemaId")

        id = d.pop("id", UNSET)

        project_id = d.pop("projectId", UNSET)

        validation_comment = d.pop("validationComment", UNSET)

        validation_status = None
        _validation_status = d.pop("validationStatus", UNSET)
        if _validation_status is not None and _validation_status is not UNSET:
            validation_status = AssayRunValidationStatus(_validation_status)

        assay_run_create = cls(
            fields=fields,
            schema_id=schema_id,
            id=id,
            project_id=project_id,
            validation_comment=validation_comment,
            validation_status=validation_status,
        )

        return assay_run_create
