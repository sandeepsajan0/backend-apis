from .models import Company, User


def hostname_from_request(request):
    # split on `:` to remove port
    return request.get_host().split(":")[0].lower()


def tenant_from_request(request):
    hostname = hostname_from_request(request)
    url_prefix = hostname.split(".")[0]
    return Company.objects.filter(url_prefix=url_prefix).first()


def is_company_user(username, company):
    try:
        user = User.objects.get(username=username)
        print(user, company, user.company)
    except:
        print("dsds")
        return False
    if user.company == company:
        return True
    else:
        return False
