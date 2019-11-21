from src.user.models import User


def get_or_create_user_through_github(github_profile: dict) -> User:

    if not github_profile['email']:
        return False

    user: User or None = User.query.filter_by(
        email=github_profile['email'],
    ).first()

    if user is not None:
        return user.update({
            'is_oauth': True,
        })

    return User(
        login=github_profile['login'],
        email=github_profile['email'],
        firstname=github_profile['name'],
        is_oauth=False,
    )
