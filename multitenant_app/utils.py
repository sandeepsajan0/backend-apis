from rest_framework_simplejwt.tokens import RefreshToken


def get_activation_token(user):
    token = RefreshToken.for_user(user)
    return str(token)


def get_access_token(refresh):
    token = RefreshToken(refresh)
    return str(token.access_token)


def get_activation_url(user, scheme, host):
    token = get_activation_token(user)
    company_name = user.company.url_prefix
    if (str(company_name) + ".") in str(host):
        host = host.replace((str(company_name) + "."), "")
    url = "{}://{}.{}/invitation/{}".format(scheme, company_name, host, token)

    return url
