from datetime import date
from person import Person
from bank_account import Account

pessoa1 = Person("70984106519","Giovanni", "Rua Carlos Rios, 104", "Recife", "PE", "M", "09-01-1999")
santander = Account("70984106519")



menu = ("""
[0] Deposit
[1] Withdraw
[2] Bank balance
[3] Quit

=> """)

while True:
    options = input(menu)
    if options == "0":
        deposits = float(input("Put a value to deposit in your account: "))
        result = santander.deposit(deposits)
        if result:  # Exibe mensagem de erro se houver
            print(result)
        
    elif options == "1":
        withdraws = float(input("Put a value to withdraw: "))
        result = santander.withdrawals(withdraws)
        if result:  # Exibe mensagem de erro se houver
            print(result)
        
    elif options == "2":
        print(santander.get_statement())
        
    elif options == "3":
        print("Program finished")
        break
    else:
        print("Invalid option. Try again.")
