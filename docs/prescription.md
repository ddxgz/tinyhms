# Prescription
A doctor can make prescriptions on a patient

## Make a Prescription

### POST `/v1/prescription/{doctorid}/{patientid}`
> to make a prescription on a patient, post with data like this:
```
{
    "drug_name":"",
    "datetime":"",
    "after_meal":"",
    "amount":"",
    "dosage_per_day":"",
    "description":"",
}
```
> returns a drug ID

## Get Prescriptions of a patient

### GET `/v1/prescriptions/{patientid}`
> to get all prescriptions of a patient
