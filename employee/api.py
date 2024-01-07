from ninja import UploadedFile, File
from django.core.files.storage import FileSystemStorage
from .schemas import EmployeeIn, EmployeeOut
from ninja import NinjaAPI
from .models import Employee
from django.shortcuts import get_object_or_404


api = NinjaAPI(version="2.0.0")


@api.post("/employees")
def create_employee(request, payload: EmployeeIn, cv: UploadedFile = File(...)):
    payload_dict = payload.dict()
    employee = Employee(**payload_dict)
    employee.cv.save(cv.name, cv)  # will save model instance as well
    return {"id": employee.id}


# If you just need to handle a file upload:
STORAGE = FileSystemStorage()


@api.post("/upload")
def create_upload(request, cv: UploadedFile = File(...)):
    filename = STORAGE.save(cv.name, cv)
    # Handle things further


@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee


@api.get("/employees", response=list[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs


@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}


"""
Note

Here we used the payload.dict method to set all object attributes:

for attr, value in payload.dict().items()

You can also do this more explicit:


employee.first_name = payload.first_name
employee.last_name = payload.last_name
employee.department_id = payload.department_id
employee.birthdate = payload.birthdate
"""

### PARTIAL UPDATE ###

"""
Partial updates

To allow the user to make partial updates, use payload.dict(exclude_unset=True).items(). This ensures that only the specified fields get updated.

Enforcing strict field validation

By default, any provided fields that don't exist in the schema will be silently ignored. To raise an error for these invalid fields, you can set extra = "forbid" in the schema's Config class. For example:

```
class EmployeeIn(Schema):
    # your fields here...

    class Config:
        extra = "forbid"
```

"""


@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
