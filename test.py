class bank:
    def __init__(self, bank_name, interest_rate):
        self.bank_name = bank_name
        self.interest_rate = interest_rate

    def getInfo(self):
        print(f"bank name: {self.bank_name} | interest rate: {self.interest_rate}")

class bank_employee:
    def __init__(self, emp_name, emp_salary):
        self.emp_name = emp_name
        self.emp_salary = emp_salary

    ## class as a parameter
    def getBankAndEmployeeInfo(self, bank):
        print(f"employee name:{self.emp_name}")
        print(f"employee salary: {self.emp_salary}")
        print(f"bank name: {bank.bank_name} | interest rate: {bank.interest_rate}")

bank1 = bank()
    
employee = bank_employee('shiva', 40000)
employee.getBankAndEmployeeInfo(bank)