"""
Importing tkinter for the usage of gui desigining and required tools
importing os for running commands and directory purposes
"""
from pymsgbox import *
from tkinter import filedialog
from os import system,getcwd
from tkinter import *
import tkinter.font as Tkfonts

gui = Tk()
gui.title("Welcome - Code Editor")
gui.geometry("900x450")

menu_frame = Frame()
menu_frame.pack(fill=X)

text_frame = Frame()
text_frame.pack(fill=BOTH,expand=True)

terminal_frame = Frame()

def newFile():
	textarea.pack(fill=BOTH,expand=True,ipadx=10,ipady=10)
	gui.title("Code Editor - Untitled")
	textarea.delete("1.0",END)

def help():
	confirm(text='', title='', buttons=['OK', 'Cancel'])

def browseFiles():
	filename = filedialog.askopenfilename(initialdir =getcwd(),title = "Select a File",filetypes = (("All files","*"),("Text files", "*.txt*"),("Python files","*.py")))
	label_file_explorer.configure(text=filename)
	global file
	file =  label_file_explorer.cget("text")
	openFile(file)

def openFile(file):
	newFile()
	if file=="":
		newFile()
	else:
		open_file = open(file,"r")
		content = open_file.read()
		textarea.insert("1.0",content)
		dirs = file.split("/")
		last_index = len(dirs)-1
		filename = dirs[last_index]
		gui.title(f"Code Editor -{filename}")

def Save():
	try:
		filename = open(file,"w")
		content = textarea.get("1.0",END)
		filename.write(content)
		filename.close()
	except Exception as e:
		system("touch Untitled")
		filename = open("Untitled","w")
		content = textarea.get("1.0",END)
		filename.write(content)
		filename.close()

def showTerminal():
	terminal_frame.pack(fill=X,expand=True)

menu = Menu(menu_frame,bg="black",activebackground="white"
	,fg="white",activeforeground="green",)

menu_bar = Menu(menu,tearoff=0)
menu_bar.add_command(label="New",command=newFile)
menu_bar.add_command(label="Open",command=browseFiles)
menu_bar.add_command(label="Save",command=Save)
menu_bar.add_command(label="Save As",command=newFile)

fonts = Menu(menu,tearoff=0)
for font in Tkfonts.families():
	fonts.add_command(label=font,command=newFile)

view = Menu(menu,tearoff=0)
view.add_cascade(label="Font-Family",menu=fonts)

view.add_command(label="Background",command=newFile)

help = Menu(menu,tearoff=0)
help.add_command(label="Visit our website",command=help)
help.add_command(label="Help",command=help)

terminal = Menu(menu,tearoff=0)
terminal.add_command(label="New Terminal",command=showTerminal)

menu.add_cascade(label="File", menu=menu_bar)
menu.add_cascade(label="Edit",menu=view)
menu.add_cascade(label="View",menu=view)
menu.add_cascade(label="Terminal",menu=terminal)
menu.add_cascade(label="Settings",menu=menu_bar)
menu.add_cascade(label="Help",menu=help)

textarea = Text(master=text_frame,bg="white",fg="black")

label_file_explorer = Label(gui)
gui.config(menu=menu)

gui.mainloop()
