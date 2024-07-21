from users.models import User


def register_user(data):
    password = data.pop("password")
    user = User.objects.create(**data)
    user.set_password(password)
    user.save()
    return user
