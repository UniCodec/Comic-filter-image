from tkinter import *
from tkinter.ttk import Style

from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
from tkinter.filedialog import asksaveasfile

a = Tk()
toolbar = Frame(a)
toolbar2 = Frame(a)
text = Text(a)
a.title("Image to Comic")
a.geometry("1300x850+350+75")
a.resizable(width=True, height=True)


def mFileopen():
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.tif;*.gif;*.bmp;*.tiff;*.eps;*.raw;*.cr2;*.nef;*.orf;*.sr2"),
                   ("All files", "*.*")))
    print(file_path)
    img = Image.open(file_path)
    img = img.resize((450, 450), Image.ANTIALIAS)
    # display as photo
    img = ImageTk.PhotoImage(img)
    panel = Label(a, image=img, borderwidth=3, relief="solid")
    panel.image = img
    panel.pack(side=LEFT, padx=90, pady=20)
    toolbar.pack(side=TOP)


def mProcess():
    global img
    print("File path outside the function")
    print(file_path)
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    b_img = cv2.medianBlur(gray, 7)

    low_sigma = cv2.GaussianBlur(b_img, (3, 3), 0)
    high_sigma = cv2.GaussianBlur(b_img, (15, 15), 0)
    # 0 is starting point

    # Calculate the DoG by subtracting
    dog = low_sigma - high_sigma
    dog = cv2.fastNlMeansDenoising(dog, None, 90, 7, 21)
    # output window size as it is, threshold, 7 window size, 21 size of matrix

    edges = cv2.Canny(b_img, 45, 7)
    # largest value find initial edges, smaller value link edges
    edges = cv2.fastNlMeansDenoising(edges, None, 50, 7, 21)
    final_edges = cv2.addWeighted(dog, 1, edges, 1, 0)

    ret, final_edges = cv2.threshold(final_edges, 127, 255, cv2.THRESH_BINARY_INV)

    final_edges = cv2.bilateralFilter(final_edges, 7, 75, 75)
    # filter resize, sigma size(difference between 2 neighbors), sigma color(influence #no. of pixel)

    # 2) Color
    color = cv2.bilateralFilter(img, 9, 300, 300)
    b, g, r = cv2.split(color)
    b = cv2.medianBlur(b, 5)
    g = cv2.medianBlur(g, 5)
    r = cv2.medianBlur(r, 5)
    color = cv2.merge((b, g, r))

    # k-maens clustering used for color quantization
    # kmeans function which takes a 2D array in input and since our original image is 3D(height, width, depth)
    Z = color.reshape((-1, 3))
    # reshape 3D image to 2D image

    # convert to np.float32, each feature should be put in a single column
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    # stop the iteration when any of the above condition is met
    # max_iter - An integer specifying maximum number of iterations
    #  epsilon - Required accuracy

    K = 8
    # Number of clusters required
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS) # 10 is iteration

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    # flatten() is used to convert into 1D array and res gives result of multiple 1D array
    color = res.reshape((color.shape))
    # reshape our color image with res

    color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)

    # multiple by a factor to change the saturation
    color[..., 1] = color[..., 1] * 1.5

    color = cv2.cvtColor(color, cv2.COLOR_HSV2BGR)

    # 3) Comic
    comic = cv2.bitwise_and(color, color, mask=final_edges)
    # color image multiply with color image and rotate the mask on this image
    comic = comic[..., ::-1]
    # put into 0-255
    new_img = Image.fromarray(comic)
    # to show an image

    img = new_img.resize((450, 450), Image.ANTIALIAS)
    img_1 = ImageTk.PhotoImage(img)
    panel = Label(a, image=img_1, borderwidth=3, relief="solid")
    panel.image = img_1
    panel.pack(side=RIGHT, padx=90, pady=10)
    toolbar.pack(side=TOP)


def save():
    files = [("Image files", "*.jpg;*.jpeg;*.png;*.tif;*.gif;*.bmp;*.tiff;*.eps;*.raw;*.cr2;*.nef;*.orf;*.sr2"),
             ("All files", "*.*")]
    file = asksaveasfile(filetypes=files, defaultextension=".jpg")
    img.save(file)


btn1 = Button(toolbar, text="Upload your file", height=3, width=20, command=mFileopen)
btn1.pack(side=LEFT, padx=190, pady=50)
toolbar.pack(side=TOP, fill=X, padx=30, pady=10)

btn2 = Button(toolbar, text="Run", height=3, width=20, command=mProcess)
btn2.pack(side=RIGHT, padx=190, pady=20)
toolbar.pack(side=TOP, fill=X)

btn3 = Button(toolbar2, text="Note:Choose Only Image", foreground="pink", bg="yellow", fg="white", height=2, width=20)
btn3.pack(side=LEFT, padx=190, pady=10)
btn3.configure(state="disable", font=('Sans', '11', 'bold'))
toolbar2.pack(side=BOTTOM, fill=X, padx=30, pady=10)

btn4 = Button(toolbar2, text="Download", height=2, width=20, command=lambda: save())
btn4.pack(side=RIGHT, padx=190, pady=20)
toolbar2.pack(side=BOTTOM, fill=X, padx=50, pady=10)

a.mainloop()
