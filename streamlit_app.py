#import tensorflow as tf
import openai
import pinecone
import streamlit as st
from time import sleep

st.title("Budd-E")

openai.api_key = st.secrets["OPENAI_API_KEY"]

query = st.text_input("What do you want to know?")

if st.button("Search"):
   
   

#from datasets import load_dataset
#from tqdm.auto import tqdm

#from PyPDF2 import PdfReader

 

 

# first let's make it simpler to get answers
def complete(prompt):
    # query text-davinci-003
    res = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=0,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return res['choices'][0]['text'].strip()

 

def retrieve_base(query):
    
    
    
    res = openai.Embedding.create(
         input=[query],
        engine=embed_model
     )

 

    # retrieve from Pinecone
    xq = res['data'][0]['embedding']

 

    # get relevant contexts
    res = index.query(xq, top_k=3, include_metadata=True)
    contexts = [
        x['metadata']['text'] for x in res['matches']
    ]

 

    # build our prompt with the retrieved contexts included
    prompt_start = (
        "Answer the question based on the context below.\n\n"+
        "Context:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {query}\nAnswer:"
    )
    # append contexts until hitting limit
    for i in range(0, len(contexts)):
    #    print(i)
        
        
        
        if len("\n\n---\n\n".join(contexts[:i])) >= 3750:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts[:i-1]) +
                prompt_end
            )
            break
        elif i == len(contexts)-1:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts) +
                prompt_end
            )
    return prompt   

 

################# Config ###################
# get API key from top-right dropdown on OpenAI website
openai.api_key = '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'
pinecone_api_key='4869f1d2-5980-402e-a8e0-5b6fe3557385'
 


# set embedding model 
embed_model = "text-embedding-ada-002"

# Provide an index name 
index_name = 'knowledge'

 
# initialize connection to pinecone 
pinecone.init(
    api_key=pinecone_api_key,
    environment='us-east4-gcp'  # may be different, check at app.pinecone.io
)
    
#  Send to pinecone 
index = pinecone.Index(index_name)

 

    
    
############################ Query ##################

 

 

# Now Run Query we complete the context-infused query
while (True):
    query = input("What would you like to know about?: ")
    print("")
    print("Responding....")
    print("")
#query = ("Tell be about terpenes")
    query_with_contexts = retrieve_base(query)
    print(complete(query_with_contexts))
    print("")

 
