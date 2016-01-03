# Discharge
A doctor can make discharge information on a patient

## Make a Discharge info

### POST `/v1/discharge/{doctorid}/{patientid}`
> to make discharge info of a patient, post with data like this:
```
{
    "indate":"",
    "room":"",
    "bed":"",
    "datetime":"",
    "outdate":"", #optional when post
    "description":"",
}
```
> returns a discharge ID


## Edit discharge info of a patient
### PUT `/v1/discharge/{doctorid}/{patientid}/{indate}`
> to edit info of a doctor

```
{
    "room":"",
    "bed":"",    
    "datetime":"",
    "outdate":"",
    "description":"",
}
```


## Get Discharges of a patient

### GET `/v1/discharges/{patientid}`
> to get all discharges of a patient
