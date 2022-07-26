import pytest


@pytest.mark.django_db
def test_operator_access(unapproved_operator, operator_user):
    print(operator_user.full_name)
    return True
    # assert  unapproved_operator.approval_status == "PENDING_APPROVAL"
