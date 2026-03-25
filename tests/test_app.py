import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# Utility to reset activities state before each test
def reset_activities():
    for activity in activities.values():
        # Reset to original participants for test isolation
        if activity["description"].startswith("Learn strategies and compete in chess tournaments"):
            activity["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
        elif activity["description"].startswith("Learn programming fundamentals"):
            activity["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
        elif activity["description"].startswith("Physical education"):
            activity["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
        elif activity["description"].startswith("Music band practice"):
            activity["participants"] = ["alex@mergington.edu"]
        elif activity["description"].startswith("Art and painting"):
            activity["participants"] = ["marcus@mergington.edu", "jessica@mergington.edu"]
        elif activity["description"].startswith("Science experiments"):
            activity["participants"] = ["taylor@mergington.edu"]
        elif activity["description"].startswith("Student government"):
            activity["participants"] = ["sarah@mergington.edu", "david@mergington.edu"]
        elif activity["description"].startswith("Debate and public speaking"):
            activity["participants"] = ["lucas@mergington.edu", "aisha@mergington.edu"]
        elif activity["description"].startswith("Drama and theater"):
            activity["participants"] = ["ryan@mergington.edu"]

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    # Arrange: Reset activities before each test
    reset_activities()
    yield
    reset_activities()

def test_get_activities():
    # Arrange is handled by fixture
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)

def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert "Signed up" in response.json()["message"]

def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_unregister_success():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    assert "Unregistered" in response.json()["message"]

def test_unregister_not_signed_up():
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]

def test_unregister_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
