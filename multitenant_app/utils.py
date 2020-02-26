from .models import Company, User
from django.http import Http404
from django.utils.translation import gettext as _
from .commands import get_activation_token


def hostname_from_request(request):
    # split on `:` to remove port
    return request.get_host().split(":")[0].lower()


def tenant_from_request(request):
    hostname = hostname_from_request(request)
    url_prefix = hostname.split(".")[0]
    company = Company.objects.filter(url_prefix=url_prefix).first()
    if company is None:
        raise Http404(_("Not Found"))
    return company


def is_company_user(user, company):
    if user.company == company:
        return True
    else:
        return False


def get_activation_url(user, scheme, host):
    token = get_activation_token(user)
    company_name = user.company.url_prefix
    if (str(company_name) + ".") in str(host):
        host = host.replace((str(company_name) + "."), "")
    url = (
        scheme
        + "://"
        + str(company_name)
        + "."
        + str(host)
        + "/invitation/"
        + str(token)
    )
    return url
