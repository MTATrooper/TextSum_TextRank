from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5 import uic
import sys
from LoadDataFromFile import LoadDataFrom
from summarize import summary
from docx import Document
import requests

form_class = uic.loadUiType("Main.ui")[0]
def SaveTXT(path, text):
    f = open(path, 'w+')
    f.write(text)
    f.close()
def SaveDocx(path, text):
    document = Document()
    document.add_paragraph(text)
    document.save(path)
class MainWindow(QMainWindow, form_class):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.btnBrowse.clicked.connect(self.Browse)
        self.btnSummary.clicked.connect(self.Summary)
        self.btnSave.clicked.connect(self.Save)
        self.textSource = ''
        self.textSumm = ''
        
    def Browse(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.txt, *.doc, *.docx, *.html)", options=options)
        if(fileName):
            self.txtFilepath.setText(fileName)
            textOrigin = LoadDataFrom(fileName)
            self.txtOriginal.setPlainText(textOrigin)
            self.textSource = textOrigin
    
    def Summary(self):
        #textSumm = summary(self.textSource)
        dic = {'text': self.textSource}
        respond = requests.post('http://localhost:5555/summary', json=dic)
        textSumm = respond.json()['key']
        self.txtSummary.setPlainText(textSumm)
        self.textSumm = textSumm

    def Save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save File", "",
                "All Files (*);;Text Files (*.txt);;MS Word Files (*.docx)", options=options)
        if fileName:
            if(fileName.split('.')[-1] == 'doc' or 
                fileName.split('.')[-1] == 'docx'):
                SaveDocx(fileName, self.textSumm)
            else:
                SaveTXT(fileName, self.textSumm)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    
    app.exec_()