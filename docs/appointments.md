# Appointment
A patient can only have one appointment on one day. If need to modify an appointment, delete the appointment first, then post a new one.

## Make an Appointment

### POST `/v1/appointment`
> to make an appointment, post with data like this:
```
{
    'doctorid':'d001',
    'datatimeslot':'201511201300',
    'patientid':'p001',
    'illness': 'xxx',
}
```
> returns if the action success


## Look up an Appointment

### GET `/v1/appointment/doctorid/date`
> such as /v1/appointment/20151205
> returns the available appointments
>
```
{
    '1300':'1',
    '1430':'0',
    ...
}
```

## Look up an Appointment

### GET `/v1/appointment/doctorID/datetimeslot/patientID`
> returns the info of the appointment

## Delete an Appointment

### DELETE `/v1/appointment/doctorID/datetimeslot/patientID`
> returns if the deletion success
