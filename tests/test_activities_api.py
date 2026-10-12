def test_get_activities_returns_data_without_caching(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert response.json()["Chess Club"]["participants"] == ["student@mergington.edu"]


def test_signup_adds_participant(client):
    response = client.post(
        "/activities/Art%20Club/signup",
        params={"email": "new-student@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up new-student@mergington.edu for Art Club"
    }
    assert client.get("/activities").json()["Art Club"]["participants"] == [
        "new-student@mergington.edu"
    ]


def test_signup_rejects_duplicate_participant(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert client.get("/activities").json()["Chess Club"]["participants"] == [
        "student@mergington.edu"
    ]


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_removes_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered student@mergington.edu from Chess Club"
    }
    assert client.get("/activities").json()["Chess Club"]["participants"] == []


def test_delete_returns_404_for_unregistered_participant(client):
    response = client.delete(
        "/activities/Art%20Club/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_delete_returns_404_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown%20Club/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"