from copy import deepcopy

from openapi_spec_validator import validate_spec
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader  # noqa: F401


class Parameter:
    def __init__(self, options: dict):
        self._parse_parameter(options)

    def _parse_parameter(self, options):
        for key, value in options.items():
            setattr(self, key, value)


class Path:
    def __init__(self, path: str, method: str, method_options: dict):
        self.path = path
        self.method = method
        self._parse_method_options(method_options)

    def _parse_method_options(self, method_options: dict) -> None:
        for key, value in method_options.items():
            if key == "parameters":
                parameters = []
                for params in value:
                    parameters.append(Parameter(params))
                value = parameters
            setattr(self, key, value)


class Paths:
    def __init__(self, paths: dict):
        self._parse_paths(paths)

    def _parse_paths(self, paths: dict) -> None:
        parameters = []
        for path, options in paths.items():
            if "parameters" in options:
                parameters.extend(options.pop("parameters"))
            for method, method_options in options.items():
                if method_options.get("parameters") and parameters:
                    method_options["parameters"].extend(parameters)
                else:
                    method_options["parameters"] = parameters

                path_obj = Path(path, method, method_options)
                setattr(self, path_obj.operationId, path_obj)


class Specification:
    """This class implemented methods for specification API."""

    def __init__(self, path_to_spec: str):
        self.spec = self._load_from_yaml(path_to_spec)
        self._resolve_all_references()
        self.paths = Paths(self.spec["paths"])

    def resolve_reference(self, ref: str) -> dict:
        keys_from_ref = ref.split("/")[1:]

        value_from_ref = self.spec
        for key in keys_from_ref:
            value_from_ref = value_from_ref[key]

        return value_from_ref

    def _resolve_all_references(self) -> None:
        for _, options in self.spec["paths"].items():
            for method, method_options in options.items():
                if method == "parameters":
                    for parameter in method_options:
                        if "$ref" in parameter:
                            parameter.update(self.resolve_reference(parameter["$ref"]))
                            parameter.pop("$ref")
                    continue
                if "parameters" in method_options:
                    for parameter in method_options["parameters"]:
                        if "$ref" in parameter:
                            parameter.update(self.resolve_reference(parameter["$ref"]))
                            parameter.pop("$ref")

    def _load_from_yaml(self, spec_path: str) -> dict:
        with open(spec_path) as spec_file:
            spec = load(spec_file, Loader=Loader)
        validate_spec(deepcopy(spec))
        return spec

    def get_route(self, operation_id: str) -> Path:
        return getattr(self.paths, operation_id)
