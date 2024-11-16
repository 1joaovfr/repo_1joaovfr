from tkinter import messagebox

class App:
    def __init__(self, db):
        self.db = db  # Firebase database instance

    def format_cpf(self, cpf):
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11:
            raise ValueError("O CPF deve conter 11 dígitos.")
        return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

    def format_salary(self, salario):
        try:
            salario_float = float(salario)
            return f'R${salario_float:,.2f}'
        except ValueError:
            raise ValueError("O salário deve ser um número válido.")

    def register_verify(self, nome, cpf, setor, salario, cargo):
        if not all([nome, cpf, setor, salario, cargo]):
            messagebox.showinfo(title="Alert", message="Todos os campos devem ser preenchidos.")
            return
        
        try:
            cpf_format = self.format_cpf(cpf)
            salario_format = self.format_salary(salario)

            doc_ref = self.db.collection("Colaboradores").document(cpf)
            doc_ref.set({
                'Nome': nome,
                'Cpf': cpf_format,
                'Setor': setor,
                'Salario': salario_format,
                'Cargo': cargo
            })

            messagebox.showinfo(title="Alert", message=f"Colaborador {nome} cadastrado com sucesso!")
        except ValueError as e:
            messagebox.showinfo(title="Alert", message=str(e))
