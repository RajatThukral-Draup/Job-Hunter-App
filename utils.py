import PyPDF2
import textract

def extractPdfText(filePath=''):
    fileObject = open(filePath, 'rb')
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
        text = textract.process(filePath, method='tesseract', encoding='utf-8')

    return text

