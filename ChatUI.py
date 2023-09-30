import tkinter as tk
from Chatbot import ChatbotLogic
from PIL import Image, ImageTk

class ChatbotUi:
    def __init__(self, chatbot_logic):
        #Chama a lógica do chatbot importada & cria a janela principal do tkinter
        self.chatbot_logic = chatbot_logic
        self.window = tk.Tk()
        self.window.title("Chatbot")

        # Parte em que as mensagens aparecem
        self.messageswindow = tk.Text(self.window, width=100, height=40, background="#EBEBEB", borderwidth=2, relief="solid")
        self.messageswindow.pack(pady=15)

        #Adicionando cor, bordas e fontes
        self.messageswindow.tag_configure("user_tag", foreground="black", justify="right", background="#c5c6d6",  font=("Poppins", 14))
        self.messageswindow.tag_configure("chatbot_tag", foreground="black", justify="left", background="#d5d5de",  font=("Poppins", 14))

        self.input_frame = tk.Frame(self.window)
        self.input_frame.pack()

        #Campo onde o usuário escreve a pergunta
        self.userEntry = tk.Entry(self.input_frame, width=60, foreground="black", justify="left", background="#c5c6d6",  font=("Poppins", 14))
        self.userEntry.grid(row=0, column=0) 

        #Espaço em branco entre a caixa de entrada e o botão
        tk.Label(self.input_frame, text=" ").grid(row=0, column=1)

        #Botão de enviar
        self.sendbutton = tk.Button(self.input_frame, text="Enviar", command=self.send_message, foreground="black", justify="right", background="#c5c6d6",  font=("Poppins", 14))
        self.sendbutton.grid(row=0, column=2)  

        # Imagens para o bot e o usuário
        self.bot_icon = ImageTk.PhotoImage(Image.open("./img/bot.png"))
        self.user_icon = ImageTk.PhotoImage(Image.open("./img/user.png"))
    
        #Mensagens iniciais do bot de boas vindas & mostra a nuvem de palavras
        self.show_message("Olá! Faça qualquer pergunta sobre pizza e eu tentarei responder.", tag="chatbot_tag")
        self.show_message("Você pode consultar a nuvem de palavras gerada para saber o que perguntar.", tag="chatbot_tag")
        self.show_message("Se quiser parar, é só digitar 'sair'!", tag="chatbot_tag")
        self.chatbot_logic.createWordCloud()

    #Tkinter pega a mensagem do usuário e chama o answer do chatbot
    def send_message(self):
        user_message = self.userEntry.get()
        chatbot_answer = self.chatbot_logic.answer(user_message)
        
        if user_message.lower() == 'sair':
            self.show_message("Você: " + user_message, "user_tag")
            self.userEntry.delete(0, tk.END)
            self.window.destroy()
        else:
            self.show_message(user_message, "user_tag")
            self.show_message(chatbot_answer, "chatbot_tag")
            self.userEntry.delete(0, tk.END)

    def show_message(self, message, tag=None):
        if tag == "user_tag":
            self.messageswindow.image_create(tk.END, image=self.user_icon)
        elif tag == "chatbot_tag":
            self.messageswindow.image_create(tk.END, image=self.bot_icon)
    
        self.messageswindow.config(state=tk.NORMAL)
        self.messageswindow.insert(tk.END, " " + message + "\n", tag)
        self.messageswindow.config(state=tk.DISABLED)

    def iniciar(self):
        self.window.mainloop()

if __name__ == "__main__":
    chatbot_logic = ChatbotLogic()
    chatbot_ui = ChatbotUi(chatbot_logic)
    chatbot_ui.iniciar()
