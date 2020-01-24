# Backend-apis

API's created with Django(Rest Framework) and SimpleJWT for JWT authentication.

API consists endpoints for:

  1. User Registration/ signup. (/users/)

  2. Login(post)/Logout(delete) with the use of JWT tokens. (/access-tokens/)

  3. Refresh JWT token. (/access-token/refresh)
  
  4. Create the ideas(another model) and get the ideas with pagination(10). (/ideas/)
  
  5. Get, Update, Delete particular idea with its id. (/ideas/<int:id>/)
 

Also use a custom middleware to authorize user from Header["X-Access-Token"].

