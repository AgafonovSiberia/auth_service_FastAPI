import json


async def test_create_user(client, get_user_from_database):
    user_data = {
        "full_name": "Nikolai",
        "login": "lol@kek.com",
        "password": "SamplePass1!",
    }

    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["full_name"] == user_data["full_name"]
    assert data_from_resp["login"] == user_data["login"]
    assert data_from_resp["is_active"] is False
    assert data_from_resp["is_admin"] is False

    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert data_from_resp["full_name"] == user_data["full_name"]
    assert data_from_resp["login"] == user_data["login"]
    assert data_from_resp["is_active"] is False
    assert data_from_resp["is_admin"] is False
    assert user_from_db["user_id"] == data_from_resp["user_id"]