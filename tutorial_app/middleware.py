from django.utils.deprecation import MiddlewareMixin

class CustomAuthMiddleware(MiddlewareMixin):
    """
    Pass token from header to authorization
    """
    # I think there will be an option in the JWT library to specify the 
    # header, use that instead of this.
    def process_request(self, request):
        if 'X-Access-Token' in list(request.headers.keys()):
            request.META['HTTP_AUTHORIZATION'] = "Bearer " + request.headers['X-Access-Token']
