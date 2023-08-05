from flask_first import Specification


def test_specification__load_from_yaml(fx_config):
    spec = Specification(fx_config.PATH_TO_SPEC)
    assert spec
    assert spec.spec["info"]["title"] == "Simple API for testing Flask-First"
