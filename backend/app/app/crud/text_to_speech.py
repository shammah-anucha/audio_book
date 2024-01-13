from PyPDF2 import PdfReader
from gtts import gTTS



# # Replace 'mysql://user:password@localhost/dbname' with your MySQL connection string
# db_url = 'mysql://user:password@localhost/dbname'
# engine = create_engine(db_url)
# Base.metadata.create_all(engine)

# Session = sessionmaker(bind=engine)
# session = Session()

def pdf_to_text(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

def text_to_audio(text, output_path):
    tts = gTTS(text=text, lang='en')
    tts.save(output_path)



# # Example usage:
# pdf_path = 'sample.pdf'  # Replace with your PDF file path
# output_path = 'output.mp3'  # Replace with desired audio output path
# title = 'Sample Audio'

# text_content = pdf_to_text(pdf_path)
# text_to_audio(text_content, output_path)
# save_to_database(title, text_content)
