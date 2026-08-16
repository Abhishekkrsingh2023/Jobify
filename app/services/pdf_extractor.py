from pypdf import PdfReader

def extract_text_from_pdf(file_path: str|None = None, stream: bytes|None = None) -> str:
    """_summary_

    Args:
        file_path (str): The path to the PDF file from which text needs to be extracted.
        stream (bytes): The byte stream of the PDF file from which text needs to be extracted.

    Returns:
        str: The extracted text from the PDF file.
    """
    if stream is not None:
        reader = PdfReader(stream)
    else:
        reader = PdfReader(file_path)
        
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# print(extract_text_from_pdf(file_path))