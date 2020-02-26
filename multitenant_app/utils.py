from .models import Company, User
from django.http import Http404
from django.utils.translation import gettext as _


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
