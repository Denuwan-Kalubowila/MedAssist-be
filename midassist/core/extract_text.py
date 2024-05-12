import PyPDF2


def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    try:
        # Open the PDF file
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Loop through each page and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()

        return pdf_text
    except Exception as e:
        print("Error extracting text from PDF:", str(e))
        return ""
