"""
Module that offer some useful functions to validate the data against a JSON schema.
"""

import logging
import re
from typing import Any, Dict, Iterator, List, Tuple

import jsonschema
import ruamel.yaml

import jsonschema_gentypes.jsonschema

LOG = logging.getLogger(__name__)


def _extend_with_default(
    validator_class: "jsonschema.validators._DefaultTypesDeprecatingMetaClass",
) -> "jsonschema.validators._DefaultTypesDeprecatingMetaClass":
    """
    Add the default provider.

    Extends the jsonschema validator by adding a validator that fill the missing value with the default
    provided by the JSON schema.

    Arguments:
        validator_class: The validator class to be patched
    """
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(
        validator: "jsonschema.validators._DefaultTypesDeprecatingMetaClass",
        properties: Dict[str, jsonschema_gentypes.jsonschema.JSONSchemaItem],
        instance: Dict[str, Any],
        schema: jsonschema_gentypes.jsonschema.JSONSchemaItem,
    ) -> Iterator[jsonschema.exceptions.ValidationError]:
        """
        Set the default from the JSON schema to the data.

        Arguments:
            validator: The validator class
            properties: The properties
            instance: The data class
            schema: The full schema
        """
        for prop, subschema in properties.items():
            if "$ref" in subschema:
                ref = subschema["$ref"]
                resolve = getattr(validator.resolver, "resolve", None)
                if resolve is None:
                    with validator.resolver.resolving(ref) as resolved:
                        for error in validator.descend(instance, resolved):
                            yield error
                else:
                    _, resolved = validator.resolver.resolve(ref)
                    subschema = dict(subschema)  # type: ignore
                    subschema.update(resolved)
            if "default" in subschema:
                instance.setdefault(prop, subschema["default"])

        for error in validate_properties(
            validator,
            properties,
            instance,
            schema,
        ):
            yield error

    return jsonschema.validators.extend(
        validator_class,
        {"properties": set_defaults},
    )


def validate(
    filename: str, data: Dict[str, Any], schema: Dict[str, Any], default: bool = True
) -> Tuple[List[str], Dict[str, Any]]:
    """
    Validate the YAML, with it's JSON schema.

    Arguments:
        filename: Name used to generate the error messages
        data: The data structure to be validated (should be loaded with ruamel.yaml to have the lines numbers)
        schema: The loaded JSON schema
        default: If true, fill the data with the defaults provided in the JSON schema
    """
    schema_ref = schema.get("$schema", "default")
    schema_match = re.match(r"https?\:\/\/json\-schema\.org\/(.*)\/schema", schema_ref)
    Validator = {  # noqa: N806 # variable 'Validator' in function should be lowercase
        "draft-04": jsonschema.Draft4Validator,
        "draft-06": jsonschema.Draft6Validator,
        "draft-07": jsonschema.Draft7Validator,
    }.get(
        schema_match.group(1) if schema_match else "default",
        jsonschema.Draft7Validator,
    )
    if default:
        Validator = _extend_with_default(  # noqa: N806 # variable 'Validator' in function should be lowercase
            Validator
        )

    validator = Validator(schema)

    def format_error(error: jsonschema.exceptions.ValidationError) -> str:
        position = filename

        if hasattr(error.instance, "lc"):
            position = f"{filename}:{error.instance.lc.line + 1}:{error.instance.lc.col + 1}"
        else:
            curent_data = data
            parent = None
            if hasattr(curent_data, "lc"):
                parent = curent_data
            for path in error.path:
                curent_data = curent_data[path]
                if hasattr(curent_data, "lc"):
                    parent = curent_data
            if parent is not None:
                position = f"{filename}:{parent.lc.line + 1}:{parent.lc.col + 1}"  # type: ignore

        return (
            f" - {position} "
            f'({".".join([str(i) for i in error.path] if error.path else "/")}): '
            f"{error.message} (rule: "
            f'{".".join([str(i) for i in error.schema_path] if error.schema_path else "/")})'
        )

    return sorted([format_error(e) for e in validator.iter_errors(data)]), data


class ValidationError(Exception):
    """
    Exception thrown on validation issue.
    """


def load(
    filename: str,
    schema: Dict[str, Any],
    default: bool = True,
) -> Any:
    """
    Load and validate the YAML, with it's JSON schema.

    Arguments:
        filename: Path of the file that should be loaded
        schema: The JSON schema
        default: Should fill the data with the default provided in the JSON schema
    """
    with open(filename) as data_file:
        yaml = ruamel.yaml.YAML()  # type: ignore
        data = yaml.load(data_file)
        errors, data = validate(filename, data, schema, default)

    if errors:
        raise ValidationError("The config file is invalid:\n{}".format("\n".join(errors)))

    return data
