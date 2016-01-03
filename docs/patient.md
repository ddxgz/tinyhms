

### POST `/v1/patient`
> to register a patient, post with data like this:
```
{
    "first_name":"",
    "last_name":"",
    "birthdate":"",
    "mobile_phone","",
    "email":"",
    "address":"",
    "gender":"",
    "height":"",
    "weight":"",
    "blood_group":"",
    "occupation":"",
    "marriage":"",
    "reference":"",
    "doctor_in_charge":"",
    "allergy":[],
    "accompanied_by":"",
}
```
> returns a patient ID


### GET `/v1/patient/patientid`
> to get info of a patient


### PUT `/v1/patient/patientid`
> to edit info of a patient
```
{
    "first_name":"",
    "last_name":"",
    "birthdate":"",
    "mobile_phone","",
    "email":"",
    "address":"",
    "gender":"",
    "height":"",
    "weight":"",
    "blood_group":"",
    "occupation":"",
    "marriage":"",
    "reference":"",
    "doctor_in_charge":"",
    "allergy":[],
    "accompanied_by":"",
}
```

### DELETE `/v1/patient/patientid`
> to delete info of a doctor
