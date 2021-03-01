"""
3 types of common API authentications -
1) BASIC AUTHENTICATION - base64 encrypted userId/ pwd in every request , response body

2) Jwt ie JSON WEB TOKENS. JWT is generated when you 1st login (make sure it has 2FA) & stored in authentication header
    of every HTTP request. JWT token has 3 parts - header, payload, signature. If you need authorization, role of the
    user can be put in the JWT payload.

3) Oauth - Similar to JWT but delegates dealing with credentials to a 3rd party. Eg - ask user to authenticate using
    their google credentials, through Google. Google will send the API a token
"""
