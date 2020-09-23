import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# filename = 'enter the name of the file here' 
# pdfFileObj = open('credit-suisse-gri-content-index-2019.pdf', 'rb')
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# num_pages = pdfReader.numPages
# count = 0
# text = ""

# while count < num_pages:
#     pageObj = pdfReader.getPage(count)
#     count +=1
#     text += pageObj.extractText()
# if text != "":
#    text = text
# else:
#    text = textract.process(fileurl, method='tesseract', language='eng')

f = open("raw2.txt", "r")
text = ""
for line in f:
    text += line

tokens = word_tokenize(text)
punctuations = ['(',')',';',':','[',']',',']
keywords = [word for word in tokens if not word in punctuations and word.isalpha()]
keywordSet = set(keywords)
with open('raw_formatted2.txt', 'w') as f:
    for word in keywordSet:
        f.write("%s\n" % word.lower())
