from pypdf import PdfReader

reader = PdfReader(
    r"D:\AI_SERVER\documents\heredity.pdf"
)

print(reader.pages[0].extract_text())
