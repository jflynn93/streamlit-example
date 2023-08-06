#import tensorflow as tf
import openai
import pinecone
import streamlit as st
from time import sleep

st.title("Budd-E")
# get secret vars
openai.api_key = st.secrets["OPENAI_API_KEY"]
pinecone_api_key = st.secrets["pinecone_api_key"]
index_name = st.secrets["index_name"]
my_environ = st.secrets["my_environ"]
# set embedding model 
embed_model = "text-embedding-ada-002"
# initialize connection to pinecone 
pinecone.init(
    api_key='pinecone_api_key',
    environment='my_environ' # may be different, check at app.pinecone.io
)
#  Send to pinecone 
index = pinecone.Index('index_name')

query = st.text_input("What do you want to know?")  


 # first let's make it simpler to get answers
def complete(prompt):
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

    # build our prompt with the retrieved contexts 
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

    
# radio buttomn 
    
if st.button("Search"):
    query_with_contexts = retrieve_base(query)
    answer = complete(query_with_contexts)
    st.markdown("### Answer:")
    st.write(response.choices[0]['message']['content'])
      

 
