import PyPDF2
import docx
from flask import Flask, render_template, request
from translate import translator  # Import your translation function
import os


app = Flask(__name__)


# PDF texts Extaction function
def pdf_extract_text(pdf_file):
    extracted_text = ""

    # Create a PyPDF2 reader object from the file
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Iterate through each page
    for page in pdf_reader.pages:
        text = page.extract_text()

        # Check if the text is in English
        if all(ord(char) < 128 for char in text):
            extracted_text += text

    return extracted_text


# Word Docx Texts Extraction function
def docx_extract_text(docx_file):
    extracted_text = ""

    # Create a Docx reader object from the file
    doc = docx.Document(docx_file)

    # Iterate through paragraphs and extract text
    for paragraph in doc.paragraphs:
        text = paragraph.text
        extracted_text += text

    return extracted_text



@app.route("/", methods=['GET', 'POST'])
def home():
    translated_statement = None
    input_statement = None

    if request.method == "POST":
        problemType = request.form.get('problemType')

        if problemType == "text":
            text = request.form.get('textInput')
            input_statement = text
            source_lang = "en_XX"  # English
            target_lang = "hi_IN"  # Hindi
            # Call the translation function to translate to Hindi
            translated_statement = translator(
                input_text=input_statement, src_lang=source_lang, tgt_lang=target_lang)

        elif problemType == "pdf":
            pdf_file = request.files['pdfInput']
            if pdf_file:
                # Extract text from the uploaded PDF file
                pdf_text = pdf_extract_text(pdf_file)
                print("Extacted PDF:- ", pdf_text)
                input_statement = pdf_text
                source_lang = "en_XX"  # English
                target_lang = "hi_IN"  # Hindi

                # Call the translation function to translate to Hindi
                translated_statement = translator(input_text=input_statement, src_lang=source_lang, tgt_lang=target_lang)

        elif problemType == "word":
            # Handle Word file logic here
            pdf_file = request.files['wordInput']
            if pdf_file:
                # Extract text from the uploaded PDF file
                pdf_text = docx_extract_text(pdf_file)
                print("Extacted PDF:- ", pdf_text)
                input_statement = pdf_text
                source_lang = "en_XX"  # English
                target_lang = "hi_IN"  # Hindi

                # Call the translation function to translate to Hindi
                translated_statement = translator(input_text=input_statement, src_lang=source_lang, tgt_lang=target_lang)

        elif problemType == "image":
            # Handle Image file logic here
            pass

    return render_template("home.html", translated_statement=translated_statement)


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
