# Objects


## Upload an object to a patient

### PUT `/v1/obj/patientid`
> put with headers like this:
```
    "objname: d001"
    "datetime: 201511201300"

```
> returns if the action success


## Download an object

### GET `/v1/obj/patientid/objid`
> returns the available appointments
>


## Delete an object 

### DELETE `/v1/obj/patientid/objid`
> returns if the deletion success
