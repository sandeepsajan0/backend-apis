from rest_framework_simplejwt.tokens import RefreshToken


def get_activation_token(user):
    token = RefreshToken.for_user(user)
    return str(token)


def get_access_token(refresh):
    token = RefreshToken(refresh)
    return str(token.access_token)
