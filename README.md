# Backend-apis

API's created with Django(Rest Framework) and SimpleJWT for JWT authentication.

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

