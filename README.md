# Backend-apis

API's created with Django(Rest Framework) and SimpleJWT for JWT authentication.

## Tutorial App

API consists endpoints for:

  1. User Registration/ signup. (/users/)

  2. Login(post)/Logout(delete) with the use of JWT tokens. (/access-tokens/)

  3. Refresh JWT token. (/access-token/refresh)
  
  4. Create the ideas(another model) and get the ideas with pagination(10). (/ideas/)
  
  5. Get, Update, Delete particular idea with its id. (/ideas/<int:id>/)
 

Also use a custom middleware to authorize user from Header["X-Access-Token"].


Create group(owner, admin, staff) with command `python manage.py create-groups`.

Added endpoint 6. A user can be added to a permission group by owner only. (/assign-group)

APIs are live here https://backend-apis-django.herokuapp.com/


## Multitenant App

multitenant_app is an another app bind with the same project "tutorial_1".

Company setted as a tenant that may have users and documents.

APIs consists Endpoints for:

    1. User and Company registration simultaneously and send an email for confirmation.

    2. Actiavte User via activation link.

    3. Login, Logout, for the users to get access token.

    4. Add members to company and send them activation url.

    5. Update, Delete the User details.

    6. Create, get the Documents by the authentic users.

    7. Update, delete the doucments bt the authentic users.

To send email, we use SendGrid. To create Token we use, `rest_framework_simplejwt`.

