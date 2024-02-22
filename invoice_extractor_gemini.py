#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import os
import google.generativeai as genai
from PIL import Image


# In[2]:


os.environ['GOOGLE_API_KEY'] = "your_api_key"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])


# In[4]:


# Function to load Gemini model

model = genai.GenerativeModel('gemini-pro-vision')
def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Converting images into bytes to pick specific areas of the image

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File not uploaded")


# In[6]:


# Initializing streamlit app

st.set_page_config(page_title= "Invoice Extractor")
st.header("Invoice Extractor")
input = st.text_input("Input Prompt: ", key="input")

uploaded_file = st.file_uploader("Choose an image of the invoice: ", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    
submit = st.button("Tell me about the invoice")

# Define the behaviour of Gemini Pro Model

input_prompt = '''
You are an expert which can understand invoices. I will upload the image of the invoice and
you will have to answer any questions I ask based on the uploaded invoice image
'''

# When submit button is clicked

if submit:
    image_data= input_image_setup(uploaded_file)
    response= get_gemini_response(input_prompt, image_data, input)
    st.write(response)


# In[ ]:




