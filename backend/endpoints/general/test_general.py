import os

from consts_tpl import miami_version_env_key


def test_get_version_not_set(client):
    response = client.get("/version")
    assert response.json == {'message': ''}


def test_get_version(client):
    expected_version = 'new version'
    os.environ[miami_version_env_key] = expected_version
    response = client.get("/version")
    assert response.json == {'message': expected_version}
