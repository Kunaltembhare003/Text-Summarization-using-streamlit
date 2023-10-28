# Text Summarization

This is a text summarization project that allows you to summarize text, web content, and PDF documents using the PEGASUS pre-trained model. The summarization is done through a Streamlit web application.

## Prerequisites

To use the text summarization model, you need to follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Kunaltembhare003/Text-Summarization-using-streamlit.git
   ```

1. Navigate to the project directory:

    ```bash
    cd text-summarization-project
    ```
1. Install the required Python packages using the provided requirements.txt file:
    ```bash
    pip install -r requirements.txt
    ```

1. Download the model files and place them in the "resource/pegasus-cnn-model" folder:

    * Download the model files ( pytorch_model.bin)
    Place the downloaded model and tokenizer files in the "resource/pegasus-cnn-model" folder within the project directory.

# Usage

To use the text summarization application, follow these steps:

1. Make sure you have completed the prerequisites mentioned above.

1. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

1. Access the web application in your browser at the provided URL (usually http://localhost:8501).

1. Choose your input source (Text, URL, or PDF) and provide the content.

1. Set your summarization preferences (e.g., maximum and minimum length).

1. Click the "Summarize" button to generate the summary.

1. The generated summary will be displayed on the web application.

# Supported Input Sources
* Text: You can directly enter or paste the text you want to summarize.

* URL: Provide the URL of a web page, and the application will extract the content and summarize it.

* PDF: Upload a PDF file, and the application will extract the text from the PDF and provide a summary.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

