from db import initdb
from aluno import Aluno
from alunoservice import AlunoService
from tkinter import *
from disciplina import Disciplina
from disciplinaservice import DisciplinaService
from nota import Nota
from notaservice import NotaService
import requests 
import tkinter as tk
from tkinter import ttk, messagebox


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cadastro Acadêmico (Versão Original)")
        self.root.geometry("700x550")

        # Tenta inicializar o banco de dados
        try:
            initdb()
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível inicializar o banco: {e}")
            root.destroy()
            return

        # Instância dos serviços
        self.aluno_service = AlunoService()
        self.disciplina_service = DisciplinaService()
        self.nota_service = NotaService()

        # Estrutura de Abas (Notebook)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.tab_alunos = ttk.Frame(self.notebook)
        self.tab_disciplinas = ttk.Frame(self.notebook)
        self.tab_notas = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_alunos, text='Alunos')
        self.notebook.add(self.tab_disciplinas, text='Disciplinas')
        self.notebook.add(self.tab_notas, text='Notas')

        # Populando cada aba
        self.criar_tab_alunos(self.tab_alunos)
        self.criar_tab_disciplinas(self.tab_disciplinas)
        self.criar_tab_notas(self.tab_notas)
        
        # Atualiza dados ao iniciar
        self.atualizar_lista_alunos()
        self.atualizar_lista_disciplinas()
        self.atualizar_lista_notas()


    # --- ABA ALUNOS (Sem alterações) ---
    def criar_tab_alunos(self, tab):
        frame_form = ttk.Frame(tab, padding="10")
        frame_form.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_form, text="Matrícula:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.aluno_entry_matricula = ttk.Entry(frame_form, width=40)
        self.aluno_entry_matricula.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Label(frame_form, text="Nome:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.aluno_entry_nome = ttk.Entry(frame_form, width=40)
        self.aluno_entry_nome.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Label(frame_form, text="Dt. Nasc.:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.aluno_entry_nascimento = ttk.Entry(frame_form, width=40)
        self.aluno_entry_nascimento.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

        frame_botoes = ttk.Frame(tab, padding="10")
        frame_botoes.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(frame_botoes, text="Salvar", command=self.salvar_aluno).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Editar", command=self.editar_aluno).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Excluir", command=self.excluir_aluno).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Limpar", command=self.limpar_campos_aluno).pack(side='left', padx=5)

        frame_lista = ttk.Frame(tab, padding="10")
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)

        colunas = ('matricula', 'nome', 'dt_nascimento')
        self.tree_alunos = ttk.Treeview(frame_lista, columns=colunas, show='headings')
        self.tree_alunos.heading('matricula', text='Matrícula')
        self.tree_alunos.heading('nome', text='Nome')
        self.tree_alunos.heading('dt_nascimento', text='Dt. Nascimento')
        
        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_alunos.yview)
        self.tree_alunos.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree_alunos.pack(side='left', fill='both', expand=True)

        self.tree_alunos.bind('<<TreeviewSelect>>', self.on_aluno_select)

    def atualizar_lista_alunos(self):
        try:
            for i in self.tree_alunos.get_children():
                self.tree_alunos.delete(i)
            alunos = self.aluno_service.listar_aluno()
            for aluno in alunos:
                self.tree_alunos.insert('', 'end', values=(aluno.matricula, aluno.nome, aluno.dt_nascimento))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar alunos: {e}")

    def limpar_campos_aluno(self):
        self.aluno_entry_matricula.config(state='normal')
        self.aluno_entry_matricula.delete(0, 'end')
        self.aluno_entry_nome.delete(0, 'end')
        self.aluno_entry_nascimento.delete(0, 'end')
        if self.tree_alunos.selection():
            self.tree_alunos.selection_remove(self.tree_alunos.selection())
    
    def on_aluno_select(self, event):
        selected_item = self.tree_alunos.selection()
        if not selected_item: return
        values = self.tree_alunos.item(selected_item, 'values')
        
        self.limpar_campos_aluno()
        self.aluno_entry_matricula.insert(0, values[0])
        self.aluno_entry_matricula.config(state='readonly')
        self.aluno_entry_nome.insert(0, values[1])
        self.aluno_entry_nascimento.insert(0, values[2])

    def salvar_aluno(self):
        try:
            aluno = Aluno(
                self.aluno_entry_matricula.get(), 
                self.aluno_entry_nome.get(), 
                self.aluno_entry_nascimento.get()
            )
            if not aluno.matricula or not aluno.nome:
                messagebox.showwarning("Atenção", "Matrícula e Nome são obrigatórios.")
                return
            self.aluno_service.salvar(aluno)
            messagebox.showinfo("Sucesso", "Aluno salvo!")
            self.atualizar_lista_alunos()
            self.limpar_campos_aluno()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar: {e}")
    
    def editar_aluno(self):
        try:
            matricula = self.aluno_entry_matricula.get()
            if not matricula:
                messagebox.showwarning("Atenção", "Selecione um aluno da lista.")
                return
            
            aluno = Aluno(matricula, self.aluno_entry_nome.get(), self.aluno_entry_nascimento.get())
            self.aluno_service.editar(aluno)
            messagebox.showinfo("Sucesso", "Aluno editado!")
            self.atualizar_lista_alunos()
            self.limpar_campos_aluno()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível editar: {e}")

    def excluir_aluno(self):
        try:
            matricula = self.aluno_entry_matricula.get()
            if not matricula:
                messagebox.showwarning("Atenção", "Selecione um aluno da lista.")
                return
            
            if messagebox.askyesno("Confirmar", f"Excluir aluno {matricula}?"):
                self.aluno_service.excluir(matricula)
                messagebox.showinfo("Sucesso", "Aluno excluído!")
                self.atualizar_lista_alunos()
                self.limpar_campos_aluno()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível excluir: {e}")

    # --- ABA DISCIPLINAS (Sem alterações) ---
    def criar_tab_disciplinas(self, tab):
        frame_form = ttk.Frame(tab, padding="10")
        frame_form.pack(fill='x', padx=10, pady=5)
        
        self.disciplina_entry_id = ttk.Entry(frame_form) 
        
        ttk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.disciplina_entry_nome = ttk.Entry(frame_form, width=40)
        self.disciplina_entry_nome.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Label(frame_form, text="Turno:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.disciplina_entry_turno = ttk.Entry(frame_form, width=40)
        self.disciplina_entry_turno.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Label(frame_form, text="Sala:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.disciplina_entry_sala = ttk.Entry(frame_form, width=40)
        self.disciplina_entry_sala.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Label(frame_form, text="Professor:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.disciplina_entry_professor = ttk.Entry(frame_form, width=40)
        self.disciplina_entry_professor.grid(row=3, column=1, sticky='ew', padx=5, pady=5)

        frame_botoes = ttk.Frame(tab, padding="10")
        frame_botoes.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(frame_botoes, text="Salvar", command=self.salvar_disciplina).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Editar", command=self.editar_disciplina).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Excluir", command=self.excluir_disciplina).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Limpar", command=self.limpar_campos_disciplina).pack(side='left', padx=5)

        frame_lista = ttk.Frame(tab, padding="10")
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)

        colunas = ('id', 'nome', 'turno', 'sala', 'professor')
        self.tree_disciplinas = ttk.Treeview(frame_lista, columns=colunas, show='headings')
        self.tree_disciplinas.heading('id', text='ID')
        self.tree_disciplinas.heading('nome', text='Nome')
        self.tree_disciplinas.heading('turno', text='Turno')
        self.tree_disciplinas.heading('sala', text='Sala')
        self.tree_disciplinas.heading('professor', text='Professor')
        
        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_disciplinas.yview)
        self.tree_disciplinas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree_disciplinas.pack(side='left', fill='both', expand=True)

        self.tree_disciplinas.bind('<<TreeviewSelect>>', self.on_disciplina_select)

    def atualizar_lista_disciplinas(self):
        try:
            for i in self.tree_disciplinas.get_children():
                self.tree_disciplinas.delete(i)
            disciplinas = self.disciplina_service.listar_disciplina()
            for d in disciplinas:
                self.tree_disciplinas.insert('', 'end', values=(d.id, d.nome, d.turno, d.sala, d.professor))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar disciplinas: {e}")

    def limpar_campos_disciplina(self):
        self.disciplina_entry_id.delete(0, 'end')
        self.disciplina_entry_nome.delete(0, 'end')
        self.disciplina_entry_turno.delete(0, 'end')
        self.disciplina_entry_sala.delete(0, 'end')
        self.disciplina_entry_professor.delete(0, 'end')
        if self.tree_disciplinas.selection():
            self.tree_disciplinas.selection_remove(self.tree_disciplinas.selection())
    
    def on_disciplina_select(self, event):
        selected_item = self.tree_disciplinas.selection()
        if not selected_item: return
        values = self.tree_disciplinas.item(selected_item, 'values')
        
        self.limpar_campos_disciplina()
        self.disciplina_entry_id.insert(0, values[0]) # ID
        self.disciplina_entry_nome.insert(0, values[1])
        self.disciplina_entry_turno.insert(0, values[2])
        self.disciplina_entry_sala.insert(0, values[3])
        self.disciplina_entry_professor.insert(0, values[4])

    def salvar_disciplina(self):
        try:
            disciplina = Disciplina(
                None, # ID é autoincrement
                self.disciplina_entry_nome.get(),
                self.disciplina_entry_turno.get(),
                self.disciplina_entry_sala.get(),
                self.disciplina_entry_professor.get()
            )
            if not disciplina.nome or not disciplina.turno:
                messagebox.showwarning("Atenção", "Nome e Turno são obrigatórios.")
                return
            self.disciplina_service.salvar(disciplina)
            messagebox.showinfo("Sucesso", "Disciplina salva!")
            self.atualizar_lista_disciplinas()
            self.limpar_campos_disciplina()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar: {e}")
    
    def editar_disciplina(self):
        try:
            id = self.disciplina_entry_id.get()
            if not id:
                messagebox.showwarning("Atenção", "Selecione uma disciplina da lista.")
                return
            
            disciplina = Disciplina(
                id,
                self.disciplina_entry_nome.get(),
                self.disciplina_entry_turno.get(),
                self.disciplina_entry_sala.get(),
                self.disciplina_entry_professor.get()
            )
            self.disciplina_service.editar(disciplina)
            messagebox.showinfo("Sucesso", "Disciplina editada!")
            self.atualizar_lista_disciplinas()
            self.limpar_campos_disciplina()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível editar: {e}")

    def excluir_disciplina(self):
        try:
            id = self.disciplina_entry_id.get()
            if not id:
                messagebox.showwarning("Atenção", "Selecione uma disciplina da lista.")
                return
            
            if messagebox.askyesno("Confirmar", f"Excluir disciplina {id}?"):
                self.disciplina_service.excluir(id)
                messagebox.showinfo("Sucesso", "Disciplina excluída!")
                self.atualizar_lista_disciplinas()
                self.limpar_campos_disciplina()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível excluir: {e}")

    # --- ABA NOTAS (Modificada para usar seu Service original) ---
    def criar_tab_notas(self, tab):
        frame_form = ttk.Frame(tab, padding="10")
        frame_form.pack(fill='x', padx=10, pady=5)
        
        # Campos de entrada de texto para os IDs
        ttk.Label(frame_form, text="Matrícula Aluno:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.nota_entry_matricula = ttk.Entry(frame_form, width=40)
        self.nota_entry_matricula.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Label(frame_form, text="ID Disciplina:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.nota_entry_disciplina_id = ttk.Entry(frame_form, width=40)
        self.nota_entry_disciplina_id.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

        ttk.Label(frame_form, text="Valor:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.nota_entry_valor = ttk.Entry(frame_form, width=40)
        self.nota_entry_valor.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

        frame_botoes = ttk.Frame(tab, padding="10")
        frame_botoes.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(frame_botoes, text="Salvar", command=self.salvar_nota).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Editar", command=self.editar_nota).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Excluir", command=self.excluir_nota).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Limpar", command=self.limpar_campos_nota).pack(side='left', padx=5)

        frame_lista = ttk.Frame(tab, padding="10")
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)

        # Colunas agora mostram os IDs, como na sua classe Nota
        colunas = ('valor', 'matricula', 'disciplina_id')
        self.tree_notas = ttk.Treeview(frame_lista, columns=colunas, show='headings')
        self.tree_notas.heading('valor', text='Nota (Valor)')
        self.tree_notas.heading('matricula', text='Matrícula Aluno')
        self.tree_notas.heading('disciplina_id', text='ID Disciplina')
        
        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_notas.yview)
        self.tree_notas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree_notas.pack(side='left', fill='both', expand=True)

        self.tree_notas.bind('<<TreeviewSelect>>', self.on_nota_select)

    def atualizar_lista_notas(self):
        try:
            for i in self.tree_notas.get_children():
                self.tree_notas.delete(i)
            
            # Chama sua função original: nota_service.listar_disciplina()
            notas = self.nota_service.listar_disciplina() 
            
            for nota in notas:
                self.tree_notas.insert('', 'end', values=(nota.valor, nota.matricula, nota.disciplina_id))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar notas: {e}")

    def limpar_campos_nota(self):
        # Habilita campos (caso 'on_select' os tenha desabilitado)
        self.nota_entry_matricula.config(state='normal')
        self.nota_entry_disciplina_id.config(state='normal')

        self.nota_entry_matricula.delete(0, 'end')
        self.nota_entry_disciplina_id.delete(0, 'end')
        self.nota_entry_valor.delete(0, 'end')
        
        if self.tree_notas.selection():
            self.tree_notas.selection_remove(self.tree_notas.selection())

    def on_nota_select(self, event):
        selected_item = self.tree_notas.selection()
        if not selected_item: return
        
        # values = (valor, matricula, disciplina_id)
        values = self.tree_notas.item(selected_item, 'values')
        
        self.limpar_campos_nota()
        
        # Preenche os campos de entrada
        self.nota_entry_valor.insert(0, values[0])
        self.nota_entry_matricula.insert(0, values[1])
        self.nota_entry_disciplina_id.insert(0, values[2])

        # Desabilita os campos de chave primária (para evitar erros na edição)
        self.nota_entry_matricula.config(state='readonly')
        self.nota_entry_disciplina_id.config(state='readonly')


    def salvar_nota(self):
        try:
            nota = Nota(
                self.nota_entry_valor.get(),
                self.nota_entry_matricula.get(),
                self.nota_entry_disciplina_id.get()
            )
            if not nota.valor or not nota.matricula or not nota.disciplina_id:
                messagebox.showwarning("Atenção", "Todos os campos são obrigatórios.")
                return
            
            self.nota_service.salvar(nota)
            messagebox.showinfo("Sucesso", "Nota salva!")
            self.atualizar_lista_notas()
            self.limpar_campos_nota()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar a nota: {e}")
    
    def editar_nota(self):
        try:
            # Pega os dados dos campos
            valor = self.nota_entry_valor.get()
            matricula = self.nota_entry_matricula.get()
            disciplina_id = self.nota_entry_disciplina_id.get()
            
            if not valor or not matricula or not disciplina_id:
                messagebox.showwarning("Atenção", "Selecione uma nota da lista para editar.")
                return

            nota = Nota(valor, matricula, disciplina_id)
            
            # Chama a sua função de editar original
            self.nota_service.editar(nota)
            messagebox.showinfo("Sucesso", "Nota editada!")
            self.atualizar_lista_notas()
            self.limpar_campos_nota()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível editar a nota: {e}")

    def excluir_nota(self):
        try:
            # Pega os dados dos campos (que foram preenchidos pelo 'on_select')
            matricula = self.nota_entry_matricula.get()
            disciplina_id = self.nota_entry_disciplina_id.get()
            
            if not matricula or not disciplina_id:
                messagebox.showwarning("Atenção", "Selecione uma nota da lista para excluir.")
                return

            # Cria o objeto Nota, como sua função 'excluir' espera
            # O valor da nota não importa para a exclusão, apenas as chaves
            nota_para_excluir = Nota(None, matricula, disciplina_id)
            
            if messagebox.askyesno("Confirmar", f"Excluir nota (Matrícula {matricula}, Disciplina {disciplina_id})?"):
                # Chama a sua função de excluir original
                self.nota_service.excluir(nota_para_excluir)
                messagebox.showinfo("Sucesso", "Nota excluída!")
                self.atualizar_lista_notas()
                self.limpar_campos_nota()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível excluir a nota: {e}")


# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    # Garante que os imports estão corretos (causa dos erros anteriores)
    try:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
    except NameError as e:
        print(f"ERRO DE IMPORTAÇÃO: {e}")
        print("Verifique se você tem 'import tkinter as tk' e 'from tkinter import ttk, messagebox' no topo do arquivo.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")