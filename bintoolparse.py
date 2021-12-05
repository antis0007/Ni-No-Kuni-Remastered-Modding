import tkinter
import os
from tkinter import filedialog
from tkinter import *
import codecs
import binascii
import struct
import sys
import time

def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])[2:]

root = Tk()
root.title("Simple Ni No Kuni .bin modding tool")

filename = ""
ext = ""

def save():
    data_final_name = (filename+ "_final"+ ext)
    data_final = open((data_final_name), "w") #full write to reset
    data_final.write("")
    data_final.close()
    data_final = open((data_final_name), "ab")#Now open in append mode, to add new data to mod version
    for i in range(0, len(data_mod)):
        #newdatatr = str(data_mod[i]+'\n')
        try:
            data_final.write(binascii.unhexlify(data_mod[i]))
        except:
            binascii.unhexlify("0000000000000000")
    print("Saved")
def load():
    global filename
    global data
    global ext
    global data_mod
    global data_mod_tkvar
    global var_mod
    global var_mod_tkvar
    global varpos
    global varnames
    
    filename =  filedialog.askopenfilename(title = "Select .bin file",filetypes = (("Binary File","*.bin"),("All files","*.*")))
    data = list(open(filename,"rb"))
    ext = os.path.splitext(filename)[1]
    filename = os.path.splitext(filename)[0]

    print(filename)
    print(ext)
    
    data_mod = codecs.open((filename+ext), "rb").read()
    data_mod_list = []
    bcount = 0    
    for b in range(0, len(data_mod)//8):
        newb = (data_mod)[b*8:b*8+8].hex()
        #newb = bytearray(newb)
        data_mod_list.append(newb)
        bcount+=1
        
    #print(data_mod_list)
    
    varpos = []
    offsets = []
    varnames= []
    fbound = 0
    for i in range(0, len(data_mod_list)):
        #print((data_mod_list[i])[0:8])
        if (data_mod_list[i])[0:8]=="ad549b59":
            values = (str(int(((data_mod_list[i])[8:12]),16)))
            #print("V: "+ values)
            varpos.append(i)
            #print("off: "+(data_mod_list[i+1]))
            b = (data_mod_list[i+1])[0:4]
            b = binascii.unhexlify(b)
            b =int.from_bytes(b, byteorder=sys.byteorder)
            offsets.append(b)
            
        if data_mod_list[i] == "ffffffffffffffff":
            fbound = i
            break
            
    names= ("".join(data_mod_list[fbound:bcount]))[16:]
    #print(names)
    
    tempitem = ""

    for x in range(0, len(names)-2, 2):
        b = names[x:(x+2)]
        b= "".join(map(str,b))        
        try:
            b = hex(int(b, 16))[2:]
            b = binascii.unhexlify(b).decode('utf-8')
        except:
            b = " "          
        tempitem+=b
        
    names_str = tempitem
    for i in range(0, len(offsets)-1):

        #print("SET NEW")
        #print(offsets[i])
        #print(offsets[i+1])
        varnames.append(names_str[(offsets[i]):(offsets[i+1])])
    data_mod=data_mod_list
    data_mod_tkvar.set(data_mod)
    
    var_mod=(varnames)
    var_mod_tkvar.set(var_mod)
    

varpos = []
varnames = []
frame = Frame(root)
frame.pack()
mainmenu = Menu(frame)
mainmenu.add_command(label = "Save", command= save)
mainmenu.add_command(label = "Load", command= load)
mainmenu.add_command(label = "Exit", command= root.destroy)
 
root.config(menu = mainmenu)

data_mod_name = (filename+ "_mod"+ ext)
data_mod = open((data_mod_name), "w") #full write to reset
data_mod.write("")
data_mod.close()
data_mod = open((data_mod_name), "ab")#Now open in append mode, to add new data to mod version

#GUI:

root.geometry("1280x720")



def delete(event):
    selected = data_mod_gui.curselection()
    for i in selected[::-1]:
        data_mod.pop(i)        
    data_mod_tkvar.set(data_mod)
    #deselection:
    #data_mod_gui.selection_clear(0, tkinter.END)

def select(event):
    i = data_mod_gui.curselection()[0]
    item_hex.set(data_mod[i])
    item_numbers.set(str(int((data_mod[i])[0:2],16)))
    tempitem = ""
    #print("START")
    for x in range(0, len(data_mod[i]), 2):
        b = (data_mod[i])[x:(x+2)]
        b= "".join(map(str,b))
        
        
        #print(b)
        
        try:
            b = hex(int(b, 16))[2:]
            b = binascii.unhexlify(b).decode('utf-8')
        except:
            b = " "
            
        tempitem+=b
    item_letters.set(tempitem)
    
def selectvar(event):
    global var_mod_gui
    global data_mod_gui
    global varpos
    global selec
    
    selec = var_mod_gui.curselection()[0]
    #varpos[i]
    #data_mod_gui.see(varpos[selec])
    
def seeval():
    global var_mod_gui
    global data_mod_gui
    global varpos
    global selec
    
    b = (data_mod[varpos[selec]])[8:10]
    b = binascii.unhexlify(b)
    b =int.from_bytes(b, byteorder=sys.byteorder)
    valnum = b
    
    print(valnum)
    data_mod_gui.selection_set(varpos[selec]+3,varpos[selec]+(valnum))
    data_mod_gui.see(varpos[selec])
    

def update_hex(event):
    i = data_mod_gui.curselection()[0]
    new = item_hex.get()        
    if new.isdigit():
        new = int(new)
        new = hex(new)[2:]
        
    elif new.isdecimal():
        new = float(new)
        new = float_to_hex(new)
        
    data_mod.pop(i)
    data_mod.insert(i,new)
    data_mod_tkvar.set(data_mod)
    
def update_numbers(event):
    i = data_mod_gui.curselection()[0]
    new = item_numbers.get()
    new = hex(int(new))[2:]
    new = new.ljust(16,"0")
    
    
    data_mod.pop(i)
    data_mod.insert(i,new)
    data_mod_tkvar.set(data_mod)
    
def update_letters(event):
    i = data_mod_gui.curselection()[0]
    new = item_letters.get()
    new = hex(a)
    new = binascii.hexlify(new)
    print("UPDATE L")
    print(new)
    
    data_mod.pop(i)
    data_mod.insert(i,new)
    data_mod_tkvar.set(data_mod)   
           
def up(event):
    selected = data_mod_gui.curselection()[0]
    selected += -1
    data_mod_gui.select_set(selected)
    
def down(event):
    selected = data_mod_gui.curselection()[0]
    selected += 1
    data_mod_gui.select_set(selected)
    
selec = 0
h = Scrollbar(root, orient = 'horizontal')
h.pack(side = BOTTOM, fill = X)


v = Scrollbar(root)
v.pack(side = RIGHT, fill = Y)

modcontainer = Frame(root)
data_mod = []
data_mod_tkvar = tkinter.StringVar(value=data_mod)#create a tkinter stringvar for modifications
data_mod_gui = Listbox(modcontainer, listvariable=data_mod_tkvar, xscrollcommand = h.set, yscrollcommand = v.set, selectmode='extended')
data_mod_gui.bind('<<ListboxSelect>>', select)
data_mod_gui.pack(side="left",fill="both", expand=True)

var_mod = []
var_mod_tkvar = tkinter.StringVar(value=data_mod)#create a tkinter stringvar for modifications
var_mod_gui = Listbox(modcontainer, listvariable=var_mod_tkvar, xscrollcommand = h.set, yscrollcommand = v.set, selectmode='extended')
var_mod_gui.bind('<<ListboxSelect>>', selectvar)
var_mod_gui.pack(side="left",fill="both", expand=True)

modcontainer.pack(side="left",fill="both", expand=True)

#for i in range(0, len(data_mod)):
    #data_mod_gui.insert(END,data_mod[i])




root.iconify() #Unclick and reclick, scuffed solution but it works!
root.deiconify()

data_mod_gui.bind('<Delete>', delete)
data_mod_gui.bind('<Up>', up)
data_mod_gui.bind('<Down>', down)

h.config(command=data_mod_gui.xview)
v.config(command=data_mod_gui.yview)

character_list = ["None"]
button_list = []
character_list_tkvar = tkinter.StringVar()#create a tkinter stringvar for modifications
character_list_tkvar.set(character_list[0])

modframe = Frame(root)

item_numbers = tkinter.StringVar()
entry_numbers = tkinter.Entry(modframe, textvariable=item_numbers, width=20)
entry_numbers.pack(side="top",fill="x", expand=True)
entry_numbers.bind('<Return>', update_numbers)

item_letters = tkinter.StringVar()
entry_letters = tkinter.Entry(modframe, textvariable=item_letters, width=20)
entry_letters.pack(side="top",fill="x", expand=True)
entry_letters.bind('<Return>', update_letters)

item_hex = tkinter.StringVar()
entry_hex = tkinter.Entry(modframe, textvariable=item_hex, width=20)
entry_hex.pack(side="top",fill="x", expand=True)
entry_hex.bind('<Return>', update_hex)

seeval = tkinter.Button(modframe, text ="See values", command = seeval)
seeval.pack(side="bottom",fill="x", expand=True)

modframe.pack(side="right",fill="x", expand=True)

root.mainloop() 
    
