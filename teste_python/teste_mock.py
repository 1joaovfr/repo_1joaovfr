import pytest  # Importa o pytest, uma biblioteca para facilitar a escrita de testes.
from unittest.mock import Mock, patch  # Importa Mock e patch para simular objetos e funções.
from app import App  # Importa a classe App que será testada, localizada no arquivo app.py.

@pytest.fixture
def app():
    mock_db = Mock()  # Cria um mock (simulação) do banco de dados Firebase.
    return App(db=mock_db)  # Retorna uma instância de App usando o mock do banco de dados.

def test_format_cpf(app):
    assert app.format_cpf("12345678901") == "123.456.789-01"  # Verifica se o método format_cpf formata corretamente um CPF com 11 dígitos.

    with pytest.raises(ValueError, match="O CPF deve conter 11 dígitos."):  # Verifica se o método lança um erro quando o CPF não tem 11 dígitos.
        app.format_cpf("1234567890")  # Testa um CPF inválido.

def test_format_salary(app):
    assert app.format_salary("1500") == "R$1,500.00"  # Verifica se o método format_salary formata corretamente o salário.

    with pytest.raises(ValueError, match="O salário deve ser um número válido."):  # Verifica se o método lança um erro quando o salário não é um número válido.
        app.format_salary("abc")  # Testa um salário inválido.

@patch("app.messagebox.showinfo")  # Substitui temporariamente a função messagebox.showinfo por um mock para evitar janelas reais durante o teste.
def test_register_verify_success(mock_messagebox, app):
    mock_collection = Mock()  # Cria um mock da coleção do Firebase.
    app.db.collection.return_value = mock_collection  # Configura o mock para retornar mock_collection quando app.db.collection for chamado.

    mock_doc = Mock()  # Cria um mock do documento do Firebase.
    mock_collection.document.return_value = mock_doc  # Configura o mock para retornar mock_doc quando mock_collection.document for chamado.

    app.register_verify(  # Chama o método register_verify com dados de teste.
        nome="João",
        cpf="12345678901",
        setor="RH",
        salario="2000",
        cargo="Gerente"
    )

    mock_doc.set.assert_called_once_with({  # Verifica se o método set foi chamado no mock do documento com os dados formatados corretamente.
        'Nome': "João",
        'Cpf': "123.456.789-01",
        'Setor': "RH",
        'Salario': "R$2,000.00",
        'Cargo': "Gerente"
    })

    mock_messagebox.assert_called_once_with(  # Verifica se a função messagebox.showinfo foi chamada para exibir uma mensagem de sucesso.
        title="Alert",
        message="Colaborador João cadastrado com sucesso!"
    )

@patch("app.messagebox.showinfo")  # Substitui temporariamente a função messagebox.showinfo por um mock para evitar janelas reais durante o teste.
def test_register_verify_missing_fields(mock_messagebox, app):
    app.register_verify(  # Chama o método register_verify com alguns campos vazios.
        nome="",
        cpf="",
        setor="RH",
        salario="2000",
        cargo="Gerente"
    )

    mock_messagebox.assert_called_once_with(  # Verifica se a função messagebox.showinfo foi chamada para exibir uma mensagem de erro.
        title="Alert",
        message="Todos os campos devem ser preenchidos."
    )
