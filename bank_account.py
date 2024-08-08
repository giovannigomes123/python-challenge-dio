from person import Person

class Account:
    agency = "0001"
    account_number = 1

    def __init__(self, cpf):
        self.cpf = cpf
        self.balance = 0
        self.agency = Account.agency
        self.account = Account.account_number
        Account.account_number += 1
        self.num_withdrawalss = 0
        self.bank_statement = ""

    def return_data(self):
        return f"CPF: {self.cpf}\nAccount: {self.account}\nAgency: {self.agency}"
    
    def deposit(self, value):
        # Verifica se o valor é um número
        if type(value) not in [int, float]:  # Verifica se 'value' é um número
            return "Invalid value, please enter a number."
        
        if value > 0:
            self.balance += value
            self.bank_statement += f"Deposit: {value:.2f}\n"
        else:  # Se o número for negativo
            return "Invalid value, please enter a value greater than 0."
        
    def withdrawals(self, value):
        # Verifica se o valor é um número
        if type(value) not in [int, float]:  # Verifica se 'value' é um número
            return "Invalid value, please enter a number."
        
        if value <= 500 and value > 0 and self.num_withdrawalss < 3:
            self.num_withdrawalss += 1
            self.balance -= value
            self.bank_statement += f"Withdrawal: {value:.2f}\n"
        elif value > 500:
            return "You can only withdraw a value equal to or lower than 500."
        elif value <= 0:
            return "You can only withdraw positive values."
        elif self.num_withdrawalss >= 3:
            return "Operation failed, you have made 3 withdrawals today."
    
    def get_statement(self):
        return f"Bank Balance: {self.balance}\n{self.bank_statement}"
