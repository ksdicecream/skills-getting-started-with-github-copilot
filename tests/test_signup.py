"""Tests for participant signup endpoints."""

from src.app import activities


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})

    # Assert
    assert response.status_code == 200
    assert new_email in activities[activity_name]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_mutates_only_target_activity(client):
    # Arrange
    target_activity = "Programming Class"
    untouched_activity = "Art Club"
    new_email = "focus.student@mergington.edu"
    untouched_before = list(activities[untouched_activity]["participants"])

    # Act
    response = client.post(
        f"/activities/{target_activity}/signup",
        params={"email": new_email},
    )

    # Assert
    assert response.status_code == 200
    assert new_email in activities[target_activity]["participants"]
    assert activities[untouched_activity]["participants"] == untouched_before


def test_signup_supports_url_encoded_activity_and_email(client):
    # Arrange
    activity_name = "Basketball Team"
    encoded_email = "first.last+team@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": encoded_email})

    # Assert
    assert response.status_code == 200
    assert encoded_email in activities[activity_name]["participants"]
