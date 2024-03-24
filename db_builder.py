import os
import shutil
from langchain.docstore.document import Document
from langchain_community.document_loaders import TextLoader
from langchain.document_loaders.pdf import PyMuPDFLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from datetime import datetime

import tkinter as tk
from tkinter import*
import customtkinter

from model_loader import db
from constants import SOURCE_DIRECTORY, METADATA_DIRECTORY, ARCHIVE_SOURCE_DIRECTORY

# Define a dictionary to map file extensions to their respective loaders
LOADER_ENGINES = {
    '.pdf': PyMuPDFLoader,
    '.txt': TextLoader,
    '.csv': CSVLoader
}

def db_update_single(new_doc_path,db):
    ## Get database list of ids and metadata
    db_dic = db.get()
    ids_list = db_dic["ids"]
    meta_list = db_dic["metadatas"]
    ## Load and split new document
    # Check file type
    file_extension = os.path.splitext(new_doc_path)[1]
    file_name = os.path.splitext(new_doc_path)[0]
    # Load .txt file
    if file_extension == ".txt":
        loader = TextLoader(new_doc_path,encoding='utf-8') # If not specific encoding, it will have rise UnicodeDecodeError
    # Load .pdf file
    elif file_extension == ".pdf":
        print("loading")
        loader = PyMuPDFLoader(new_doc_path)
    else:
        print(f"{file_name} is not supported")
        return None
    pages = loader.load()
    # Initialize new_doc
    new_doc = [Document]
    new_doc[0].page_content = ""
    new_doc[0].metadata = pages[0].metadata
    for page in pages:
            new_doc[0].page_content = new_doc[0].page_content + page.page_content
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    new_doc_slices = text_splitter.split_documents(new_doc)

    ## Check if the new document file name is existed in the database and remove the duplicate old document vectors
    i = 0
    for slice_meta_data in meta_list:
        if file_name in slice_meta_data["source"]:
            ids = ids_list[i]
            print(f"Existed document slice with ids = {ids} from file {file_name} is removed from the database")
            db.delete(ids)
        i = i+1
    ## Add new document slices to database
    print(f"{len(new_doc_slices)} slices are loaded successfully")
    db.add_documents(new_doc_slices)
    print(f"New document {file_name} is added to the database")
    return None
    

def db_update(db,source_directory):
    for root, _, files in os.walk(source_directory):
        for file_name in files:
            #file_extension = os.path.splitext(file_name)[1]
            source_file_path = os.path.join(root, file_name)
            # Remove duplicate files and get new document slices
            db_update_single(new_doc_path=source_file_path, db=db)
            # Move source file to the archive folder
            archive_source_file =  os.path.join(ARCHIVE_SOURCE_DIRECTORY, file_name)
            # Delete the old file in archive folder
            if os.path.exists(archive_source_file):
                os.remove(archive_source_file)
                print(f"{file_name} in {ARCHIVE_SOURCE_DIRECTORY} was successfully deleted.")
            else:
                print(f"{file_name} does not exist in {ARCHIVE_SOURCE_DIRECTORY}.")
            # Add new file to archive folder
            shutil.move(source_file_path, ARCHIVE_SOURCE_DIRECTORY)
    return None


#db_update_single(db=en_db, new_doc_path=EN_SINGLE_SOURCE, source_directory=EN_SOURCE_DIRECTORY)
#db_update(db=db, source_directory=SOURCE_DIRECTORY)
#db_update(db=zh_db, source_directory=ZH_SOURCE_DIRECTORY)
customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("dark-blue")

class db_window(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("700x350")
        self.title("Giraffe AI Chatbot")
        self.attributes('-topmost',True) # make this window above the home
        self.info_box = customtkinter.CTkTextbox(master=self, 
                                                   width=650, 
                                                   height=250, 
                                                   font=("Arial", 15),
                                                   fg_color=("lightgrey","grey"))
        # Position of answer box
        self.info_box.pack(pady=20, padx=25)

        self.bottom_frame = customtkinter.CTkFrame(master=self,
                                                   width=550, 
                                                   height=50)
        # Position of button frame
        self.bottom_frame.pack(pady=(0,20), padx=25)
        self.build_button = customtkinter.CTkButton(master=self.bottom_frame, 
                                                   text="Build DB",
                                                   command=self.db_build)
        self.spare_button = customtkinter.CTkButton(master=self.bottom_frame, 
                                                   text="Spare",
                                                   command=self.zh_db_build)
        self.check_button = customtkinter.CTkButton(master=self.bottom_frame, 
                                                    text="Check", 
                                                    command=self.db_check)
        self.back_button = customtkinter.CTkButton(master=self.bottom_frame, 
                                                   text="Back",
                                                   command=self.back)
        # Position of buttons
        self.build_button.grid(row=0, column=0)
        self.spare_button.grid(row=0, column=1, padx=[10,0])
        self.check_button.grid(row=0, column=2, padx=10)
        self.back_button.grid(row=0, column=3)

        # Welcome message
        self.info_box.insert('end', "Welcome to Giraffe AI Database Builder\n")

    
    def db_build(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.info_box.insert('end', f"\n{current_time} > Embedder is loaded\n")
        db_update(db=db, source_directory=SOURCE_DIRECTORY)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.info_box.insert('end', f"\n{current_time} > Database is updated\n")
        # Generate database report
        en_db_dic = db.get()
        ids_list = en_db_dic["ids"]
        self.info_box.insert('end', f"\n > The database is comprised of {len(ids_list)} segments of embedded data\n")
    
    def zh_db_build(self):
        pass

    def db_check(self):
        en_db_dic = db.get()
        ids_list = en_db_dic["ids"]
        self.info_box.insert('end', f"\n > The database is comprised of {len(ids_list)} segments of embedded data\n")

    def back(self):
        self.destroy()
