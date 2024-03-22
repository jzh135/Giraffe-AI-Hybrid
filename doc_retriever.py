import os

from typing import Tuple
from langchain_community.vectorstores import Chroma
from chromadb.config import Settings

import tkinter as tk
from tkinter import*
import customtkinter

from model_loader import db

## Load embedding function
#embeddings = get_bge_zh_embeddings()
## Load local database
#db = Chroma(persist_directory=DB_DIRECTORY, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)

# SmartDoc UI

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("dark-blue")

class doc_window(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("960x600")
        self.title("SmartDoc Retriever")
        self.attributes('-topmost',True) # make this window above the home
        self.answer_box = customtkinter.CTkTextbox(master=self, 
                                                   width=860, 
                                                   height=400, 
                                                   font=("Arial", 15),
                                                   fg_color=("lightgrey","grey"))
        # Position of answer box
        self.answer_box.pack(pady=20, padx=25)

        self.question_box = customtkinter.CTkEntry(master=self, 
                                                   width=860, 
                                                   height=50, 
                                                   font=("Arial", 15), 
                                                   placeholder_text="Enter your query here...",
                                                   fg_color=("white","grey"))
        # Position of question box
        self.question_box.pack(pady=(0,20), padx=25)

        self.bottom_frame = customtkinter.CTkFrame(master=self,
                                                   width=860, 
                                                   height=50)
        # Position of button frame
        self.bottom_frame.pack(pady=(0,20), padx=25)
        self.send_button = customtkinter.CTkButton(master=self.bottom_frame, 
                                                   text="Send Query", 
                                                   command=self.search)
        self.zh_button = customtkinter.CTkButton(master=self.bottom_frame, 
                                                   text="Spare",
                                                   command=self.zh_search)
        self.clear_answer_button = customtkinter.CTkButton(master=self.bottom_frame, 
                                                    text="Clear History", 
                                                    command=self.clear_answer)
        self.back_button = customtkinter.CTkButton(master=self.bottom_frame, 
                                                   text="Back",
                                                   command=self.back)
        # Position of buttons
        self.send_button.grid(row=0, column=0)
        self.zh_button.grid(row=0, column=1, padx=10)
        self.clear_answer_button.grid(row=0, column=2, padx=(0,10))
        self.back_button.grid(row=0, column=3)

        # Welcome message
        self.answer_box.insert('end', "Welcome to Giraffe AI ChatBot！\n")

    def search(self):
        user_message = self.question_box.get()
        self.answer_box.insert('end', f"\n> User: {user_message}\n")
        #self.question_box.delete('0', tk.END)  # First index must be '0' for Text box

        # Get the answer from the database
        sim_results = db.similarity_search_with_relevance_scores(user_message, k=2)

        # Display the answer and source documents
        self.answer_box.insert('end', "\n> Results:\n")
        for sim_slice in sim_results:
            self.answer_box.insert('end', f"relevance score: {sim_slice[1]}\n")
            self.answer_box.insert('end', f"{sim_slice[0].metadata['source']}\n")
            self.answer_box.insert('end', f"{sim_slice[0].page_content}\n")
            self.answer_box.insert('end', "-----------------------------\n")
    
    def zh_search(self):
        pass
    
    def clear_answer(self):
        self.answer_box.delete('1.0', tk.END) # First index must be '1.0' for Entry box

    def back(self):
        self.destroy()