import os
#from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
#from langchain.chains import RetrievalQA
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.retrievers import EnsembleRetriever


from model_loader import get_llm, db

import tkinter as tk
from tkinter import*
import customtkinter

DB_DIRECTORY = os.path.join(os.path.dirname(__file__), 'data_base')

# Prompt template
template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}

    Helpful Answer:"""

prompt = PromptTemplate.from_template(template)

# Load LLM and Embeddings
llm = get_llm()

#db = Chroma(persist_directory=DB_DIRECTORY, embedding_function=embeddings)
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

#ensemble_retriever = EnsembleRetriever(retrievers=[retriever_1, retriever_2], 
#                                       weights=[0.5, 0.5])

#retriever = db.docsearch.as_retriever(
#    search_type="mmr",
#    search_kwargs={'k': 6, 'lambda_mult': 0.25} # 0 = max diversity
#)
# RetrievalQA
qa = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever, 
    return_source_documents=True,
    verbose=True,
    chain_type_kwargs={
    "prompt": prompt}
    )
# ChatBot UI

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("dark-blue")

class chat_window(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("960x600")
        self.title("Giraffe AI Chatbot")
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
                                                   command=self.send_question)
        self.zh_button = customtkinter.CTkButton(master=self.bottom_frame, 
                                                   text="Spare",
                                                   command=self.send_question_zh)
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

    def send_question(self):
        user_message = self.question_box.get()
        self.answer_box.insert('end', f"\n> User: {user_message}\n")
        self.question_box.delete('0', tk.END)  # First index must be '0' for Text box

        # Get the answer from the chain (replace with your actual QA function)
        res = qa(user_message)
        answer, docs = res["result"], res["source_documents"]

        # Display the answer and source documents
        self.answer_box.insert('end', "\n> Giraffe:\n")
        self.answer_box.insert('end', answer + "\n")
        self.answer_box.insert('end', "\n> SOURCE DOCUMENTS\n")
        for document in docs:
            self.answer_box.insert('end', f"\n> {document.metadata['source']}:\n")
            self.answer_box.insert('end', document.page_content + "\n")
    
    def send_question_zh(self):
        pass
    
    def clear_answer(self):
        self.answer_box.delete('1.0', tk.END) # First index must be '1.0' for Entry box

    def back(self):
        self.destroy()

