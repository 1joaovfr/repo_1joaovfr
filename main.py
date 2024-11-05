import customtkinter as ctk
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('C:/programs/customtkinter/config/pytkinter.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

window = Tk()

class App():
    def  __init__(self, db):
        self.db = db
        self.window = window
        self.window_config()
        self.window_login()
        self.register_frame = None
        self.list_frame = None
        window.mainloop()

    def login_verify(self):
        try:
            email = self.email_entry.get()
            senha = self.password_entry.get()
            self.users_ref = self.db.collection('Usuarios')
            user_doc = self.users_ref.document(email).get()

            if user_doc.exists:
                self.user_data = user_doc.to_dict()
                email_db = self.user_data.get('Email')
                password_db = self.user_data.get('Senha')

                if email_db == email and password_db == senha: 
                    messagebox.showinfo(title="Alert", message="Login feito com sucesso.")
                    self.email_entry.delete(0, ctk.END)
                    self.password_entry.delete(0, ctk.END)

                    for widget in window.winfo_children():
                        widget.destroy()
                    self.window_home()

                else:
                    messagebox.showerror("Erro", "E-mail ou Senha incorreta")
            else:
                messagebox.showerror("Erro", "Usuário não encontrado")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    
    def register_verify(self):
        nome = self.name_entry.get()
        cpf = self.cpf_entry.get()
        setor = self.setor_entry.get()
        salario = self.salary_entry.get()
        cargo = self.option_menu.get()

        if not all([nome, cpf, setor, salario, cargo]): # Verifica se todos os campos foram preenchidos
            messagebox.showinfo(title='Alert', message="Todos os campos devem ser preenchidos.")
        else:
            try:
                cpf = ''.join(filter(str.isdigit, cpf)) # Remove caracteres não numéricos

                if len(cpf) == 11:  # Verifica se o CPF tem 11 dígitos
                    cpf_format = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}' # Formata o CPF
                else:
                    messagebox.showinfo(title='Alert', message="O CPF deve conter 11 digitos.")

                salario_float = float(salario)
                salario_format = f'R${salario_float:,.2f}'
            except ValueError:
                messagebox.showinfo(title='Alert', message="O salário deve ser um número válido.")
                return
            
            doc_ref = self.db.collection('Colaboradores').document(cpf)
            doc_ref.set({
                'Nome': nome,
                'Cpf': cpf_format,
                'Setor': setor,
                'Salario': salario_format,
                'Cargo': cargo
            })

            messagebox.showinfo(title="Alert", message=f"Colaborador {nome} cadastrado com sucesso!")

            self.name_entry.delete(0, ctk.END)
            self.cpf_entry.delete(0, ctk.END)
            self.setor_entry.delete(0, ctk.END)
            self.salary_entry.delete(0, ctk.END)
            self.option_menu.set(self.options[0])

    """def update_verify(self):
        cpf = self.cpf_entry.get()

        user_doc = self.db.collection('Colaboradores').document(cpf).get()

        if user_doc.exists:
            salario = self.salary_entry.get()

            try:
                # Tenta converter o salário para float
                salario_float = float(salario)
                salario_format = f'R${salario_float:,.2f}'
            except ValueError:
                print("O salário deve ser um número válido.")
                return

            doc_ref = self.db.collection('Colaboradores').document(cpf)
            doc_ref.update({
                'Salario': salario_format,
            })
            
            messagebox.showinfo(title="Sucesso", message="Dados atualizados com sucesso.")
        else:
            messagebox.showinfo(title="Erro", message="Colaborador não encontrado.")"""

    def filter_search(self, event):
        filtro = self.search_entry.get()

        for row in self.table.get_children():
            self.table.delete(row)

        if filtro:
            query = self.users_ref.where('Nome', '>=', filtro).where('Nome', '<=', filtro + '\uf8ff')
        else:
            # Se não houver filtro, busca todos os documentos
            query = self.users_ref

        docs = query.stream()
        
        # Atualizar a tabela com os resultados filtrados
        for doc in docs:
            dados = doc.to_dict()
            self.table.insert('', 'end', values=(dados['Nome'], dados['Cpf'], dados['Setor'], dados['Cargo'], dados['Salario']))

    def dismiss_verify(self):
        # Obter o item selecionado
        selected_item = self.table.selection()

        if selected_item:
            # Obtendo o primeiro item selecionado (se houver múltiplos, você pode ajustar conforme necessário)
            item = selected_item[0]
            
            # Para pegar os dados do item, você precisa recuperar as informações que você precisa para deletar do Firebase
            nome = self.table.item(item)['values'][0]  # Supondo que o nome está na primeira coluna

            # Agora, você deve buscar o documento correspondente no Firebase
            docs = self.users_ref.where('Nome', '==', nome).limit(1).stream()

            for doc in docs:
                # Deletar o documento do Firebase
                self.users_ref.document(doc.id).delete()  # Remove o documento pelo ID

            # Remover a linha da tabela
            self.table.delete(item)  # Remove a linha selecionada

            messagebox.showinfo(title="Alert", message="Usuário demitido!")

    def logout_verify(self, event):
        for widget in window.winfo_children():
            widget.destroy()
        self.window_login()

    def logout_btn_hover(self, event):
        event.widget.configure(cursor="hand2")

    def logout_btn_leave(self, event):
        event.widget.configure(cursor="")

    def login_btn_hover(self, event):
        self.login_button.configure(fg_color="white", text_color="#19649D")

    def login_btn_leave(self, event):
        self.login_button.configure(fg_color="#19649D", text_color="white")

    def register_btn_hover(self, event):
        self.register_button.configure(fg_color="white", text_color="#2F9D19") 

    def register_btn_leave(self, event):
        self.register_button.configure(fg_color="#2F9D19", text_color="white")

    def update_btn_hover(self, event):
        self.update_button.configure(fg_color="white", text_color="#00C6DC")

    def  update_btn_leave(self, event):
        self.update_button.configure(fg_color="#00C6DC", text_color="white")

    def search_hover(self, event):
        event.widget.configure(cursor="hand2")

    def search_leave(self, event):
        event.widget.configure(cursor="")

    def notify_btn_hover(self, event):
        self.notify_button.configure(fg_color="white", text_color="#FF9500")

    def notify_btn_leave(self, event):
        self.notify_button.configure(fg_color="#FF9500", text_color="white")

    def dismiss_btn_hover(self, event):
        self.dismiss_button.configure(fg_color="white", text_color="#9D1919")

    def dismiss_btn_leave(self, event):
        self.dismiss_button.configure(fg_color="#9D1919", text_color="white")

    def officer_list(self):
        self.table = ttk.Treeview(
            master=self.list_frame,
            columns=('name', 'cpf', 'setor', 'possition', 'salary'), 
            show='headings', 
            style="Custom.Treeview"
        )

        self.table.heading('name', text='Nome', anchor='w')
        self.table.heading('cpf', text='CPF', anchor='w')
        self.table.heading('setor', text='Setor', anchor='w')
        self.table.heading('possition', text='Cargo', anchor='w')
        self.table.heading('salary', text='Salário', anchor='w')

        self.table.column('name', width=200, anchor='w')
        self.table.column('cpf', width=80, anchor='w')
        self.table.column('setor', width=70, anchor='w')
        self.table.column('possition', width=60, anchor='w')
        self.table.column('salary', width=50, anchor='w')

        self.users_ref = db.collection('Colaboradores')
        docs = self.users_ref.stream()

        for doc in docs:
            dados = doc.to_dict()
            self.table.insert('', 'end', values=(dados['Nome'], dados['Cpf'], dados['Setor'], dados['Cargo'], dados['Salario']))
        
        self.table.place(x=5, y=5, width=770, height=540)

        style = ttk.Style()
        style.theme_use('clam')

        style.configure(
            "Custom.Treeview",
            bordercolor="white",
            borderwidth=0,
            background="white",
            foreground="#19649D",
            font=('Istok Web', 13),
            rowheight=25,
        )

        style.configure(
            "Custom.Treeview.Heading",
            background="white",
            foreground="#19649D",
            borderwidth=0,
            font=('Istok Web', 14, 'bold'),
        )

        style.map(
            "Custom.Treeview.Heading",
            background=[('active', 'white'), ('pressed', 'white'), ('!active', 'white')],
            foreground=[('active', '#19649D'), ('pressed', '#19649D'), ('!active', '#19649D')]
        )

        style.map("Custom.Treeview", background=[('!selected', 'white'), ('selected', '#A3C1D8')])

    def open_register_frame(self):
        if self.list_frame:
            self.list_frame.destroy()
            self.search_entry.destroy()
            self.notify_button.destroy()
            self.dismiss_button.destroy()
            self.search_img.destroy()

        self.register_frame_button = ctk.CTkButton(
            master=window,
            width=300,
            height=50,
            fg_color="#19649D",
            bg_color="#19649D",
            font=("Istok Web", 16, 'bold'),
            text="Cadastrar Colaboradores" + " " * 12,
            text_color="white",
            border_width=2,
            border_color="#A3C1D8",
            command=self.open_register_frame
        )
        self.register_frame_button.place(x=0, y=175)

        self.list_frame_button = ctk.CTkButton(
            master=window,
            width=300,
            height=50,
            fg_color="#19649D",
            bg_color="#19649D",
            font=("Istok Web", 16, 'bold'),
            text="Listar Colaboradores" + " " * 20,
            text_color="white",
            border_width=0,
            border_color="#19649D",
            command=self.open_list_frame
        )
        self.list_frame_button.place(x=0, y=240)

        self.register_label = ctk.CTkLabel(
            master=window,
            text="Preencha os campos abaixo para cadastrar um colaborador.",
            font=("Istok Web", 20, 'bold'),
            text_color="#19649D",
            fg_color="white",
            bg_color="white",
        )
        self.register_label.place(x=360, y=86)

        self.register_frame = ctk.CTkFrame(
            master=window, 
            width=780, 
            height=550,
            border_color="#19649D",
            border_width=2,
            corner_radius=5,
            bg_color="white",
            fg_color="white"
        )
        self.register_frame.place(x=360, y=115)

        name_label = ctk.CTkLabel(
            master=self.register_frame, 
            text="Nome",  
            font=("Istok Web", 16), 
            bg_color='white', 
            text_color="#19649D"
        )
        name_label.place(x=50, y=45)

        self.name_entry = ctk.CTkEntry(
            master=self.register_frame, 
            width=300, 
            height=40 , 
            font=("Istok Web", 16), 
            placeholder_text="Digite o nome do colaborador", 
            placeholder_text_color="#A3C1D8", 
            fg_color="white", 
            bg_color="white",
            border_color="#19649D",
            text_color="#19649D"
        )
        self.name_entry.place(x=50, y=74)

        cpf_label = ctk.CTkLabel(
            master=self.register_frame, 
            text="CPF",  
            font=("Istok Web", 16), 
            bg_color='white', 
            text_color="#19649D"
        )
        cpf_label.place(x=50, y=173)

        self.cpf_entry = ctk.CTkEntry(
            master=self.register_frame, 
            width=300, 
            height=40 , 
            font=("Istok Web", 16), 
            placeholder_text="Digite o CPF do colaborador", 
            placeholder_text_color="#A3C1D8", 
            fg_color="white", 
            bg_color="white",
            border_color="#19649D",
            text_color="#19649D"
        )
        self.cpf_entry.place(x=50, y=202)

        setor_label = ctk.CTkLabel(
            master=self.register_frame, 
            text="Setor",  
            font=("Istok Web", 16), 
            bg_color='white', 
            text_color="#19649D"
        )
        setor_label.place(x=50, y=296)

        self.setor_entry = ctk.CTkEntry(
            master=self.register_frame, 
            width=300, 
            height=40 , 
            font=("Istok Web", 16), 
            placeholder_text="Digite o setor do colaborador", 
            placeholder_text_color="#A3C1D8", 
            fg_color="white", 
            bg_color="white",
            border_color="#19649D",
            text_color="#19649D"
        )
        self.setor_entry.place(x=50, y=325)

        cep_label = ctk.CTkLabel(
            master=self.register_frame, 
            text="CEP",  
            font=("Istok Web", 16), 
            bg_color='white', 
            text_color="#19649D"
        )
        cep_label.place(x=50, y=419)

        self.cep_entry = ctk.CTkEntry(
            master=self.register_frame, 
            width=300, 
            height=40 , 
            font=("Istok Web", 16), 
            placeholder_text="Digite o CEP do colaborador", 
            placeholder_text_color="#A3C1D8", 
            fg_color="white", 
            bg_color="white",
            border_color="#19649D",
            text_color="#19649D"
        )
        self.cep_entry.place(x=50, y=448)

        position_label = ctk.CTkLabel(
            master=self.register_frame, 
            text="Cargo",  
            font=("Istok Web", 16), 
            bg_color='white', 
            text_color="#19649D"
        )
        position_label.place(x=430, y=45)

        option_menu_border = ctk.CTkFrame(
            master=self.register_frame,
            width=302,
            height=40,
            border_width=2,
            border_color="#19649D",
        )
        option_menu_border.place(x=428, y=74)

        self.options = ["Funcionario", "Gerente", "Diretor"]

        self.option_menu = ctk.CTkOptionMenu(
            master=self.register_frame, 
            values=self.options, 
            width=298, 
            height=36, 
            font=("Istok Web", 16), 
            dropdown_font=("Istok Web", 14),
            fg_color="white",  # Cor de fundo da área de texto
            bg_color="#19649D",
            button_color="white",  # Cor do botão da seta
            button_hover_color="white",  # Cor ao passar o mouse na seta
            dropdown_hover_color="#A3C1D8",  # Cor ao passar o mouse nas opções
            text_color="#19649D",
        )
        self.option_menu.place(x=430, y=76)
        self.option_menu.set(self.options[0])

        salary_label = ctk.CTkLabel(
            master=self.register_frame, 
            text="Salario",  
            font=("Istok Web", 16), 
            bg_color='white',
            text_color="#19649D"
        )
        salary_label.place(x=430, y=173)

        self.salary_entry = ctk.CTkEntry(
            master=self.register_frame, 
            width=300, 
            height=40 , 
            font=("Istok Web", 16), 
            placeholder_text="Digite o salario do colaborador", 
            placeholder_text_color="#A3C1D8", 
            fg_color="white", 
            bg_color="white",
            border_color="#19649D",
            text_color="#19649D"
        )
        self.salary_entry.place(x=430, y=202)

        self.check_admin = ctk.CTkCheckBox(
            master=self.register_frame,
            text="Colaborador Admin.",
            text_color="#19649D",
            border_color="#19649D"
        )
        self.check_admin.place(x=430, y=330)

        self.register_button = ctk.CTkButton(
            master=self.register_frame,  
            text="Cadastrar",
            text_color="white",
            width=300,
            height=30,
            fg_color="#2F9D19",
            border_width=2,
            border_color="#2F9D19",
            command=self.register_verify
        )
        self.register_button.place(x=430, y=453)
        self.register_button.bind("<Enter>", self.register_btn_hover)
        self.register_button.bind("<Leave>", self.register_btn_leave)

        """ self.update_button = ctk.CTkButton(
            master=self.register_frame,  
            text="Atualizar",
            text_color="white",
            width=125,
            height=30,
            fg_color="#00C6DC",
            border_width=2,
            border_color="#00C6DC",
            command=self.update_verify
        )
        self.update_button.place(x=605, y=453)
        self.update_button.bind("<Enter>", self.update_btn_hover)
        self.update_button.bind("<Leave>", self.update_btn_leave) """
        
    def open_list_frame(self):
        if self.register_frame:
            self.register_frame.destroy()
            self.register_label.destroy()

        self.register_frame_button = ctk.CTkButton(
            master=window,
            width=300,
            height=50,
            fg_color="#19649D",
            bg_color="#19649D",
            font=("Istok Web", 16, 'bold'),
            text="Cadastrar Colaboradores" + " " * 12,
            text_color="white",
            border_width=0,
            border_color="#19649D",
            command=self.open_register_frame
        )
        self.register_frame_button.place(x=0, y=175)

        self.list_frame_button = ctk.CTkButton(
            master=window,
            width=300,
            height=50,
            fg_color="#19649D",
            bg_color="#19649D",
            font=("Istok Web", 16, 'bold'),
            text="Listar Colaboradores" + " " * 20,
            text_color="white",
            border_width=2,
            border_color="#A3C1D8",
            command=self.open_list_frame
        )
        self.list_frame_button.place(x=0, y=240)

        self.list_frame = ctk.CTkFrame(
            master=window, 
            width=780, 
            height=550,
            border_color="#19649D",
            border_width=2, 
            corner_radius=5,
            bg_color="white",
            fg_color="white"
        )
        self.list_frame.place(x=360, y=115)

        self.search_entry = ctk.CTkEntry(
            master=self.window,
            width=339, 
            height=30, 
            font=("Istok Web", 16), 
            placeholder_text="Pesquise um colaborador", 
            placeholder_text_color="#A3C1D8", 
            fg_color="white", 
            bg_color="white",
            border_color="#19649D",
            text_color="#19649D"
        )
        self.search_entry.place(x=360, y=80)

        self.search_img = ctk.CTkImage(
            light_image=Image.open('C:/repo_1joaovfr/img/search.png'), 
            dark_image=Image.open('C:/repo_1joaovfr/img/search.png'), 
            size=(30, 30)
        )

        self.search_img = ctk.CTkLabel(
            master=window, 
            image=self.search_img,
            text=""
        )
        self.search_img.place(x=694, y=80)
        self.search_img.bind("<Button-1>", self.filter_search)
        self.search_img.bind("<Enter>", self.search_hover)
        self.search_img.bind("<Leave>", self.search_leave)

        self.notify_button = ctk.CTkButton(
            master=self.window,  
            text="Notificar",
            text_color="white",
            width=125,
            height=30,
            fg_color="#FF9500",
            bg_color="white",
            border_width=2,
            border_color="#FF9500",
        )
        self.notify_button.place(x=865, y=80)
        self.notify_button.bind("<Enter>", self.notify_btn_hover)
        self.notify_button.bind("<Leave>", self.notify_btn_leave)

        self.dismiss_button = ctk.CTkButton(
            master=self.window,  
            text="Demitir",
            text_color="white",
            width=125,
            height=30,
            fg_color="#9D1919",
            bg_color="white",
            border_width=2,
            border_color="#9D1919",
            command=self.dismiss_verify
        )
        self.dismiss_button.place(x=1015, y=80)
        self.dismiss_button.bind("<Enter>", self.dismiss_btn_hover)
        self.dismiss_button.bind("<Leave>", self.dismiss_btn_leave)

        self.officer_list()

    def window_config(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        window.geometry("1200x750")
        window.title("Sistema de administração")
        window.resizable(False, False)

    def window_login(self):
        img = ctk.CTkImage(
            light_image=Image.open('C:/repo_1joaovfr/img/bg1.png'), 
            dark_image=Image.open('C:/repo_1joaovfr/img/bg1.png'), 
            size=(1200, 750)
        )

        label_img = ctk.CTkLabel(
            master=window, 
            text="", 
            image=img
        )
        label_img.pack(anchor=CENTER)

        tt_label = ctk.CTkLabel(
            master=window,  
            text=f"Entre com sua", 
            font=("Istok Web", 32, "bold"), 
            bg_color='white', 
            text_color="#19649D"
        )
        tt_label.place(x=750, y=55)

        tt_label = ctk.CTkLabel(
            master=window,  
            text=f"conta", 
            font=("Istok Web", 32, "bold"), 
            bg_color='white', 
            text_color="#19649D"
        )
        tt_label.place(x=750, y=100)

        email_label = ctk.CTkLabel(
            master=window, 
            text="E-mail",  
            font=("Istok Web", 16), 
            bg_color='white', 
            text_color="#19649D"
        )
        email_label.place(x=750, y=217)

        self.email_entry = ctk.CTkEntry(
            master=window, 
            width=380, 
            height=40 , 
            font=("Istok Web", 16), 
            placeholder_text="exemplo@email.com", 
            placeholder_text_color="#A3C1D8", 
            fg_color="white", 
            bg_color="white",
            border_color="#19649D",
            text_color="#19649D"
        )
        self.email_entry.place(x=750, y=241)

        password_label = ctk.CTkLabel(
            master=window, 
            text="Senha",  
            font=("Istok Web", 16), 
            bg_color='white', 
            text_color="#19649D",
        )
        password_label.place(x=750, y=340)

        self.password_entry = ctk.CTkEntry(
            master=window, 
            width=380, 
            height=40 , 
            font=("Istok Web", 16), 
            placeholder_text="********", 
            placeholder_text_color="#A3C1D8", 
            fg_color="white", 
            bg_color="white",
            border_color="#19649D",
            text_color="#19649D",
            show="*"
        )
        self.password_entry.place(x=750, y=364)

        checkbox = ctk.CTkCheckBox(
            master=window, 
            text="Lembrar de mim.", 
            bg_color="white",
            border_color="#19649D",
            text_color="#19649D"
        )
        checkbox.place(x=750, y=459)

        self.login_button = ctk.CTkButton(
            master=window, 
            width=380, 
            height=30, 
            font=("Istok Web", 16), 
            fg_color="#19649D", 
            bg_color="white",
            border_width=2,
            border_color="#19649D",
            text="Entrar",
            text_color="white",
            command=self.login_verify
        )
        self.login_button.place(x=750, y=554)
        self.login_button.bind("<Enter>", self.login_btn_hover)
        self.login_button.bind("<Leave>", self.login_btn_leave)

    def window_home(self):
            img = ctk.CTkImage(
                light_image=Image.open('C:/repo_1joaovfr/img/bg2.png'), 
                dark_image=Image.open('C:/repo_1joaovfr/img/bg2.png'), 
                size=(1200, 750)
            )

            label_img = ctk.CTkLabel(
                master=window, 
                text="", 
                image=img
            )
            label_img.pack(anchor=CENTER)

            stt_label = ctk.CTkLabel(
                master=window, 
                text="Funções",
                text_color="#A3C1D8",
                font=("Istok Web", 15),
                bg_color="#19649D"
            )
            stt_label.place(x=30, y=99)

            self.register_frame_button = ctk.CTkButton(
                master=window,
                width=300,
                height=50,
                fg_color="#19649D",
                bg_color="#19649D",
                font=("Istok Web", 16, 'bold'),
                text="Cadastrar Colaboradores" + " " * 12,
                text_color="white",
                border_width=0,
                border_color="#19649D",
                command=self.open_register_frame
            )
            self.register_frame_button.place(x=0, y=175)

            self.list_frame_button = ctk.CTkButton(
                master=window,
                width=300,
                height=50,
                fg_color="#19649D",
                bg_color="#19649D",
                font=("Istok Web", 16, 'bold'),
                text="Listar Colaboradores" + " " * 20,
                text_color="white",
                border_width=0,
                border_color="#19649D",
                command=self.open_list_frame
            )
            self.list_frame_button.place(x=0, y=240)

            logout_img = ctk.CTkImage(
                light_image=Image.open('C:/repo_1joaovfr/img/logout.png'), 
                dark_image=Image.open('C:/repo_1joaovfr/img/logout.png'), 
                size=(30, 30)
            )

            logout_img = ctk.CTkLabel(
                master=window, 
                text="Log out" +  " " * 41,
                text_color="white",
                font=("Istok Web", 14, 'bold'),
                fg_color="#19649D",
                image=logout_img,
                compound="left",
                width=300,
                height=40
            )
            logout_img.place(x=0, y=690)

            logout_img.bind("<Button-1>", self.logout_verify )
            logout_img.bind("<Enter>", self.logout_btn_hover)
            logout_img.bind("<Leave>", self.logout_btn_leave)
            
            user_icon_img = ctk.CTkImage(
                light_image=Image.open('C:/repo_1joaovfr/img/user_icon.png'), 
                dark_image=Image.open('C:/repo_1joaovfr/img/user_icon.png'), 
                size=(30, 30)
            )

            user_icon_img = ctk.CTkLabel(
                master=window, 
                text="",
                bg_color="white",
                image=user_icon_img,
            )
            user_icon_img.place(x=1145, y=10)

            user = self.user_data['Nome']

            user_icon_label = ctk.CTkLabel(
                master=window,
                text=user,
                text_color="#19649D",
                font=("Istok Web", 14, 'bold'),
                bg_color='white'
            )
            user_icon_label.place(x=1145, y=25, anchor='e')

App(db)
