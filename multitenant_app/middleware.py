from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _

from .models import Company


class SetTenantMiddleware(MiddlewareMixin):
    """
    Pass token from header to authorization
    """

    def process_request(self, request):
        host_name = request.get_host().split(":")[0].lower()
        url_prefix = host_name.split(".")[0]
        company = Company.objects.filter(url_prefix=url_prefix).first()
        if company is None:
            raise Http404(_("Not Found"))
        request.company = company
