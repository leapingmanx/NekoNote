from tkinter import filedialog
import tkinter as tk

root = tk.Tk()
main_area = tk.Frame(root)
main_area.pack(side = "top")
root.title("NekoNote")

# functions for the menu options
# file name for reuse
current_file = ""

# file menu functions
def save_as(event = None):
	global current_file
	
	try:
		filename = filedialog.asksaveasfilename(initialdir = "/", title = "Select File", defaultextension = ".txt")
		file_handle = open(filename, "w")
		file_handle.write(str(text_area.get(1.0, "end")))
		file_handle.close()
		
		current_file = filename
		root.title(current_file)
		
	except FileNotFoundError:
		pass
	
def save_file(event = None):
	global current_file
	
	if current_file != "":
		file_handle = open(current_file, "w")
		file_handle.write(str(text_area.get(1.0, "end")))
		file_handle.close()
	else:
		save_as()

root.bind("<Control-s>", save_file)
	
def open_file():
	global current_file
	
	try:
		filename = filedialog.askopenfilename(initialdir = "/", title = "Select File", filetypes = (("Text Files", "*.txt"),))
		file_handle = open(filename, "r")
		new_text = file_handle.readlines()
	
		for line in new_text:
			text_area.insert("end", line)
		root.update()
	
		file_handle.close()
		current_file = filename
		root.title(current_file)
	
	except FileNotFoundError:
		pass
	
def exit(event = None):
	quit()
	
root.bind("<Control-q>", exit)

# edit menu functions
def copy(event = None):
	try:
		root.clipboard_clear()
		root.clipboard_append(text_area.get("sel.first", "sel.last"))
	except tk.TclError:
		pass
	
root.bind("<Control-c>", copy)

def paste(event = None):
	try:
		text_area.delete("sel.first", "sel.last")
		text_area.insert("insert", root.clipboard_get())
	except tk.TclError:
		pass
	
root.bind("<Control-v>", paste)

def cut(event = None):
	try:
		root.clipboard_clear()
		root.clipboard_append(text_area.get("sel.first", "sel.last"))
		text_area.delete("sel.first", "sel.last")
	except tk.TclError:
		pass
	
root.bind("<Control-x>", cut)

# format menu functions
def wrap_none():
	text_area.config(wrap = "none")
	
def wrap_word():
	text_area.config(wrap = "word")
	
def wrap_char():
	text_area.config(wrap = "char")

# menubar set up
menubar = tk.Menu(main_area)

# file menu
file = tk.Menu(menubar)
file.add_command(label = "Save As", command = save_as)
file.add_command(label = "Save", command = save_file, accelerator = "Ctrl+s")
file.add_command(label = "Open", command = open_file)
file.add_command(label = "Exit", command = exit, accelerator = "Ctrl+q")
menubar.add_cascade(label = "File", menu = file)

# edit menu
edit = tk.Menu(menubar)
edit.add_command(label = "Copy", command = copy, accelerator = "Ctrl+c")
edit.add_command(label = "Paste", command = paste, accelerator = "Ctrl+v")
edit.add_command(label = "Cut", command = cut, accelerator = "Ctrl+x")
menubar.add_cascade(label = "Edit", menu = edit)

# format menu
format = tk.Menu(menubar)
format.add_command(label = "Wrap (None)", command = wrap_none)
format.add_command(label = "Wrap (Char)", command = wrap_char)
format.add_command(label = "Wrap (Word)", command = wrap_word)
menubar.add_cascade(label = "Format", menu = format)

# display the menu bar
root.config(menu = menubar)

# text area for the program
text_area = tk.Text(main_area, wrap = "word")
text_area.pack(side = "left", fill = "both", expand = True)
text_scroll = tk.Scrollbar(main_area, orient = "vertical", command = text_area.yview)
text_scroll.pack(side = "right", fill = "y")
text_area["yscrollcommand"] = text_scroll.set

root.mainloop()