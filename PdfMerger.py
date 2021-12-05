from tkinter import *
import tkinter.font as tkFont
from tkinter import filedialog
from PyPDF2 import PdfFileReader, PdfFileMerger


class App:
    def __init__(self, master, screenWidth, screenHeight, font, background="white"):
        self.master = master
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.font = font
        self.background = background
        self.mainPdfPath = None
        self.extraPdfPath = None
        self.pdfMergePositionsPath = None
        self.mergedPdfPath = None
        self.master.title("PDF Merger")
        self.master.geometry(
            f"{self.screenWidth}x{self.screenHeight}+{int((self.master.winfo_screenwidth() / 2) - (self.screenWidth / 2))}+{int((self.master.winfo_screenheight() / 4) - (self.screenHeight / 2))}")
        self.master.resizable(False, False)
        self.master.configure(bg=background)

    def createWidgets(self):
        self.titleText = Label(self.master, text="PDF Merger", font=tkFont.Font(family=self.font, size=24)).place(
            relx=0.5,
            rely=0.1, anchor=CENTER)
        self.mainButton = Button(self.master, text="Choose Main PDF", font=tkFont.Font(family=self.font),
                                 command=self.getMainPdfPath).place(relx=0.5, rely=0.3, anchor=CENTER)
        self.extraButton = Button(self.master, text="Choose Extra PDF", font=tkFont.Font(family=self.font),
                                  command=self.getExtraPdfPath).place(relx=0.5, rely=0.5, anchor=CENTER)
        self.pdfMergePositionsButton = Button(self.master, text="Choose Positions Text File",
                                              font=tkFont.Font(family=self.font),
                                              command=self.getPdfMergePositionsFile).place(relx=0.5, rely=0.7,
                                                                                           anchor=CENTER)
        self.mergeButton = Button(self.master, text="Merge", font=tkFont.Font(family=self.font), command=self.mergePdfs)

    def getMainPdfPath(self):
        self.mainPdfPath = filedialog.askopenfilename(title="Select Main Pdf", initialdir="/",
                                                      filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))
        if len(self.mainPdfPath) == 0:
            self.mainPdfPath = None
        else:
            Label(self.master, text=f"Main File Path: {self.mainPdfPath}", fg="blue").place(relx=0.5, rely=0.4, anchor=CENTER)
        self.checkMerge()

    def getExtraPdfPath(self):
        self.extraPdfPath = filedialog.askopenfilename(title="Select Extra Pdf", initialdir="/",
                                                       filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))
        if len(self.extraPdfPath) == 0:
            self.extraPdfPath = None
        else:
            Label(self.master, text=f"Extra File Path: {self.extraPdfPath}", fg="blue").place(relx=0.5, rely=0.6,
                                                                                              anchor=CENTER)
        self.checkMerge()

    def getPdfMergePositionsFile(self):
        self.pdfMergePositionsPath = filedialog.askopenfilename(title="Select Merge Positions File", initialdir="/",
                                                                filetypes=(
                                                                    ("Text files", "*.txt"), ("All files", "*.*")))
        if len(self.pdfMergePositionsPath) == 0:
            self.pdfMergePositionsPath = None
        else:
            Label(self.master, text=f"Merge Positions Path: {self.pdfMergePositionsPath}", fg="blue").place(relx=0.5,
                                                                                                            rely=0.8,
                                                                                                            anchor=CENTER)
        self.checkMerge()

    def checkMerge(self):
        if self.mainPdfPath is not None and self.extraPdfPath is not None and self.pdfMergePositionsPath is not None:
            self.mergeButton.place(relx=0.5, rely=0.9, anchor=CENTER)

    def mergePdfs(self):
        self.mergedPdfPath = filedialog.asksaveasfilename(defaultextension=".pdf")
        if self.mergedPdfPath is None:
            return
        else:
            mainPdf = PdfFileReader(self.mainPdfPath)
            extraPdf = PdfFileReader(self.extraPdfPath)

            mergedPdf = PdfFileMerger()
            mergedPdf.append(mainPdf)

            with open(self.pdfMergePositionsPath, "r") as f:
                ls = f.read().split("\n")
                receiptPositionsList = list(map(int, [ls[i][:ls[i].index(":")] for i in range(len(ls))]))
                receiptGroupingsList = list(map(int, [ls[i][ls[i].index(" ") + 1:] for i in range(len(ls))]))
                receiptGroupingsList.insert(0, 0)

            j = 0
            for i in range(len(receiptPositionsList)):
                mergedPdf.merge(j + receiptPositionsList[i], extraPdf,
                                pages=(receiptGroupingsList[i], receiptGroupingsList[i + 1]))
                j += receiptGroupingsList[i + 1] - receiptGroupingsList[i]

            with open(self.mergedPdfPath, "wb") as f:
                mergedPdf.write(f)

    def do(self):
        self.createWidgets()


root = Tk()
myApp = App(root, 640, 360, "Courier")
myApp.do()
root.mainloop()
