# Auth
Post request with username and password to certain api for a certain role, returns a token, the token and the role should be put in header for further requests.

## Login as Admin

### POST `/v1/auth/{admin}`
> post with data like this:

```
{
    "username":"d001",
    "password":"201511201300"
}
```

> returns if the access token or 0 on failure

## Login as Doctor

### POST `/v1/auth/doctor`
> post with data like this:
```
{
    "username":"d001",
    "password":"201511201300"
}
```
> returns if the access token or 0 on failure


## Login as Patient

### POST `/v1/auth/patient`
> post with data like this:

```
{
    "username":"d001",
    "password":"201511201300"
}
```
> returns if the access token or 0 on failure

# Authentication when make requests
Send requests with headers include:
> "token":token_from_auth

> "role":the_role_when_you_auth
