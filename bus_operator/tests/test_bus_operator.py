import pytest


@pytest.mark.django_db
def test_operator_access(unapproved_operator, operator_user):
    print("full_name: ", operator_user.full_name)
    print("approval_status", unapproved_operator.approval_status)
    assert False