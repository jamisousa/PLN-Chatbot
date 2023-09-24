from ChatUI import ChatbotUi
from Chatbot import ChatbotLogic
import tkinter as tk

if __name__ == "__main__":
    #chama a lógica do chatbot
    chatbot_logic = ChatbotLogic()

    #chama a lógica do tkinter
    chatbot_ui = ChatbotUi(chatbot_logic)

    #loop p/ atualizar a interface conforme as mensagens
    chatbot_ui.window.mainloop()