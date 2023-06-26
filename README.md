# Image-Text-Search
Python Tkinter GUI application using PyTesseract to read text from images and search through the text

Dependencies (may require installation):
- NumPy
- CV2
- PyTesseract
- Pillow

Other non-local modules used are tkinter and re, which are included with Python.

This desktop application uses Tkinter for the interface and it is designed for a user to upload an image file to search through its textual contents.
Current supported file types:
- PNG
- JPG/JPEG
- TIFF/TIF
- GIF
- BMP

The CV2 library is used for image processing to help reduce any noise present in the image.
This processed image is then input into PyTesseract and any text extracted is returned.
Finally, the text is converted into a trie for storage and efficient searching by users.

Note: for Windows use, the path to an installed PyTesseract executable must be passed for the initialization of the app.
As for Linux/MacOS, this may be unnecesary, but I have not tested it.

For all users, this should be ran with Python 3.10. At the time of writing, Python 3.11 is not supported by PyTesseract.