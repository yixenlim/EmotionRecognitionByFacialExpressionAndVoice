import os

class Employee:
    def __init__(self, id, name):
        self.id = id
        self.name = name

def getEmployeesInfo():
    employees_base_dir = os.path.join('Program', 'Employees')
    employees = []
    
    for employeeFolder in os.listdir(employees_base_dir):
        path = os.path.join(employees_base_dir, employeeFolder)
        for file in os.listdir(path):
            if file.endswith('info.txt'):
                infoFile = os.path.join(path, file)                
                with open(infoFile) as f:
                    info = f.read().splitlines()
                    emp = Employee(info[0],info[1])
                    employees.append(emp)
    return employees

def getEmployeeInfoById(id):
    employeesList = getEmployeesInfo()

    for employee in employeesList:
        if employee.id == id:
            employees = [employee]
            return employees

def getEmployeesIdList(idList):
    employeeList = getEmployeesInfo()

    for emp in employeeList:
        idList.append(str(emp.id)+' - '+emp.name)

    return idList