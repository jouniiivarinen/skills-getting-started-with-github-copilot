"""
Tests for the FastAPI application endpoints using pytest and TestClient.
Following AAA (Arrange-Act-Assert) testing pattern.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture that provides a TestClient for testing the FastAPI app."""
    return TestClient(app)


class TestActivitiesEndpoints:
    """Test cases for the /activities endpoints."""

    def test_get_activities_success(self, client):
        """Test retrieving all activities successfully."""
        # Arrange
        # (No specific setup needed for this test)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        # Check that we have the expected activities
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_signup_for_activity_success(self, client):
        """Test signing up for an activity successfully."""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_for_nonexistent_activity(self, client):
        """Test signing up for a non-existent activity returns 404."""
        # Arrange
        activity_name = "NonExistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_participant(self, client):
        """Test signing up a student who is already enrolled returns 400."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in the initial data

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_unregister_from_activity_success(self, client):
        """Test unregistering from an activity successfully."""
        # Arrange
        activity_name = "Chess Club"
        email = "daniel@mergington.edu"  # Already in the initial data

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]

    def test_unregister_from_nonexistent_activity(self, client):
        """Test unregistering from a non-existent activity returns 404."""
        # Arrange
        activity_name = "NonExistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_nonexistent_participant(self, client):
        """Test unregistering a participant who is not enrolled returns 404."""
        # Arrange
        activity_name = "Chess Club"
        email = "notenrolled@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Participant not found" in data["detail"]