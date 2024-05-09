from cryptography.fernet import Fernet #Biblioteca de criptografia.
import tkinter as tk #Biblioteca de Interface Gráfica.
from tkinter import filedialog, messagebox
import pyperclip

def selecionar_arquivo():
    global label_arquivo
    arquivo = filedialog.askopenfilename(initialdir='/', title="Selecione o arquivo", filetypes=(('Arquivos de texto', '*.txt'), ('Todos os arquivos', '*.*')))
    if arquivo:
        try:
            label_arquivo.config(text='Arquivo selecionado: ' + arquivo)
            with open(arquivo, 'rb') as file:
                conteudo = file.read()
                chave = Fernet.generate_key()
                criptografia = Fernet(chave)
                conteudo_criptografado = criptografia.encrypt(conteudo)
                nome_arquivo_criptografado = arquivo + '.encrypted'
                with open(nome_arquivo_criptografado, 'wb') as file_criptografado:
                    file_criptografado.write(conteudo_criptografado)
            chave_label.config(text='Chave: ' + chave.decode())
            copiar_chave_button = tk.Button(janela, text='Copiar Chave', command=lambda chave=chave: copiar_chave(chave))
            copiar_chave_button.pack()
            messagebox.showinfo('Criptografia Concluída!', 'Arquivo criptografado com sucesso. \nChave: {}'.format(chave.decode()))
        except Exception as e:
            messagebox.showerror('Erro', str(e))

def copiar_chave(chave):
    chave_str = chave.decode() #Convertendo bytes para strings
    pyperclip.copy(chave_str)
    messagebox.showinfo('Chave Copiada!', 'Chave Copiada para area de transfencia.')

def descriptografar_arquivo():
    arquivo = filedialog.askopenfilename(initialdir='/', title='Selecione o arquivo', filetypes=(('Arquivos criptografados', '*.encrypted'), ('Todos os arquivos', '*.*')))
    if arquivo:
        try:
            chave = chave_descriptografar.get()
            criptografia = Fernet(chave.encode())
            with open(arquivo, 'rb') as file_criptografado:
                conteudo_criptografado = file_criptografado.read()
                conteudo_descriptografado = criptografia.decrypt(conteudo_criptografado)
                nome_arquivo_descriptografado = arquivo[:-10] #Remover a extensão ".encrypted"
                with open(nome_arquivo_descriptografado, 'wb') as file_descriptografado:
                    file_descriptografado.write(conteudo_descriptografado)
            messagebox.showinfo('Descriptografia Concluída!', 'Arquivo descriptografado com sucesso.')
        except Exception as e:
            messagebox.showerror('Erro', str(e))


# Cria a janela principal
janela = tk.Tk()
janela.title('Criptografia')

# Cria um texto (label) sobre oque o botão faz.
instrucao = tk.Label(janela, text='Clique no botão abaixo para selecionar um arquivo.')
instrucao.pack(pady=10)

# Cria um botão e chama a função selecionar_arquivo.
botao_selecionar = tk.Button(janela, text='Selecionar Arquivo', command=selecionar_arquivo)
botao_selecionar.pack(pady=5)

label_arquivo = tk.Label(janela, text='')
label_arquivo.pack(pady=10)

# Cria um botão para descriptografar o arquivo
botao_descriptografar = tk.Button(janela, text='Descriptografar Arquivo', command=descriptografar_arquivo)
botao_descriptografar.pack(pady=5)

# Campo para inserir a chave de descriptografia
label_chave = tk.Label(janela, text='Insira a chave de descriptografia: ')
label_chave.pack(pady=5)
chave_descriptografar = tk.Entry(janela, show='*')
chave_descriptografar.pack(pady=5)

# Campo para exibir a chave gerada
chave_label = tk.Label(janela, text='Chave: ')
chave_label.pack(pady=5)

janela.geometry('700x300') #Definir tamanho da janela.

janela.mainloop() #Inicia o loop principal da aplicação.
