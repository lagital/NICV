from Tkinter import *
import tkFileDialog
import correlate
import points

def start():    
    '''if F.get()=='C':
        window=Toplevel(root)
        window.title("Fingerprint Check")
        r=correlate.checkFinger(inPut.get(),outPut.get())
        Label(window, text="Match: "+str(r*100)+"%").pack()
    if F.get()=='P':'''
    points.checkFinger(inPut.get(),outPut.get())

def openRef(event):
    options={}
    options['defaultextension'] = ''
    options['filetypes'] = [('text files', '.txt')]
    options['initialdir'] = 'C:\\'
    options['parent'] = root
    options['title'] = 'Open Input File'
    
    input=tkFileDialog.askopenfilename()
    if input:
        inPut.set(input)

def openVer(event):
    options={}
    options['defaultextension'] = ''
    options['filetypes'] = [('text files', '.txt')]
    options['initialdir'] = 'C:\\'
    options['parent'] = root
    options['title'] = 'Open Output File'
    
    output=tkFileDialog.askopenfilename()  
    if output:
        outPut.set(output)

global root
root=Tk()
root.title("Defender")

global inPut
global outPut
global autoGraph
inPut=StringVar()
inPut.set('')
outPut=StringVar()
outPut.set('')
autoGraph=StringVar()
autoGraph.set('')

inEntry=Entry(root, textvariable=inPut)
outEntry=Entry(root, textvariable=outPut)

getInFile=Button(root, text='Open Reference')
getOutFile=Button(root, text='Open Verificable')

getInFile.bind('<1>',openRef)
getOutFile.bind('<1>',openVer)

''''
global F
F=StringVar()
F.set('C')
Cor=Radiobutton(root,text='Correlate', variable=F, value='C')
Pnt=Radiobutton(root,text='Control Points', variable=F, value='P')
'''
sign=Button(root, text='Start', command=start)

inEntry.grid(row=0,column=0)
outEntry.grid(row=1,column=0)

getInFile.grid(row=0,column=1)
getOutFile.grid(row=1,column=1)

'''Cor.grid(row=2,column=0)
Pnt.grid(row=2,column=1)'''
sign.grid(row=3,column=1)


root.mainloop()
