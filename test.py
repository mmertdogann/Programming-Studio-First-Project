from tkinter.colorchooser import askcolor
import PIL.Image
from tkinter import filedialog, colorchooser
from tkinter import *
from PIL import ImageTk, Image, ImageDraw

choosenColor=(0,0,0)
drawingImage = None
labelValues=None
global image1
image = None


def main():

    global root
    root = Tk()


    root.title("Basic Paint")
    root.geometry("800x600+500+100")
    root.configure(bg='#007700')

    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=openFile)
    filemenu.add_command(label="Draw", command=drawing)
    filemenu.add_command(label="SaveImage", command=saveImage)
    filemenu.add_command(label="SaveDrawimg", command=saveDrawing)
    filemenu.add_command(label="Clear", command=clear)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)


    root.config(menu=menubar)
    pickColor = Button(root, text="Pick Color", bg="#7fff00",
                       fg= "black", font="Verdana 12 bold italic", command=getColor).pack()


    root.mainloop()


def openFile():

    file_path = filedialog.askopenfilename()
    global drawingImage
    drawingImage = PIL.Image.open(file_path)
    drawingImage = drawingImage.resize((300,300))
    global pix
    pix = drawingImage.load()   

    xSize, ySize = drawingImage.size
    for i in range(xSize):
        for j in range(ySize):
            pix[i, j] = vanishNoisesFromPixel(pix[i, j])
    addToScreen(drawingImage)
    labeling(drawingImage)


def getColor():

        color = askcolor()
        r = color [0][0]
        g = color [0][1]
        b =color[0][2]
        global choosenColor
        choosenColor=int (r) ,int (g),int (b)
        print (choosenColor)




def saveImage():

    drawingImage.save("D:\\proje\\saved.png")

def clear():


    xSize, ySize = drawingImage.size
    for i in range(1, xSize):
        for j in range(1, ySize):
            if labelValues[i][j]!=1:
                pix[i,j] = (255,255,255)
                drawingImage.putpixel((i,j),(255,255,255))

    render = ImageTk.PhotoImage(drawingImage)
    img = Label(root, image=render)
    img.image = render
    img.place(x=250, y=100)
    img.bind("<Button-1>", printcoords)



def labeling (Img):

    Img=drawingImage
    xSize, ySize = drawingImage.size
    for i in range(xSize):
        for j in range(ySize):
            pix[i, j] = vanishNoisesFromPixel(pix[i, j])

    pixelValues = [[0 for x in range(ySize)] for y in range(xSize)]
    for i in range(xSize):
        for j in range(ySize):
            pixelValues[i][j] = converToBinaryValue(pix[i, j])
    addToScreen(drawingImage)

    for i in range(xSize):
        for j in range(ySize):
            if i == 0 or j == 0 or i == xSize - 1 or j == ySize - 1:
                pixelValues[i][j] = 0


    global labelValues
    labelValues = [[0 for x in range(ySize)] for y in range(xSize)]
    for i in range(xSize):
        for j in range(ySize):
            labelValues[i][j] = 0

    labelCounter = 2
    for i in range(1, xSize - 1):
        for j in range(1, ySize - 1):
            if pixelValues[i][j] == 1:
                if pixelValues[i - 1][j] == 1 and pixelValues[i][j - 1] == 1:
                    if labelValues[i - 1][j] == labelValues[i][j - 1]:
                        labelValues[i][j] = labelValues[i][j - 1]
                    else:
                        labelValues[i][j] = labelValues[i - 1][j]
                        for t in range(1, xSize):
                            for k in range(1, ySize):
                                if labelValues[t][k] == labelValues[i][j - 1]:
                                    labelValues[t][k] = labelValues[i - 1][j]
                                if t == i and k == j:
                                    break
                            if t == i and k == j:
                                break
                elif pixelValues[i - 1][j] == 1 or pixelValues[i][j - 1] == 1:
                    if pixelValues[i - 1][j] == 1:
                        labelValues[i][j] = labelValues[i - 1][j]
                    else:
                        labelValues[i][j] = labelValues[i][j - 1]
                else:
                    labelValues[i][j] = labelCounter
                    labelCounter += 1
            else:
                labelValues[i][j] = 1



def addToScreen( Img ):

    render = ImageTk.PhotoImage(Img)
    img = Label (root, image =render)
    img.image=render
    img.place(x=250,y=100)
    img.bind("<Button-1>",printcoords)


def printcoords(event):

    print (event.x,event.y)
    paintReagion(event.x,event.y)



def paintReagion(x,y):

    xSize , ySize =drawingImage.size
    global labelValues
    if labelValues[x][y]!=1:
        for t in range(1, xSize):
            for k in range(1, ySize):
                 if labelValues[x][y] == labelValues[t][k]:
                    global choosenColor
                    pix[t, k] = choosenColor
                    drawingImage.putpixel((t, k), choosenColor)

    render = ImageTk.PhotoImage(drawingImage)
    img = Label (root,image=render)
    img.image=render
    img.place(x=250,y=100)
    img.bind("<Button-1>",printcoords)



def converToBinaryValue(rgbValues):

    if len (rgbValues)==4:
        r,g,b,f=rgbValues
    else:
        r,g,b=rgbValues
    average=(r+g+b)/3
    if average==255 :
        return 1
    return 0


def vanishNoisesFromPixel(  rgbValues ):

    if len(rgbValues) == 4:
        r, g, b, f = rgbValues
    else:
        r, g, b = rgbValues
    average = (r + g + b) / 3
    if average > 200:
        return 255, 255, 255
    return 0, 0, 0


def drawing():
    global image1
    width = 400
    height = 500
    white = (255, 255, 255)




    def paint(event):

        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        canvas.create_oval(x1, y1, x2, y2, fill="black", width=5)
        draw.line([x1, y1, x2, y2], fill="black", width=5)

    root = Tk()


    canvas = Canvas(root, width=width, height=height, bg='white')
    canvas.pack()

    image1 = PIL.Image.new("RGB", (width, height), white)
    draw = ImageDraw.Draw(image1)



    canvas.pack(expand=YES, fill=BOTH)
    canvas.bind("<B1-Motion>", paint)



def saveDrawing():

    filename = "D:\\proje\\savedrawing.png"
    image1.save(filename)

if __name__=='__main__':
    main()