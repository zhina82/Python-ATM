import uuid 
from datetime import datetime  
import csv 
import os 

file_name = "account.csv"

if not os.path.exists(file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("first_name,last_name,phone_number,date_of_birth,national_code,balance,email,account_number\n")

def generate_account_number(accounts):
    existing_numbers = [acc.account_number for acc in accounts] 
    while True:
        account_number = str(uuid.uuid4().int)[:12] 
        if account_number not in existing_numbers:
            return account_number

def validate_email(email):
    valid_domains = [
        'email.com',
        'gmail.com',
        'yahoo.com',
        'outlook.com',
        'hotmail.com',
        'live.com',
        'icloud.com'] 
    if '@' not in email or email.count('@') != 1:
        return False
    user, domain = email.split('@')
    if not user or not domain:
        return False
    if user[0] == '.' or user[-1] == '.':
        return False
    if domain not in valid_domains:
        return False
    return True

def validate_phone_number(phone_number):
    return phone_number.isdigit() and len(phone_number) == 11 and phone_number.startswith('09') 

def validate_national_code(national_code):
    return national_code.isdigit() and len(national_code) == 10

def validate_date(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d') 
        if date > datetime.now():
            return False
        return True
    except ValueError:
        return False

def validate_name(name):
    return name.isalpha() 

class BankAccount:
    def __init__(self, first_name, last_name, phone_number, date_of_birth, national_code, balance, email, account_number=None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.national_code = national_code
        self.balance = float(balance)
        self.email = email

        if account_number:
            self.account_number = account_number
        else:
            self.account_number = str(uuid.uuid4().int)[:12] 

    def save_to_file(self):
        with open(file_name, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([self.first_name, self.last_name, self.phone_number,
                             self.date_of_birth, self.national_code, self.balance,
                             self.email, self.account_number]) 

    def deposit(self, amount):
        if amount <= 0:
            print("Amount must be positive!")
            return False

        self.balance += amount
        print(f"Deposit successful! New balance: {self.balance}")
        self.update_csv()
        return True

    def withdraw(self, amount):
        if amount <= 0:
            print("Amount must be positive!")
            return False

        if amount > self.balance:
            print("Insufficient balance!")
            return False

        self.balance -= amount
        print(f"Withdrawal successful! New balance: {self.balance}")
        self.update_csv()
        return True

    def view_balance(self):
        print(f"Your balance: {self.balance}")

    def update_info(self, field, new_value):
        if field == 'first_name':
            if validate_name(new_value):
                self.first_name = new_value
            else:
                print("Invalid first name!")
                return

        elif field == 'last_name':
            if validate_name(new_value):
                self.last_name = new_value
            else:
                print("Invalid last name!")
                return

        elif field == 'phone_number':
            if validate_phone_number(new_value):
                self.phone_number = new_value
            else:
                print("Invalid phone number!")
                return
            
        elif field == 'date_of_birth':
            if validate_date(new_value):
                self.date_of_birth = new_value
            else:
                print("Invalid date format!")
                return
            
        elif field == 'national_code':
            if validate_national_code(new_value):
                self.national_code = new_value
            else:
                print("Invalid national code!")
                return

        elif field == 'email':
            if validate_email(new_value):
                self.email = new_value
            else:
                print("Invalid email format!")
                return
                    
        print("Update completed!")
        self.update_csv() 

    def transfer_to(self, other_account, amount):
        if amount <= 0:
            print("Amount must be positive!")
            return False
        if other_account.account_number == self.account_number:
            print("You cannot transfer money to your own account!")
            return False
        if amount > self.balance:
            print("Insufficient balance!")
            return False
        self.balance -= amount
        other_account.balance += amount
        print("Transfer successful!") 
        print(f"Your new balance: {self.balance}")
        self.update_csv()
        other_account.update_csv()
        return True

    def update_csv(self):
        accounts = []
        with open(file_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                accounts.append(row)

        updated = False
        for row in accounts:
            if row[7] == self.account_number:
                row[0] = self.first_name
                row[1] = self.last_name
                row[2] = self.phone_number
                row[3] = self.date_of_birth
                row[4] = self.national_code
                row[5] = str(self.balance)
                row[6] = self.email
                updated = True
                break

        if not updated:
            accounts.append([self.first_name, self.last_name, self.phone_number,
                             self.date_of_birth, self.national_code, self.balance,
                             self.email, self.account_number])

        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(accounts)

def load_accounts():
    accounts = []
    if not os.path.exists(file_name):
        return accounts
    with open(file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            account = BankAccount(row[0], row[1], row[2], row[3], row[4], float(row[5]), row[6], row[7])
            accounts.append(account) 
    return accounts

def find_account(accounts, account_number):
    for acc in accounts:
        if acc.account_number == account_number:
            return acc
    return None

accounts_list = load_accounts() 

while True:
    print('----------------------')
    print('1. Create your account.')
    print('2. Login to your account.') 

    choice = input('Choose an option: ')

    if choice == '1':
        while True:
            first_name = input('Enter your first name: ')
            if validate_name(first_name):
                break
            else:
                print('Please enter only letters!')

        while True:
            last_name = input('Enter your last name: ')
            if validate_name(last_name):
                break
            else:
                print('Please enter only letters!')

        while True:
            phone_number = input('Enter your phone number: ')
            if validate_phone_number(phone_number):
                break
            else:
                print('Please enter a valid 11-digit phone number starting with 09!') 

        while True:
            date_of_birth = input('Enter your date of birth(YYYY-MM-DD): ') 
            if validate_date(date_of_birth):
                break
            else:
                print('Invalid date! Please enter in format.')

        while True:
            national_code = input('Enter your national code: ')
            if validate_national_code(national_code):
                break
            else:
                print('Please enter only number and 10 character!')

        while True:
            try:
                balance = float(input('Enter your balance: '))
                if balance < 0:
                    print('Balance cannot be negative!')
                else:
                    break
            except ValueError:
                print('Please enter number for balance!')

        while True:
            email = input('Enter your email: ').strip()
            if validate_email(email):
                break
            print('Invalid email format!')

        account_number = generate_account_number(accounts_list) 
        new_account = BankAccount(first_name, last_name, phone_number, date_of_birth, national_code, balance, email, account_number) 
        new_account.save_to_file()
        accounts_list.append(new_account)
        print('Account created successfully!')
        print(f'* Account number: {new_account.account_number}') 

    elif choice == '2':
        acc_number = input('Enter your account number: ')
        account = find_account(accounts_list, acc_number)
        if not account:
            print("You don't have an account in our Bank!")
            continue


        print('----------------------')
        print('Welcome!') 

        while True:
            print('1. Deposit to account')
            print('2. Withdrawal from account')
            print('3. Update info')
            print('4. View balance')
            print('5. Transfer to account')
            print('6. Exit')

            option = input('Choose an option: ')

            if option == '1':
                while True:
                    try:
                        amount = float(input('Enter the deposit amount: ')) 
                        if account.deposit(amount):
                            break
                    except ValueError:
                        print('Please enter number!')

            elif option == '2':
                while True:
                    try:
                        amount = float(input('Enter the withdrawal amount: ')) 
                        if account.withdraw(amount):
                            break
                    except ValueError:
                        print('Please enter number!')

            elif option == '3':
                field = input('Which option? first_name, last_name, phone_number, date_of_birth, national_code, email: ').strip()
                if field not in ['first_name','last_name','phone_number','date_of_birth','national_code','email']:
                    print('Please choose from the options.')
                else:
                    new_value = input(f'Enter new value for {field}: ')
                    account.update_info(field, new_value) 

            elif option == '4':
                account.view_balance()

            elif option == '5':
                while True:
                    dest_acc_number = input("Enter destination account number: ")
                    dest_account = find_account(accounts_list, dest_acc_number)

                    if not dest_account:
                        print("Destination account not found!")
                        continue

                    if dest_account.account_number == account.account_number:
                        print("You cannot transfer money to your own account!")
                        continue
                    break
                while True:
                    try:
                        amount = float(input("Enter transfer amount: "))
                        if account.transfer_to(dest_account, amount):
                            break
                    except ValueError:
                        print("Please enter a valid number!")
            elif option == '6':
                print('Good Bye!')
                break 

            else:
                print("Invalid option! Please choose between 1 and 6.") 
    else:
        print("Invalid option! Please choose 1 or 2.")