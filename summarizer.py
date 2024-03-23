import os

from langchain.docstore.document import Document
from langchain_community.document_loaders import TextLoader
from langchain.document_loaders.pdf import PyMuPDFLoader
from langchain.document_loaders.csv_loader import CSVLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.chains import (
    StuffDocumentsChain,
    LLMChain,
    ReduceDocumentsChain,
    MapReduceDocumentsChain,
)
from langchain_core.prompts import PromptTemplate

from model_loader import get_llm
from constants import TRANSCRIPTION

def load_single(new_doc_path):
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
         print(f"{file_name}{file_extension} is not supported")
         return None
    pages = loader.load()
    # Initialize new_doc
    new_doc = [Document]
    new_doc[0].page_content = ""
    new_doc[0].metadata = pages[0].metadata
    for page in pages:
            new_doc[0].page_content = new_doc[0].page_content + page.page_content
    return new_doc

def summarizer(documents:list[Document]): # Argument must be the list of Document
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=8000, chunk_overlap=2000)
    new_doc_slices = text_splitter.split_documents(documents)
    print(len(new_doc_slices))
    # This controls how each document will be formatted. Specifically,
    # it will be passed to `format_document` - see that function for more
    # details.
    document_prompt = PromptTemplate(
        input_variables=["page_content"],
        template="{page_content}"
        )
    document_variable_name = "context"
    llm = get_llm()
    # The prompt here should take as an input variable the
    # `document_variable_name`
    prompt = PromptTemplate.from_template(
        "Summarize this content: {context}"
        )
    llm_chain = LLMChain(llm=llm, 
                         prompt=prompt,
                         verbose = True
                         )
    
    # Check length of the document, use map reduce documents chain when necessary
    if len(new_doc_slices) == 1:
         summary = llm_chain.invoke(new_doc_slices)
    else:
        # We now define how to combine these summaries
        reduce_prompt = PromptTemplate.from_template(
            "Combine these summaries: {context}"
            )
        reduce_llm_chain = LLMChain(
            llm=llm, 
            prompt=reduce_prompt,
            verbose = True
            )
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_llm_chain,
            document_prompt=document_prompt,
            document_variable_name=document_variable_name,
            verbose = True
            )
        reduce_documents_chain = ReduceDocumentsChain(
            combine_documents_chain=combine_documents_chain,
            verbose = True
            )
        map_reduce_chain = MapReduceDocumentsChain(
            llm_chain=llm_chain,
            reduce_documents_chain=reduce_documents_chain,
            document_variable_name = document_variable_name,
            verbose = True
            )
        summary = map_reduce_chain.invoke(new_doc_slices)
    return summary["text"]
     
## Test Code
"""
for root, _, files in os.walk(TRANSCRIPTION):
    for file_name in files:
        loaded_doc = load_single(os.path.join(root, file_name))
        if loaded_doc is None:
             print(f"{file_name} is not supported")
        else:
            summary = summarizer(loaded_doc)
    print(summary)
"""