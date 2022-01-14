import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile

from PIL import Image, ImageTk
import numpy as np
import cv2

from container import ScaleBarContainer

class InputPanel(ttk.Frame):
    """ Create the input panel of the picture application

    Attributes:
        inputFile: A string representing the path to the selected file.
    """
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        self.container = container
        self.inputFile = None
        self._displayFilePath = tk.StringVar()

        # create the selection button
        self._selectFrameBtn = ttk.Button(self, text="Select frame",
                                         command=self._popFileDialog)
        self._selectFrameBtn.grid(row=0, column=0, sticky='W')

        # create the label to display path of selected file
        self._selectedFileLbl = ttk.Label(self, textvariable=self._displayFilePath)
        self._selectedFileLbl.grid(row=0, column=1, sticky='EW')

    def _popFileDialog(self):
        """ Pop input file selection dialog window and save input file
        """
        open_file = askopenfile()
        if open_file:
            self.inputFile = open_file.name
            self._displayFilePath.set(self.inputFile)
            self.container.controller.updateFromInput(self.inputFile)


class DisplayPanel(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        self.container = container

        # Create default image
        self.imgh, self.imgw = 200, 200
        self.tk_img = ImageTk.PhotoImage(
            Image.fromarray(np.zeros((self.imgh, self.imgw, 3), dtype=np.uint8))
        )

        # Create canvas that displays the default image
        self._insertCanvas(self.imgh, self.imgw, self.tk_img)

    def _insertCanvas(self, imgh, imgw, tk_img):
        """ Insert image into canvas

        :param imgh:    An integer representing the height of input image
        :param imgw:    An integer representing the width of input image
        :param tk_img:  A Tkinter image
        """
        self.canvas = tk.Canvas(self, height=imgh, width=imgw)
        self.canvas.create_image(0,0, anchor='nw', image=tk_img)
        self.canvas.grid(row=0, column=0, sticky='E')
        self.canvas.bind("<Button-1>", self._savePos)
        self.canvas.bind("<B1-Motion>", self._addLine)

    def _savePos(self, event):
        self.x, self.y = event.x, event.y

    def _addLine(self, event):
        self.canvas.create_line((self.x, self.y, event.x, event.y))
        self._savePos(event)

    # def _zoomer(self, event):
    #     if (event.delta > 0):
    #         self.canvas.scale("all", event.x, event.y, 5, 5)
    #     elif (event.delta < 0):
    #         self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
    #     self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def update_image(self, img_path):
        """ Update the image in the canvas given a new input image path

        :param img_path: A string representing path to the new image
        """
        # read the new image into numpy array
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # update image aspect ratio
        self.imgh, self.imgw = img.shape[:2]
        self.tk_img = ImageTk.PhotoImage(Image.fromarray(img))

        # update the canvas
        self._insertCanvas(self.imgh, self.imgw, self.tk_img)

class ProcessingPanel(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.scaleBar1 = ScaleBarContainer(self, 0, 255, "Threshold parameter")
        self.scaleBar1.grid()

class Controller:
    def __init__(self, container):
        self.container = container

        # key internal environment variables
        self._inputFile = None

    def updateFromInput(self, inputFile):
        self._inputFile = inputFile
        self.container.displayPanel.update_image(self._inputFile)

class PictureApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.inputPanel = InputPanel(self)
        self.displayPanel = DisplayPanel(self)
        self.processingPanel = ProcessingPanel(self)
        self.controller = Controller(self)

        self.inputPanel.grid(row=0, column=0)
        self.displayPanel.grid(row=1, column=0)
        self.processingPanel.grid(row=1, column=1)

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = PictureApp()
    app.run()