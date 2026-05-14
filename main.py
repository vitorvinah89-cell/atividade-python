import sqlite3 as conector

# ---------------- CONEXÃO ----------------

conexao = conector.connect("clientes.db")
conexao.execute("PRAGMA foreign_keys = ON")
cursor = conexao.cursor()

# ---------------- CRIAÇÃO DAS TABELAS ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS Pessoa (
    cpf TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    nascimento TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Veiculo (
    placa TEXT PRIMARY KEY,
    cor TEXT NOT NULL,
    cpf_proprietario TEXT NOT NULL,
    
    FOREIGN KEY(cpf_proprietario)
    REFERENCES Pessoa(cpf)
)
""")

conexao.commit()

# ---------------- FUNÇÕES ----------------

def cadastrar_pessoa():
    try:
        cpf = input("CPF: ")
        nome = input("Nome: ")
        nascimento = input("Nascimento: ")

        comando = """
        INSERT INTO Pessoa VALUES (?, ?, ?)
        """

        cursor.execute(comando, (cpf, nome, nascimento))
        conexao.commit()

        print("Pessoa cadastrada!")

    except conector.IntegrityError:
        print("Erro: CPF já existe!")


def cadastrar_veiculo():
    try:
        placa = input("Placa: ")
        cor = input("Cor: ")
        cpf = input("CPF do proprietário: ")

        comando = """
        INSERT INTO Veiculo VALUES (?, ?, ?)
        """

        cursor.execute(comando, (placa, cor, cpf))
        conexao.commit()

        print("Veículo cadastrado!")

    except conector.IntegrityError:
        print("Erro: veículo duplicado ou CPF inexistente!")


def listar_relatorio():

    comando = """
    SELECT Pessoa.nome, Veiculo.placa, Veiculo.cor
    FROM Pessoa
    JOIN Veiculo
    ON Pessoa.cpf = Veiculo.cpf_proprietario
    """

    cursor.execute(comando)

    dados = cursor.fetchall()

    print("\nRELATÓRIO\n")

    for nome, placa, cor in dados:
        print(f"Proprietário: {nome}")
        print(f"Placa: {placa}")
        print(f"Cor: {cor}")
        print("-" * 20)


# ---------------- MENU ----------------

while True:

    print("\n1 - Cadastrar Pessoa")
    print("2 - Cadastrar Veículo")
    print("3 - Listar Relatório")
    print("4 - Sair")

    opcao = input("Escolha: ")

    if opcao == "1":
        cadastrar_pessoa()

    elif opcao == "2":
        cadastrar_veiculo()

    elif opcao == "3":
        listar_relatorio()

    elif opcao == "4":
        break

    else:
        print("Opção inválida!")

# ---------------- FECHAMENTO ----------------

cursor.close()
conexao.close()