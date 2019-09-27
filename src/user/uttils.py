from src.user.models import User


def get_or_create_user_through_github(github_profile: dict) -> User:

    user: User or None = User.query.filter_by(
        email=github_profile['email']).first()

    if user is not None:
        return user

    return User(
        email=github_profile['email'],
        login=github_profile['login'],
        is_oauth=True,
    ).save()
