from datetime import date

class Person:
    registered_cpfs = set()  # Atributo de classe para armazenar CPFs já cadastrados
    valid_sex = {"M", "F", "Other"}  # Conjunto de sexos válidos

    def __init__(self, cpf, name, address, city, state, sex, dateOfBirth):
        # Inicializa os atributos da pessoa
        self.cpf = cpf
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.sex = sex
        self.dateOfBirth = dateOfBirth  

    @classmethod
    def create_person(cls, cpf, name, address, city, state, sex, dateOfBirth):
        # Verifica se o CPF já está registrado
        if cpf in cls.registered_cpfs:
            raise ValueError("CPF already registered.")
        
        # Verifica se o sexo é válido
        if sex not in cls.valid_sex:
            raise ValueError("Sex is not valid, sex must be 'M', 'F' or 'Other'")
        
        # Verifica a idade do usuário
        today = date.today()
        # Calcula a idade completa
        age = today.year - dateOfBirth.year
        
        # Verifica se o aniversário já ocorreu este ano
        if (today.month, today.day) < (dateOfBirth.month, dateOfBirth.day):
            age -= 1  # Ajusta a idade se o aniversário ainda não ocorreu neste ano
        
        # Se a idade for menor que 18, levanta um erro
        if age < 18:
            raise ValueError("User must be at least 18 years old to create an account.")
        
        # Cria a instância da pessoa se todas as validações passarem
        person = cls(cpf, name, address, city, state, sex, dateOfBirth)
        cls.registered_cpfs.add(cpf)  # Adiciona o CPF ao conjunto de CPFs registrados
        return person
