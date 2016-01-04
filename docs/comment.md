# Comment
A doctor can make comments on a patient

## Make a Comment

### POST `/v1/comment/{doctorid}/{patientid}`
> to make a comment of a patient, post with data like this:
```
{
    "comment":"",
    "datetime":"",
}
```
> returns a comment ID

## Get Comments of a patient

### GET `/v1/comments/{patientid}`
> to get all comments of a patient
