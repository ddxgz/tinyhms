# Appointment
A patient can only have one appointment on one day. If need to modify an appointment, delete the appointment first, then post a new one.

Send all requests with headers include:
> "token":token_from_auth

> "role":the_role_when_you_auth


## Make an Appointment

### POST `/v1/appointment`
> to make an appointment, post with data like this:
```
{
    "doctorid":"d001",
    "datetimeslot":"201511201300",
    "patientid":"p001",
    "illness": "xxx",
}
```
> returns if the action success


## Look up Appointments of a doctor on a day

### GET `/v1/appointment/{doctorid}/{date}`
> such as /v1/appointment/20151205
> returns the available appointments
>
```
{
    "0900":"0",
    "1000":"0",
    "1300":"1",
    "1430":"1",
    ...
}
```

## Look up an Appointment

### GET `/v1/appointment/{doctorID}/{datetimeslot}/{patientID}`
> returns the info of the appointment

## Delete an Appointment

### DELETE `/v1/appointment/{doctorID}/{datetimeslot}/{patientID}`
> returns if the deletion success
