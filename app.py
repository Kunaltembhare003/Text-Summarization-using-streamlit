import streamlit as st
import requests
import fitz  # PyMuPDF
import pdfplumber
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

@st.cache_resource
def load_summarizer():
    model_name = "resource/pegasus-cnn-model"  # Replace with your own model name
    tokenizer_name = "resource/tokenizer"
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

def generate_chunks(inp_str):
    max_chunk = 500
    inp_str = inp_str.replace('.', '.<eos>')
    inp_str = inp_str.replace('?', '?<eos>')
    inp_str = inp_str.replace('!', '!<eos>')
    
    sentences = inp_str.split('<eos>')
    current_chunk = 0 
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1: 
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])
    return chunks

tokenizer, model = load_summarizer()
st.title("Text Summarization")
#sentence = st.text_area('Please paste your article:', height=30)
#button = st.button("Summarize")
# Input options
input_option = st.selectbox("Choose Input Source", ("Text", "URL", "PDF"))

# Depending on the input source, show relevant fields
if input_option == "Text":
    input_text = st.text_area("Enter text to summarize")
    button = st.button("Summarize")
elif input_option == "URL":
    url = st.text_input("Enter the URL")
    button = st.button("Summarize")
elif input_option == "PDF":
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    button = st.button("Summarize")
# Extract text from URL
# Function to extract text from a URL
def extract_text_from_url(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all the text content (excluding HTML tags)
            text = soup.get_text()

            return text
        else:
            return f"Request failed with status code {response.status_code}"
    except Exception as e:
        return str(e)


max_length = st.sidebar.slider('Select max', 50, 500, step=10, value=150)
min_length = st.sidebar.slider('Select min', 10, 450, step=10, value=50)
do_sample = st.sidebar.checkbox("Do sample", value=False)

with st.spinner("Generating Summary.."):
    if input_option =="Text":
        if button and input_text:
            chunks = generate_chunks(input_text)
            summaries = []

            for chunk in chunks:
                input_ids = tokenizer.encode(chunk, return_tensors="pt", max_length=1024, truncation=True)
                summary_ids = model.generate(input_ids, max_length=max_length, min_length=min_length, do_sample=do_sample)
                summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                summaries.append(summary)

            text = ' '.join(summaries)
            st.write(text)
    # process url        
    if input_option =="URL":
        if button and input_option:
            extracted_text = extract_text_from_url(url)
            chunks = generate_chunks(extracted_text)
            summaries = []

            for chunk in chunks:
                input_ids = tokenizer.encode(chunk, return_tensors="pt", max_length=1024, truncation=True)
                summary_ids = model.generate(input_ids, max_length=max_length, min_length=min_length, do_sample=do_sample)
                summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                summaries.append(summary)

            text = ' '.join(summaries)
            input_ids = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)
            summary_ids = model.generate(input_ids, max_length=max_length, min_length=min_length, do_sample=do_sample)
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
              
            st.write(summary)

    # process pdf
    if input_option == 'PDF':
        if button and pdf_file:
            pdf_text = ""
            # Open the PDF file
            try:
                with pdfplumber.open(pdf_file) as pdf:
                    # Loop through each page in the PDF file
                    for page in pdf.pages:
                        # Extract text from the page
                        text = page.extract_text()
                        pdf_text += text

                chunks = generate_chunks(pdf_text)
                summaries = []

                for chunk in chunks:
                    input_ids = tokenizer.encode(chunk, return_tensors="pt", max_length=1024, truncation=True)
                    summary_ids = model.generate(input_ids, max_length=max_length, min_length=min_length, do_sample=do_sample)
                    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                    summaries.append(summary)

                text = ' '.join(summaries)
                input_ids = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)
                summary_ids = model.generate(input_ids, max_length=max_length, min_length=min_length, do_sample=do_sample)
                summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
              
                st.write(summary)
            except Exception as e:
                st.error(f"Error while processing PDF: {str(e)}")
            

