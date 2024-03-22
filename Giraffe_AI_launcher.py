# pip install customtkinter
import os

import customtkinter
from PIL import Image

from db_builder import db_window
from chatbot import chat_window
from doc_retriever import doc_window

IMG_DIRECTORY = os.path.join(os.path.dirname(__file__), 'giraffe.png')

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("dark-blue")

class home(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x600")
        self.title("Giraffe AI")
        
        self.logo_image = customtkinter.CTkImage(light_image=Image.open(IMG_DIRECTORY), size=(400, 600))
        self.image_label = customtkinter.CTkLabel(master=self, image=self.logo_image, text="")
        self.image_label.grid(column=0, row=0)

        self.main_frame = customtkinter.CTkFrame(master=self, width=300, height=600)
        self.main_frame.grid(column=1,row=0)
        self.welcome_message = customtkinter.CTkLabel(master=self.main_frame, text="Giraffe AI Hybrid\n version 1.0", font=customtkinter.CTkFont(size=20, weight="bold"), width=300, height=300)
        self.welcome_message.grid(row=0, column=1)
        self.db_button = customtkinter.CTkButton(master=self.main_frame, text="Build Database", command=self.db_event, width=200)
        self.db_button.grid(row=1, column=1, padx=30, pady=(15, 15))
        self.doc_button = customtkinter.CTkButton(master=self.main_frame, text="Document Retrieval", command=self.doc_event, width=200)
        self.doc_button.grid(row=2, column=1, padx=30, pady=(15, 15))
        self.doc_button = customtkinter.CTkButton(master=self.main_frame, text="AI Chatbot", command=self.chat_event, width=200)
        self.doc_button.grid(row=3, column=1, padx=30, pady=(15, 140))

    def db_event(self):
        db_ui = db_window()

    def doc_event(self):
        doc_ui = doc_window()

    def chat_event(self):
        chat_ui = chat_window()

home_ui = home()
home_ui.mainloop()

