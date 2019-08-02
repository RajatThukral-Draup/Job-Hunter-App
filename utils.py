import PyPDF2
import textract
import pandas as pd
import numpy as np

def extractPdfText(fileObject=''):
    pdfFileReader = PyPDF2.PdfFileReader(fileObject)
    totalPageNumber = pdfFileReader.numPages

    print('This pdf file contains totally ' + str(totalPageNumber) + ' pages.')

    currentPageNumber = 0
    text = ''

    while (currentPageNumber < totalPageNumber):
        pdfPage = pdfFileReader.getPage(currentPageNumber)
        text = text + pdfPage.extractText()
        currentPageNumber += 1

    if (text == ''):
        return ''
    return text


ans_list = [2,1,1,2,2,1,4,1,1,1,1,1,4,1,1,3,2,1,1,1,1]
traits = ["visionary", "persuasive", "methodical", "agreeable", "challenge_driven", "reliant", "creative"]

def get_answers_traits(qa, ans_list = ans_list, traits = traits):
    a = []
    b = []
    for i in range(21):
        if eval(qa[i]) == ans_list[i]:
          a = a+[1]
        else:
          a = a+[0]
    a = np.array(a).reshape(-1, 3).tolist()
    for x in a:
        x = sum(x)/3
        b = b+[x]

    dictionary = dict(zip(traits, b))
    return dictionary


