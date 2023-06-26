#imports for image processing, character recognition, GUI, regex, and data structure
from PIL import Image
import pytesseract as ocr
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import scrolledtext
import numpy as np
import re
import cv2
from trie import Trie

class App:
    def __init__(self, path):
        #configuring window
        self.root = tk.Tk()
        self.root.title('Image Text Search')
        self.root.geometry('850x500')
        
        #setting pytesseract to its executable
        ocr.pytesseract.tesseract_cmd = path
        
        #text variable for user input, display for text content from images
        self.user_value = tk.StringVar()
        self.display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font='tahoma 12',
            width=20, height=20, state='disabled')
        
        #entry box for user input
        self.entry = tk.Entry(self.root, font='tahoma 12', textvariable=self.user_value)
        self.entry.bind('<KeyRelease>', lambda event: self.search_trie())
        
        #directions for app, upload and refresh buttons
        self.directions = tk.Label(self.root, font='tahoma 12', text='Steps to search text in images:' +
            '\n1. Upload image file\n2. Type into box between buttons to search text\n' +
            '3. Click rightmost button to show all words again')
        self.upload = tk.Button(self.root, font='tahoma 12', text='Upload image file', command=self.select_file)
        self.refresh = tk.Button(self.root, font='tahoma 12', text='Refresh word list', command=self.refresh_list)
        
        #setting widgets into grid on screen with padding and filling up cell entirely
        self.upload.grid(row=0, column=0, padx=10, pady=10, sticky='NSEW')
        self.entry.grid(row=0, column=1, padx=10, pady=10, sticky='NSEW')
        self.directions.grid(row=1, column=0, padx=10, pady=10, sticky='NSEW')
        self.display.grid(row=1, column=1, padx=10, pady=10, sticky='NSEW')
        self.refresh.grid(row=0, column=2, padx=10, pady=10, sticky='NSEW')
        
        #configuring each row/column to fill cells as screen resizes
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        
        #data structure for storing and searching words
        self.trie = Trie()
    
    #begins GUI application to show screen
    def start_app(self):
        self.root.mainloop()
    
    #updating Text widget with conten
    def update_display(self, content):
        self.display.config(state='normal')
        self.display.delete(1.0, tk.END)
        
        for word in content:
            self.display.insert(tk.END, f'{word}\n')
        
        self.display.config(state='disabled')
    
    #applies OCR engine to file to extract text
    def read_image(self, filename):
        #normalize image and reduce noise to increase chances of reading characters
        img = np.array(Image.open(filename))
        norm_img = np.zeros((img.shape[0], img.shape[1]))
        
        #normalizing, thresholding, and applying blur to image
        img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
        img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
        img = cv2.GaussianBlur(img, (1, 1), 0)
        
        #extract any text from the new image
        text = ocr.image_to_string(img)
        
        #no text was found, inform the user
        if len(text) == 0:
            tk.messagebox.showinfo(title='Information', message='No text content found')
            return
        
        #build trie from text in image
        self.trie.build_trie(re.split('\\s+', text))
        word_list = list()
        self.trie.traverse_trie(self.trie.root, word_list, '')
        word_list.sort()
        
        self.update_display(word_list)
    
    #called when user hits button to upload file
    def select_file(self):
        #specifying file types and opening file chooser
        file_types = [('Image Files', '.png .jpg .jpeg .tiff .tif .git .bmp')]
        file = fd.askopenfilename(title='Select Image File', filetypes=file_types)
        
        #if no file selected, inform user to select one
        if len(file) == 0:
            tk.messagebox.showinfo(title='Error', message='Please select a file')
            return
        
        #try to read content from image
        self.read_image(file)
    
    #called when user releases key to search text
    def search_trie(self):
        #if trie not built yet or no input, do not do anything
        user_input = self.user_value.get().lower()
        if not self.trie.is_trie_present() or len(user_input) == 0:
            return
        
        matches = self.trie.search_trie(user_input)
        self.update_display(matches)
    
    #called when user hits button to show all words
    def refresh_list(self):
        #if no trie generated, stop
        if not self.trie.is_trie_present():
            tk.messagebox.showinfo(title='Error', message='Please upload an image first')
            return
        
        current_words = list()
        self.trie.traverse_trie(self.trie.root, current_words, '')
        current_words.sort()
        
        self.update_display(current_words)