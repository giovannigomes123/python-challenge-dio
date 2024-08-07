bank_balance = 0  # saldo bancário
limit = 500
bank_statement = ""  # extrato bancário
num_withdraws = 0
deposit = 0

menu = ("""
[0] Deposit
[1] Withdraw
[2] Bank balance
[3] Quit

=> """)

while True:
    options = input(menu)
    if options == "0":
        deposit = float(input("Put a value to deposit in your account: "))
        if deposit > 0:
            bank_balance += deposit
            bank_statement += f"Deposit: R$ {deposit:.2f} \n"
        else:
            print("Your value is invalid. Try again.")
    elif options == "1":
        withdraws = float(input("Put a value to withdraw: "))
        if withdraws <= 0:
            print("Your value is invalid. Try again.")
        elif withdraws > limit:
            print("Your value is too high to withdraw.")
        elif num_withdraws >= 3:
            print("Operation failed, you made 3 withdrawals per day.")
        elif bank_balance <= 0:
            print("Your bank balance does not have money to withdraw.")
        elif bank_balance < withdraws:
            print("Your withdrawal value is too high.")
        else:
            num_withdraws += 1
            bank_balance -= withdraws
            bank_statement += f"Withdraw: R$ {withdraws:.2f} \n"
    elif options == "2":
        print(f"Your bank balance is R$ {bank_balance:.2f}")
        print(bank_statement if bank_statement else "No transactions made.")
    elif options == "3":
        print("Program finished")
        break
    else:
        print("Invalid option. Try again.")
