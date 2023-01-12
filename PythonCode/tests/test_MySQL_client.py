from unittest import TestCase
import pytest
from MySQL_client import MySQL_client


@pytest.fixture
def client():
    return MySQL_client("database.discordbothosting.com",
                        "u1604_6WUWgkmAxW",
                        "a3jXvb=fvbwOU=^3KQwO5s=b",
                        "s1604_ProjectSoftwareEngineering")


def test__fetchone(client):

    assert type(client._fetchone("sensor", "sensor_id")) == int
    assert type(client._fetchone("payload", "payload_id")) == int


def test_update_data_table(client):
    expected_result1 = client._fetchone("sensor", "sensor_id")
    expected_result2 = client._fetchone("payload", "payload_id")

    client.update_data_table()

    assert client._fetchone("data", "sensor_id") == expected_result1
    assert client._fetchone("data", "payload_id") == expected_result2


def test_reconnect(client):
    client.reconnect()
