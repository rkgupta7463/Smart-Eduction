from flask import Flask, render_template, request
from translate import translator  # Import your translation function
import PyPDF2
 
app = Flask(__name__)


def pdf_extract_text(pdf_path):
    extracted_text = ""

    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Iterate through each page
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text = page.extractText()

            # Check if the text is in English
            if all(ord(char) < 128 for char in text):
                extracted_text += text

    return extracted_text


@app.route("/", methods=['GET', 'POST'])
def home():
    translated_statement = None
    input_statement = None

    if request.method == "POST":
        problemType = request.form.get('problemType')
        text = request.form.get('textInput')
        input_statement = text
        source_lang = "en_XX"  # English
        target_lang = "hi_IN"  # Hindi

        # Call the translation function to translate to Hindi
        translated_statement = translator(
            input_text=input_statement, src_lang=source_lang, tgt_lang=target_lang)

        # if problemType == "text":
        #     text = request.form.get('textInput')
        #     input_statement = text
        #     source_lang = "en"  # English
        #     target_lang = "hi"  # Hindi

        #     # Call the translation function to translate to Hindi
        #     translated_statement = translator(
        #         input_text=input_statement, src_lang=source_lang, tgt_lang=target_lang)

        # elif problemType == "pdf":
        #     pdf_file = request.files['pdfInput']
        #     if pdf_file:
        #         pdf_text = pdf_extract_text(pdf_file)
        #         # You can process pdf_text here or pass it to translation
        #         print("PDF Extract:- ", pdf_text)

        # elif problemType == "word":
        #     # Handle Word file logic here
        #     pass

        # elif problemType == "image":
        #     # Handle Image file logic here
        #     pass

    return render_template("home.html", translated_statement=translated_statement)


if __name__ == "__main__":
    app.run(debug=True)
