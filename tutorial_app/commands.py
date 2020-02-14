from rest_framework_simplejwt.tokens import RefreshToken


def calculate_average_score(data):
    average_score = (data["ease"] + data["impact"] + data["confidence"]) / 3
    return average_score


# def get_token(user):
#     token = RefreshToken.for_user(user)
#     return {
#         "jwt": str(token.access_token),
#         "refresh-token": str(token),
#     }
