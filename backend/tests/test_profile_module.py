from __future__ import annotations


def test_profile_crud_and_username_availability(client, auth_headers):
    missing_response = client.get("/api/v1/profile/me", headers=auth_headers)
    assert missing_response.status_code == 404

    availability_response = client.get(
        "/api/v1/profile/username-availability",
        query_string={"username": "cyberanalyst"},
        headers=auth_headers,
    )
    assert availability_response.status_code == 200
    assert availability_response.get_json()["data"]["available"] is True

    create_response = client.post(
        "/api/v1/profile/me",
        headers=auth_headers,
        json={
            "full_name": "Demo Analyst",
            "username": "cyberanalyst",
            "college": "CTID College",
            "course": "Cyber Threat Intelligence",
            "organization": "CTID Lab",
            "country": "Nigeria",
            "bio": "Focused on cyber threat intelligence and SOC operations.",
            "avatar": None,
            "preferred_theme": "dark",
        },
    )
    assert create_response.status_code == 201
    assert create_response.get_json()["data"]["username"] == "cyberanalyst"

    profile_response = client.get("/api/v1/profile/me", headers=auth_headers)
    assert profile_response.status_code == 200
    assert profile_response.get_json()["data"]["email"] == "demo@ctid.local"

    update_response = client.put(
        "/api/v1/profile/me",
        headers=auth_headers,
        json={
            "full_name": "Demo Analyst Updated",
            "username": "cyberanalyst",
            "college": "CTID College",
            "course": "Cyber Threat Intelligence",
            "organization": "CTID Lab",
            "country": "Nigeria",
            "bio": "Updated bio for the CTID profile module.",
            "avatar": None,
            "preferred_theme": "system",
        },
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["data"]["full_name"] == "Demo Analyst Updated"


def test_profile_routes_require_jwt(client):
    response = client.get("/api/v1/profile/me")
    assert response.status_code == 401
