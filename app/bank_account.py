from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)

# Configuração do Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo para a Tabela de Usuários
class User(db.Model):
    cpf = db.Column(db.String(11), primary_key=True)  # CPF tratado como string
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    sex = db.Column(db.String(5), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

    # Verificação de idade
    @classmethod
    def is_valid_age(cls, birthdate: date) -> bool:
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age >= 18

# Modelo para a Tabela de Contas Bancárias
class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpf = db.Column(db.String(11), db.ForeignKey('user.cpf'), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    agency = db.Column(db.String(4), default="0001")
    account_number = db.Column(db.Integer, nullable=False)
    num_withdrawals = db.Column(db.Integer, default=0)
    bank_statement = db.Column(db.Text, default="")

    def __repr__(self):
        return f'<Account {self.account_number}>'

    def deposit(self, value):
        if type(value) not in [int, float] or value <= 0:
            return "Invalid value, please enter a positive number."
        self.balance += value
        self.bank_statement += f"Deposit: {value:.2f}\n"
        db.session.commit()
        return f"Deposited {value:.2f} successfully."

    def withdraw(self, value):
        if type(value) not in [int, float]:
            return "Invalid value, please enter a number."
        if value > 500:
            return "You can only withdraw a value equal to or lower than 500."
        if value <= 0:
            return "You can only withdraw positive values."
        if self.num_withdrawals >= 3:
            return "Operation failed, you have made 3 withdrawals today."
        if value > self.balance:
            return "Insufficient balance."
        
        self.balance -= value
        self.num_withdrawals += 1
        self.bank_statement += f"Withdrawal: {value:.2f}\n"
        db.session.commit()
        return f"Withdrawn {value:.2f} successfully."

    def get_statement(self):
        return self.bank_statement

# Cria o banco de dados e as tabelas
with app.app_context():
    db.create_all()

# Rotas para renderizar as páginas HTML
@app.route('/')
def home():
    return render_template('register_user.html')

@app.route('/add_user_and_account', methods=['GET', 'POST'])
def add_user_and_account():
    if request.method == 'POST':
        data = request.form
        cpf = data.get('cpf')
        name = data.get('name')
        address = data.get('address')
        city = data.get('city')
        state = data.get('state')
        sex = data.get('sex')
        date_of_birth_str = data.get('date_of_birth')

        # Validação do sexo
        if sex not in ["M", "F", "Other"]:
            return jsonify({"error": "Invalid sex. Please choose 'M', 'F' or 'Other'."}), 400
        
        # Validação da idade
        try:
            date_of_birth = date.fromisoformat(date_of_birth_str)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        if not User.is_valid_age(date_of_birth):
            return jsonify({"error": "User must be at least 18 years old to create an account."}), 400

        # Criação do usuário e da conta bancária
        new_user = User(cpf=cpf, name=name, address=address, city=city, state=state, sex=sex, date_of_birth=date_of_birth)
        db.session.add(new_user)

        # Número da conta gerado automaticamente
        account_number = Account.query.count() + 1
        new_account = Account(cpf=cpf, account_number=account_number)
        db.session.add(new_account)

        db.session.commit()

        return jsonify({"message": f"User {name} and account {account_number} created successfully!"}), 201
    return render_template('register_user.html')
#
@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        data = request.form
        account_id = data.get('account_id')
        value = float(data.get('value'))

        account = Account.query.get(account_id)
        if account:
            return jsonify({"message": account.deposit(value)}), 200
        else:
            return jsonify({"error": "Account not found."}), 404
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        data = request.form
        account_id = data.get('account_id')
        value = float(data.get('value'))

        account = Account.query.get(account_id)
        if account:
            return jsonify({"message": account.withdraw(value)}), 200
        else:
            return jsonify({"error": "Account not found."}), 404
    return render_template('withdraw.html')

@app.route('/statement', methods=['GET'])
def statement():
    if request.method == 'GET':
        account_id = request.args.get('account_id')

        account = Account.query.get(account_id)
        if account:
            return jsonify({"statement": account.get_statement()}), 200
        else:
            return jsonify({"error": "Account not found."}), 404
    return render_template('statement.html')

if __name__ == '__main__':
    app.run(debug=True)
