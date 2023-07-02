""" This module creates a view class. """
from tkinter import *
from tkinter import ttk,font
from tkinter.messagebox import showinfo
import customtkinter as ctk
from myapp.helpers import myfunc as func
from PIL import Image, ImageTk
import time


class WinView(ctk.CTk): 	
	""" Main application window class """

	projectname = None
	projectfile = None	
	active_button = None
	project_class_before = None
	project_class_after = None
	active_class = None
	timer_id = None
	animation_canvas = None

	def __init__(self):
		""" initialize the window view class """
		
		super(WinView, self).__init__()		
		self._set_appearance_mode("light")
		ctk.set_default_color_theme("green")		  
		#w, h = 560, 400
		w, h = 860, 660					
		self.geometry("{}x{}".format(w,h))
		self.minsize(w-300,h-260)
		self.maxsize(w,h)		
		self.w = w
		self.h = h 
		self.title('PROBITAN - An Equipment Process Reliability Analytical Tool.')
		self.top_level_window = None				

	def base_view(self):
		""" creates the project entry view """
		
		main_bg = func.create_image_obj('myapp/appfiles/images/bg/1.PNG',(self.w, self.h))
		btn_bg_image = func.create_image_obj('myapp/appfiles/images/bg/12.PNG',(self.h/40, self.h/40))
		
		#Labels
		bg_lab1 = ctk.CTkLabel(self, text="",bg_color="#495068",fg_color="#495068",height=self.h, width=self.w).place(x=0, y=0)				

		#buttons 
		start_btn = ctk.CTkButton(self, text="New Project",bg_color="#495068",fg_color="#fffada",text_color="#495068", width=self.w/11, height=self.h/20, command=self.create_new_project)
		select_btn = ctk.CTkButton(self, text="Select Project",bg_color="#495068",fg_color="#fffada",text_color="#495068", width=self.w/11, height=self.h/20, command=self.select_project)
		#start_btn.pack(relx=self.w/3, rely=self.h/2, expand=True)
		#self.update()
		#select_btn.pack(relx=start_btn.winfo_x()+120, rely=start_btn.winfo_y(), expand=True)
		start_btn.place(x=self.w/3,y=self.h/2)
		self.update()		
		select_btn.place(x=start_btn.winfo_x()+120,y=start_btn.winfo_y())
	
	def create_label(self,**kwargs):
		""" This function creates a label when given any number of key-word args """
		
		text = kwargs["text"] if "text" in kwargs else ""			
		image = kwargs["image"] if "image" in kwargs else ""
		height = kwargs["height"] if "height" in kwargs else 0
		width = kwargs["width"] if "width" in kwargs else 0
		x = kwargs["x"] if "x" in kwargs else 0
		y = kwargs["y"] if "y" in kwargs else 0
		window = kwargs["window"] if "window" in kwargs else self
		bg_color = kwargs["bg_color"] if "bg_color" in kwargs else "blue"
		fg_color = kwargs["fg_color"] if "fg_color" in kwargs else "transparent"
		text_color = kwargs["text_color"] if "text_color" in kwargs else "white"
		font = kwargs["font"] if "font" in kwargs else "Segoe UI"
		font_size = kwargs["font_size"] if "font_size" in kwargs else 12
		font_weight = kwargs["font_weight"] if "font_weight" in kwargs else "normal"
		anchor = kwargs["anchor"] if "anchor" in kwargs else "w"

		lab = ctk.CTkLabel(window, text=text,text_color=text_color,fg_color=fg_color, image = image, bg_color=bg_color, height=height, width=width)
		lab.place(x=x, y=y)			
		lab.cget("font").configure(family=font,size=font_size,weight=font_weight)

		return lab

	def create_button(self,**kwargs):
		""" This function creates a button when given any number of key-word args """
		
		text = kwargs["text"] if "text" in kwargs else ""			
		image = kwargs["image"] if "image" in kwargs else ""
		height = kwargs["height"] if "height" in kwargs else 0
		width = kwargs["width"] if "width" in kwargs else 0
		x = kwargs["x"] if "x" in kwargs else 0
		y = kwargs["y"] if "y" in kwargs else 0
		command = kwargs["command"] if "command" in kwargs else None
		window = kwargs["window"] if "window" in kwargs else self
		bg_color = kwargs["bg_color"] if "bg_color" in kwargs else "#495068"
		fg_color = kwargs["fg_color"] if "fg_color" in kwargs else "#fffada" #"#284B63"
		text_color = kwargs["text_color"] if "text_color" in kwargs else "#495068"
		font = kwargs["font"] if "font" in kwargs else "Segoe UI"
		font_size = kwargs["font_size"] if "font_size" in kwargs else 12
		font_weight = kwargs["font_weight"] if "font_weight" in kwargs else "normal"

		butt = ctk.CTkButton(window, text=text, width=width, bg_color=bg_color, height=height,
								fg_color=fg_color,text_color=text_color, 
								border_spacing=0, command=command)
		butt.place(x=x,y=y)
				
		return butt	

	def create_display(self,**kwargs):
		""" This function creates a button when given any number of key-word args """
		
		text = kwargs["text"] if "text" in kwargs else ""
		title = kwargs["title"] if "title" in kwargs else ""
		text_position = kwargs["text_position"] if "text_position" in kwargs else "3.0"			
		image = kwargs["image"] if "image" in kwargs else ""
		height = kwargs["height"] if "height" in kwargs else self.h-210
		width = kwargs["width"] if "width" in kwargs else self.w-30 
		x = kwargs["x"] if "x" in kwargs else 15
		y = kwargs["y"] if "y" in kwargs else self.h/4
		command = kwargs["command"] if "command" in kwargs else None
		window = kwargs["window"] if "window" in kwargs else self
		bg_color = kwargs["bg_color"] if "bg_color" in kwargs else "#E5E5E5"
		fg_color = kwargs["fg_color"] if "fg_color" in kwargs else "white"
		text_color = kwargs["text_color"] if "text_color" in kwargs else "white"
		font = kwargs["font"] if "font" in kwargs else "Segoe UI"
		font_size = kwargs["font_size"] if "font_size" in kwargs else 12
		font_weight = kwargs["font_weight"] if "font_weight" in kwargs else "normal"

		txt = ctk.CTkTextbox(window)
		txt.insert("0.0",title)		
		txt.insert(text_position,"\n\n"+text)
		txt.configure(width=width, bg_color=bg_color, height=height,fg_color=fg_color,text_color=text_color, 
								border_spacing=5, border_color="black",wrap="word",font=(font,font_size,font_weight))
		txt.configure(state="disabled")
		txt.place(x=x,y=y)
		

		return txt

	def create_form_window_after(self):
		"""Creates a new toplevel window for user to choose where to upload result file from"""

		if self.top_level_window is None or not self.top_level_window.winfo_exists():
			title = "Choose Result File Destination"
			self.top_level_window = obj = TopLevel(self,title)
			self.create_button(window=self.top_level_window,command=self.upload_result_file,text="New File",bg_color="#E5E5E5",height=30,width=80, fg_color= "#495068",text_color="#fffada",x=(obj.w/2)-85,y=180)
			self.create_button(window=self.top_level_window,command=self.select_result_file,text="Existing File",bg_color="#E5E5E5",fg_color= "#495068",text_color="#fffada", height=30,width=80,x=(obj.w/2)+5,y=180)	

		else:
			self.top_level_window.focus()
			
		return

	def select_result_file(self):
		"""This will trigger file selection from program directory"""

		projectname, projectfile = func.select_file("myapp/documents/after/",2)
		if projectname == self.projectname:
			self.process_project_file(2)
			self.top_level_window.destroy()
		else:
			func.display_msg("Selected file does not match the before project file!")	
		return		

	def upload_result_file(self):
		"""This will trigger file upload from other direcories in the user computer device"""

		self.projectname, self.projectfile = func.upload_file(2,self.projectname)
		self.process_project_file(2)
		self.top_level_window.destroy()
		return

	def start_animation(self):
		"""This method creates animation canvas"""
		imagelist = ["dog001.gif","dog002.gif","dog003.gif",
             "dog004.gif","dog005.gif","dog006.gif","dog007.gif"]

		# extract width and height info
		photo = PhotoImage(file=imagelist[0])
		width = photo.width()
		height = photo.height()
		canvas = Canvas(width=width, height=height)
		canvas.place(y=(self.h/2)+40,x=(self.w/3)+40)
		self.animation_canvas = canvas

		# create a list of image objects
		giflist = []
		for imagefile in imagelist:
		    photo = PhotoImage(file=imagefile)
		    giflist.append(photo)

		def start_loading(n=0):
			"""creates image on the canvas"""
			gif = giflist[n%len(giflist)]        
			canvas.create_image(width/2.0, height/2.0, image=gif)
			self.timer_id = self.after(200, start_loading, n+1)	#call this function every 10second
		start_loading()		

	def stop_animation(self):
		"""This method stops the animation by deleting the animation canvas"""

		if self.timer_id and self.animation_canvas:
			print("we are here")
			self.after_cancel(self.timer_id)
			self.animation_canvas.delete(ALL)
			self.animation_canvas.destroy()
			self.timer_id = None 

	 				
			 
class TopLevel(ctk.CTkToplevel):
	"""This is the TopLevel class for creating windows outside the main window"""

	def __init__(self, main,title):
		super(TopLevel, self).__init__(main)
		self.title(title)
		self.w,self.h = 600,400
		self.geometry("{}x{}".format(self.w,self.h))
		
		self.grab_set()


 			
 			 	