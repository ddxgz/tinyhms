# Objects

Send all requests with headers include:
> "token":token_from_auth

> "role":the_role_when_you_auth


## Upload an object to a patient

### 1. POST `/v1/obj/{patientid}`
> put with headers like this:
```
{
    "objname": "d001",
    "datetime": "201511201300",
    "description": "x-ray"
}
```
> returns a json contains auth_token and storage_url if the action success

### 2. PUT `storage_url`
with headers:
```
    "auth_token: token"
    "objname: d001"
    "datetime: 201511201300"
    "patientname: paname"
```


## Get objects list of a patietn

### GET `/v1/objs/{patientid}`
> returns the available appointments
>

## Download an object

### GET `/v1/obj/{patientid}/{objid}`
> returns a json contains auth_token and storage_url if the action success
>


## Delete an object

### DELETE `/v1/obj/{patientid}/{objid}`
> returns if the deletion success
