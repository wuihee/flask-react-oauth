# Flask-React OAuth

## OAuth Flow

- User Initiates Login from React
  - The React frontend displays a login button.
  - When the user clicks on it, React makes a request to the backend to initiate the OAuth flow.
- Flask Prepares the Authorization URL
  - On receiving the request from the frontend, Flask constructs the provider's (Google) authorization URL.
  - This includes essential parameters like the client ID, the requested scopes, and a redirect URI.
  - Flask responds to the frontend with this authorization URL.
- User is Redirected to Provider's Authorization Page
  - React takes the authorization URL and redirects the user's browser to the OAuth provider's site.
  - The user sees the familiar login page and logs in.
- Provider Redirects Back to The Redirect URI.
  - After the user authorizes, the provider redirects the user's browser back to the specified callback route.
  - This redirect URL includes a temporary authorization code in the query parameters.
- Flask Exchanges the Authorization Code for an Access Token.
  - Flask uses the authorization code, along with the client ID and client secret, to request an access token from the provider via a POST request.
  - If successful, the provider returns an access token.
- Flask Fetches User Profile Information.
  - Using the access token, Flask queries the provider's user info endpoint.
  - Flask gets back user details like their ID, name, email, etc.
- Identifying or Creating the User in Your Database
  - Flask checks if a user exists in the database or create a record.
- Flask Sends the Authentication Result Back to React
  - The server responds to React with a JWT token.
  - React stores this token securely so it can be used for future requests.
- Subsequent Authenticated Requests
  - Whenever React makes further API calls to the backend, it includes the token.
- Token Refreshing
  - If the token expires, Flask can use the refresh token to request a new access token from the provider behind the scenes.

## Resources

- [The OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749#section-1)
- [OAuth Authentication with Flask in 2023 by Miguel Grinberg](https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask-in-2023)
- [Using OAuth 2.0 to Access Google APIs](https://developers.google.com/identity/protocols/oauth2)
