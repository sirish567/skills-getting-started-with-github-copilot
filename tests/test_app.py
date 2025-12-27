import pytest
from fastapi import HTTPException

from src.app import (
    get_activities,
    signup_for_activity,
    unregister_from_activity,
    activities,
)


def test_get_activities():
    data = get_activities()
    assert isinstance(data, dict)
    assert "Soccer Team" in data


def test_signup_and_unregister_flow():
    activity = "Soccer Team"
    email = "test_user@example.com"

    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    resp = signup_for_activity(activity, email)
    assert email in activities[activity]["participants"]
    assert "Signed up" in resp["message"]

    # Duplicate signup should raise HTTPException
    with pytest.raises(HTTPException):
        signup_for_activity(activity, email)

    # Unregister
    resp_un = unregister_from_activity(activity, email)
    assert email not in activities[activity]["participants"]
    assert "Unregistered" in resp_un["message"]


def test_unregister_nonexistent_raises():
    activity = "Soccer Team"
    email = "no_such_user@example.com"

    # Ensure not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    with pytest.raises(HTTPException):
        unregister_from_activity(activity, email)
