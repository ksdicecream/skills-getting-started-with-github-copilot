"""Tests for participant unregister endpoints."""

from src.app import activities


def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "daniel@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 200
    assert existing_email not in activities[activity_name]["participants"]


def test_unregister_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity_name = "Imaginary Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_not_found_for_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "not.registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": missing_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"


def test_unregister_mutates_only_target_activity(client):
    # Arrange
    target_activity = "Art Club"
    untouched_activity = "Music Ensemble"
    removed_email = "grace@mergington.edu"
    untouched_before = list(activities[untouched_activity]["participants"])

    # Act
    response = client.delete(
        f"/activities/{target_activity}/participants",
        params={"email": removed_email},
    )

    # Assert
    assert response.status_code == 200
    assert removed_email not in activities[target_activity]["participants"]
    assert activities[untouched_activity]["participants"] == untouched_before


def test_repeated_unregister_returns_not_found_second_time(client):
    # Arrange
    activity_name = "Drama Club"
    existing_email = "mia@mergington.edu"

    # Act
    first_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": existing_email},
    )
    second_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": existing_email},
    )

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 404
    assert second_response.json()["detail"] == "Participant not found in activity"
