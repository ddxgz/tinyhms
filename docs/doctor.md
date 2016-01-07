# Doctor

Send all requests with headers include:
> "token":token_from_auth

> "role":the_role_when_you_auth


### POST `/v1/doctor`

> Administrator only. Need a unique employee id to avoid duplicated registration. To register a doctor, post with data like this:

```
{
        "firstname":"",
        "lastname":"",
        "qualification":"",
        "profession": "xxx",
        "experience":"",
        "gender":"",
        "schedule":"",

}
```
> returns a doctor ID

### GET `/v1/doctor/{doctorid}`
> to get info of a doctor


### PUT `/v1/doctor/{doctorid}`
> to edit info of a doctor

```
{

        "qualification":"",
        "profession": "xxx",
        "experience":"",
        "gender":"",
        "schedule":"",
}
```



### DELETE `/v1/doctor/{doctorid}`
> to delete info of a doctor
