# https://www.linuxuprising.com/2019/05/how-to-convert-pdf-to-text-on-linux-gui.html
# https://pypi.org/project/ocrmypdf/
import os
import glob
import PyPDF2   # pip install PyPDF2 #pip3 install PyPDF2
# https://www.linuxuprising.com/2019/05/how-to-convert-pdf-to-text-on-linux-gui.html
# Command: apt install poppler-utils

# Bilder in PDF umwandeln
# https://pypi.org/project/ocrmypdf/
# Command: apt-get install ocrmypdf

os.chdir("/root/patenteMarcel/Patente/")
for file in glob.glob("*.pdf"):
    #print("pdftotext -layout /root/patenteMarcel/Patente/"+file+" "+file+".txt")
    os.system("ocrmypdf --jobs 40 "+"/root/patenteMarcel/Patente/"+file+" "+file+".fulltext.pdf") # convert image pdf from patente source to fulltext pdf
    os.system("pdftotext -layout /root/patenteMarcel/Patente/"+file+".fulltext.pdf"+" "+file+".txt")    # fulltext pdf to text file
    """
    pdfFileObject = open("/root/patenteMarcel/Patente/"+file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    print(" No. Of Pages :", pdfReader.numPages)
    maxPages = int(pdfReader.numPages)
    for a in range(maxPages):
        pageObject = pdfReader.getPage(a)
        print(pageObject.extractText())
    """
