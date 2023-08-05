from typing import Tuple

from flask import jsonify

ITEM = {
    "uuid": "789d995f-3aa0-4bf8-a37b-2f2f2086d503",
    "name": "test_item",
    "description": "Item from tests.",
}


def test_specification__create_item(fx_app, fx_client):
    @fx_app.specification
    def create_item() -> Tuple:
        return jsonify(ITEM), 201

    r_get = fx_client.post("/items")
    assert r_get.status_code == 201
    assert r_get.json["uuid"] == ITEM["uuid"]
    assert r_get.json["name"] == ITEM["name"]
    assert r_get.json["description"] == ITEM["description"]


def test_specification__items_list(fx_app, fx_client):
    @fx_app.specification
    def items_list() -> list:
        return jsonify([ITEM])

    args = {"page": 1, "per_page": 10}
    r_get = fx_client.get("/items", query_string=args)
    assert r_get.status_code == 200
    assert r_get.json[0]
    assert r_get.json[0]["uuid"] == ITEM["uuid"]
    assert r_get.json[0]["name"] == ITEM["name"]
    assert r_get.json[0]["description"] == ITEM["description"]


def test_specification__add_route_with_path_parameters(fx_app, fx_client):
    @fx_app.specification
    def get_item(uuid: str) -> dict:
        item = {**ITEM, **{"uuid": uuid}}
        return jsonify(item)

    item_uuid = "789d995f-3aa0-4bf8-a37b-2f2f2086d504"
    r_get = fx_client.get(f"/items/{item_uuid}")
    assert r_get.status_code == 200
    assert r_get.json["uuid"] == item_uuid


def test_specification__all_type_url_parameters(fx_app, fx_client):
    @fx_app.specification
    def get_path_params(path_str: str, path_int: int, path_float: float) -> dict:
        assert isinstance(path_str, str)
        assert isinstance(path_int, int)
        assert isinstance(path_float, float)

        item = {
            "path_str": path_str,
            "path_int": path_int,
            "path_float": path_float,
        }
        return jsonify(item)

    path_params = {
        "path_str": "test_string",
        "path_int": 1234567890,
        "path_float": 12345.67890,
    }
    r_get = fx_client.get(
        f"/get_path_params/{path_params['path_str']}/{path_params['path_int']}/{path_params['path_float']}"  # noqa: E501
    )
    assert r_get.status_code == 200
    assert r_get.json["path_str"] == path_params["path_str"]
    assert r_get.json["path_int"] == path_params["path_int"]
    assert r_get.json["path_float"] == path_params["path_float"]
