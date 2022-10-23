import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_my_user():
    user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
    assert len(User.objects.filter(username="john")) == 1
