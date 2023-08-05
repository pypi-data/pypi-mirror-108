"""Flask extension for using “specification first” principle."""

__version__ = "0.1.1"

from typing import List

from flask import Flask

from .spec_parser import Parameter, Specification


class FlaskIntegration:
    @staticmethod
    def route(route_path: str, route_parameters: List[Parameter] = None) -> str:
        if route_parameters:
            parameter_types = {"string": "", "integer": "int:", "number": "float:"}

            modified_route_path = route_path.replace("{", "<")
            modified_route_path = modified_route_path.replace("}", ">")
            for param in route_parameters:
                if getattr(param, "in") == "path":
                    modified_route_path = modified_route_path.replace(
                        f"<{param.name}>",
                        f"<{parameter_types[param.schema['type']]}{param.name}>",
                    )

            return modified_route_path
        else:
            return route_path


class First:
    """This class is used to generation routes from OpenAPI specification."""

    def __init__(self, app: Flask = None, path_to_spec: str = None) -> None:
        if path_to_spec is None:
            raise ValueError("Path to specification file not set!")

        self.app = app
        self.path_to_spec = path_to_spec

        if self.app is not None:
            self.init_app(app)

        self.specification = Specification(path_to_spec)

    def _route_registration(self, func) -> None:
        route = self.specification.get_route(func.__name__)
        self.app.add_url_rule(
            FlaskIntegration.route(route.path, getattr(route, "parameters", None)),
            func.__name__,
            func,
            methods=[route.method.upper()],
        )

    def init_app(self, app: Flask) -> None:
        app.config.setdefault("FIRST_RESPONSE_VALIDATION", False)
        app.specification = self.mapping

    def mapping(self, func) -> None:
        self._route_registration(func)
