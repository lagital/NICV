from tkinter import *
from PIL import Image
import templateSkeletize2 as sk

def binary(img):
    bImg=[]
    for i in range(img.size[0]):
        tmp=[]
        for j in range(img.size[1]):
            t=img.getpixel((i,j))
            p=t[0]*0.3+t[1]*0.59+t[2]*0.11
            if p>128:
                p=1
            else:
                p=0
            tmp.append(p)
        bImg.append(tmp)
    return bImg
    
def __removeDouble(x,y):
    z=[]
    for i in x:
        c=True
        for j in y:
            if i==j:
                c=False
        if c:
            z.append(i)
    for i in y:
        c=True
        for j in x:
            if i==j:
                c=False
        if c:
            z.append(i)
    return z

def delNoisePoint(r):
    tmp=[]
    tmp2=[]
    for i in r[1]:
        x=range(i[0]-5,i[0]+5)
        y=range(i[1]-5,i[1]+5)
        for j in r[0]:
            if j[0] in x and j[1] in y: 
                tmp.append(i)
                tmp2.append(j)
    return (__removeDouble(r[0],tmp2),__removeDouble(r[1],tmp))
    
def matchingPoint(r, v):
    all=0
    match=0
    for i in v[0]:
        x=range(i[0]-15,i[0]+15)
        y=range(i[1]-15,i[1]+15)
        all+=1
        for j in r[0]:
            if j[0] in x and j[1] in y: 
                match+=1
                break
    for i in v[1]:
        x=range(i[0]-15,i[0]+15)
        y=range(i[1]-15,i[1]+15)
        all+=1
        for j in r[1]:
            if j[0] in x and j[1] in y:
                match+=1
                break

    return (match,all)   
        

def checkThisPoint(img, x, y):
    c=0
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if img[i][j]==0:
                c+=1
    return c-1

def findCheckPoint(img):
    x=len(img)
    y=len(img[0])
    branchPoint=[]
    endPoint=[]
    for i in range(x):
        for j in range(y):
            if img[i][j]==0:
                t=checkThisPoint(img, i, j)
                if t==1:
                    endPoint.append((i,j))
                if t==3:
                    branchPoint.append((i,j))
    return (branchPoint, endPoint)
 
def checkFinger(r, v):
    reference=Image.open(r)

    ref=binary(reference)     #как оно работает   
        
    sk.tmpDelete(ref)
    rp=findCheckPoint(ref)
    rp=delNoisePoint(rp)

    verf=Image.open(v)

    ver=binary(verf)

    sk.tmpDelete(ver)
    vp=findCheckPoint(ver)
    vp=delNoisePoint(vp)

    res=matchingPoint(rp,vp)
    r=(res[0]/(res[1]*1.))*100

    
    root=Tk()
    w=len(ver)
    h=len(ver[0])
    C=Canvas(root, width=w*2, height=h)

    for i in range(w):
        for j in range(h):
            if ref[i][j]==0:
                C.create_line([(i,j),(i+1,j+1)])
            if ver[i][j]==0:
                C.create_line([(i+w+1,j+1),(i+w,j)])
    for i in rp[0]:
        C.create_oval([(i[0]-3,i[1]-3),(i[0]+3,i[1]+3)],outline="#ff0000")
    for i in rp[1]:
        C.create_rectangle([(i[0]-3,i[1]-3),(i[0]+3,i[1]+3)],outline="#0000ff")    
    for i in vp[0]:
        C.create_oval([(i[0]-3+w,i[1]-3),(i[0]+3+w,i[1]+3)],outline="#ff0000")
    for i in vp[1]:
        C.create_rectangle([(i[0]-3+w,i[1]-3),(i[0]+3+w,i[1]+3)],outline="#0000ff")

    C.create_text((w, h*0.95), fill="#009900", text=str(r)+"%",font='Arial,72')

    C.pack()
    root.mainloop()
