"""This is the main application file. We import all modules/functions necessary to execute commands into this file and then make them to perform the required tasks.
   First we create the application window (Tikinter).
"""
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
import customtkinter as ctk
from myapp.helpers import myfunc as func
from PIL import Image, ImageTk
from myapp.appclasses.views import WinView,TopLevel 
from myapp.appclasses.fileclass import FILEHANDLER
from myapp.appclasses.graphclass import MYGRAPH
from myapp.appclasses.projectclass import PROJECT

class Probitan(WinView):
	""" Class for managing app button click actions. This class inherits from the app window view class (WinView) """
	processed_data = None
	event_types = None
	cil_locations = None
	date_format = None
	current_display = None
	location_processed_data = None #computs downtime based on cil location
	monthly_events = None
	
 	
	def __init__(self):
		""" initializes the Probitan class, and calls on the base_view method which creates the project entry point """
		super(Probitan, self).__init__()
		self.base_view()
 		
	def toggle_file_mode(self,projectclass):
		"""Toggles class instance attributes between before or after file"""
		if self.active_class != projectclass:
			self.active_class = projectclass
			self.initialize_project_variables("activate project")

	def create_new_project(self):
		""" Calls the upload_file function to upload a new project file and to process it
			Calls the create_work_view to create the main work_view
		"""
		self.initialize_project_variables()		
		self.projectname, self.projectfile = func.upload_file(1)
		if self.top_level_window is not None:
			self.top_level_window.destroy()
		self.process_project_file(1)

	def select_project(self):
		""" Calls the upload_file function to upload a new project file and to process it
			Calls the create_work_view to create the main work_view
		"""
		#self.start_animation()
		self.initialize_project_variables()		
		self.projectname, self.projectfile = func.select_file("myapp/documents/before/",1)
		#self.stop_animation()

		if self.top_level_window is not None:
			self.top_level_window.destroy()
		
		self.process_project_file(1)
			

	def process_project_file(self,folder_id):
		"""Processes project file after upload/selection"""

		if self.projectname is not None:			
			#process the file data and display time span of events			
			info = FILEHANDLER(folder_id)
			full_file_path = "{}{}".format(info.file_path,self.projectfile)

			#read the file content 
			result1 = info.read_file(full_file_path)
			event_types, cil_locations = info.get_list_of_event_types(result1)

			#get the date format from the content
			datelist = [x["start_date"] for x in result1]
			date_format = func.get_date_format(datelist)			

			#group events into the months in which they occured
			result2 = info.get_event_duration_in_months(result1,date_format)
			result3 = info.group_events_by_month(result1,result2,date_format)
			monthly_events = result3

			#get the time for each event by month
			result4 = info.compute_time_for_monthly_events(result3)
			processed_data = result4

			#get processed data based on cil location
			result5 = info.process_cil_location_data(result3,cil_locations)
			location_processed_data = result5

			list_items = list(result2.items())
			first_key,first_value = list_items[0]
			last_key,last_value = list_items[-1]

			text =  "Analysing data from {} to {}.".format(first_value,last_value)
			self.instantiate_project(folder_id,self.projectname,self.projectfile,processed_data,event_types,cil_locations,date_format,location_processed_data,monthly_events)
			self.create_work_view(text)

	def instantiate_project(self,folder_id,name,file,processed_data,event_types,cil_locations,date_format,location_processed_data,monthly_events):
		"""Creates instance of the PROJECT class"""
		if folder_id == 1:
			self.project_class_before = PROJECT(name,file,processed_data,event_types,
					cil_locations,date_format,location_processed_data,monthly_events
				)
			self.active_class = self.project_class_before
			self.initialize_project_variables("activate project")
		elif folder_id == 2:
			self.project_class_after = PROJECT(name,file,processed_data,event_types,
					cil_locations,date_format,location_processed_data,monthly_events
				)
			self.active_class = self.project_class_after
			self.initialize_project_variables("activate project")	

	def create_work_view(self,text=""):
		""" This creates the working window where analytical graphs are being generated	"""		
		
		#background image objects
		view_bg = func.create_image_obj('myapp/appfiles/images/bg/12.PNG',(self.w, self.h))
		menu_bg = func.create_image_obj('myapp/appfiles/images/bg/12.PNG',(self.w, 40))
		menu_title_bg = func.create_image_obj('myapp/appfiles/images/bg/12.PNG',((self.w/2)-80, 20))
		divi_bg = func.create_image_obj('myapp/appfiles/images/bg/12.PNG',(3, 115))
		bg_1 = func.create_image_obj('myapp/appfiles/images/btn/1.PNG',(40, 20))

		#labels
		bg_lab2 = self.create_label(text="", image = view_bg, height=self.h, width=self.w)
		footer = self.create_label(text="This project is submitted to the department of Mechanical Engineering, University of Ife, Nigeria",
				height=40, width=self.w, y=self.h-40,fg_color= "#495068",text_color="#fffada", bg_color= "#495068",font_size=14,font_weight="bold")
		menu_bar = self.create_label(height=40, width=self.w,image=menu_bg)
		sub_menu_bar = self.create_label(height=115,y=40, width=self.w, bg_color= "#D9D9D9",fg_color= "#495068")
		sub_menu_bar_title1 = self.create_label(text="BEFORE",height=20,y=43,x=40, width=(self.w/2)-80, image=menu_title_bg,text_color="#495068")
		sub_menu_bar_title2 = self.create_label(text="AFTER",height=20,y=43,x=(self.w/2)+40, width=(self.w/2)-80, image=menu_title_bg,text_color="#495068")
		title_divider = self.create_label(height=115,y=40,x=(self.w/2)-1.5, width=3, image=divi_bg)
		display = self.create_label(font_size=11,height=30,y=5,x=300, width=150, text="Processing: {}\n{}".format(self.projectname,text),text_color="#fffada",fg_color="#495068",bg_color="#495068")


		#Buttons: Top Bar menu
		result_file = self.create_button(text="Load Result File", bg_color="#E5E5E5", command=self.create_form_window_after,
				height=20, width=40, y=5,x=5,fg_color= "#495068",text_color="#fffada")
		new_project_file = self.create_button(text="New Project", bg_color="#E5E5E5", command=self.create_form_window,
				height=20, width=40, y=5,x=130,fg_color= "#495068",text_color="#fffada")

		##Buttons: Sub-menu

		#uptime and dt
		uptm_dwntm1 = self.create_button(command=self.plot_uptime_and_downtime,
				height=20, width=70, y=80,x=10, text = "Uptime & DT")
		uptm_dwntm2 = self.create_button(command=self.plot_uptime_and_downtime_after,
				height=20, width=70, y=80,x=(self.w/2)+10, text = "Uptime & DT")
		#average planned downtime
		pl_dwntm1 = self.create_button(command=self.plot_average_planned_downtime_events,
				height=20, width=70, y=80,x=100, text = "Planned DT")
		pl_dwntm2 = self.create_button(command=self.plot_average_planned_downtime_events_after,
				height=20, width=70, y=80,x=(self.w/2)+100, text = "Planned DT")		
		#average cil 
		cil1 = self.create_button(command=self.plot_average_cil_planned_downtime_events,
				height=20, width=70, y=80,x=185, text = "Av. CIL")
		cil2 = self.create_button(command=self.plot_average_cil_planned_downtime_events_after,
				height=20, width=70,y=80,x=(self.w/2)+185,text = "Av. CIL") #each char is 8 by width 

		#planned and unplanned dt
		pl_updt1 = self.create_button(command=self.plot_planned_and_unplanned_downtime,
				height=20, width=70,y=80+20+10+5,x=10,text = "Planned & UPDT")
		pl_updt2 = self.create_button(command=self.plot_planned_and_unplanned_downtime_after,
				height=20, width=70, y=80+20+10+5,x=(self.w/2)+10,text = "Planned & UPDT")
		#cil per month
		cilpm1 = self.create_button(command=self.plot_cil_per_month,
				height=20, width=70, y=80+20+10+5,x=127, text = "CIL/month")
		cilpm2 = self.create_button(command=self.plot_cil_per_month_after,
				height=20, width=70, y=80+20+10+5,x=(self.w/2)+127, text = "CIL/month")

		#list event
		eventlist1 = self.create_button(command=self.create_events_list,
				height=20, width=70, y=115,x=127+90, text = "List events")
		eventlist2 = self.create_button(command=self.create_events_list_after,
				height=20, width=70, y=115,x=(self.w/2)+127+90, text = "List events")

		#list event locations
		locationlist1 = self.create_button(command=self.create_cil_location,
				height=20, width=70, y=115,x=217+98, text = "CIL Locations")
		locationlist2 = self.create_button(command=self.create_cil_location_after,
				height=20, width=70, y=115,x=(self.w/2)+217+98, text = "CIL Locations")
		
	def initialize_project_variables(self,status=""):
		""" This function initializes the following variables to default values when the user decides to start a new
			project after working on a prevoious one without reopening the app
		"""
		if status == "activate project":
			instance = self.active_class

			self.processed_data = instance.processed_data
			self.event_types = instance.event_types
			self.cil_locations = instance.cil_locations
			self.date_format = instance.date_format			
			self.location_processed_data = instance.location_processed_data
			self.monthly_events = instance.monthly_events
			self.projectname = instance.name
			self.projectfile = instance.file
		else:
			self.projectname = None
			self.projectfile_before = None
			self.active_class = None
			self.project_class_after = None
			self.project_class_before = None

	def create_form_window(self):
		"""Creates a new toplevel window for user to choose where to upload project file from"""

		if self.top_level_window is None or not self.top_level_window.winfo_exists():
			title = "Choose Result File Destination"
			self.top_level_window = obj = TopLevel(self,title)
			self.create_button(window=self.top_level_window,command=self.create_new_project,text="New File",bg_color="#E5E5E5",height=30,width=80, fg_color= "#495068",text_color="#fffada",x=(obj.w/2)-85,y=180)
			self.create_button(window=self.top_level_window,command=self.select_project,text="Existing File",bg_color="#E5E5E5",fg_color= "#495068",text_color="#fffada", height=30,width=80,x=(obj.w/2)+5,y=180)	

		else:
			self.top_level_window.focus()
			
		return		

	def create_events_list(self):
		"""Displays a list of all downtime event types in the project being analyzed"""		
		self.toggle_file_mode(self.project_class_before)
		text = ""
		if self.event_types is not None:
			count = 0

			for x in self.event_types:
				count += 1
				text += "{}. {}\n".format(count,x.title())

		#close the current display
		if self.current_display:
			self.current_display.destroy()

		#create display label
		title = "PLANNED DOWNTIME EVENTS"
		event_display = self.create_display(font_size=16,text=text, text_color="black",title=title)

		self.current_display = event_display
	
	def create_cil_location(self):
		"""Displays a list of all locations the downtime events occured"""
		self.toggle_file_mode(self.project_class_before) 
		text = ""
		if self.cil_locations is not None:
			count = 0

			for x in sorted(self.cil_locations):
				count += 1
				text += "{}. {}\n".format(count,x.title())

		#close the current display
		if self.current_display:
			self.current_display.destroy()

		#create display label
		title = "CIL WORKPOINTS"
		location_display = self.create_display(font_size=16,text=text, text_color="black",title=title)	
		self.current_display = location_display

	def plot_uptime_and_downtime(self):
		"""Plots the graph of uptime and downtime events"""

		self.toggle_file_mode(self.project_class_before)

		plot = MYGRAPH()
		title = "Monthly Uptime And Downtime Graphs"
		plot.generate_uptime_and_downtime_graph(self.processed_data,title)

	def plot_planned_and_unplanned_downtime(self):
		"""Plots the graph of planned and unplanned downtime events"""

		self.toggle_file_mode(self.project_class_before)

		plot = MYGRAPH()
		title = "Monthly Planned And Unplanned Downtme Graphs"
		plot.generate_planned_and_unplanned_dt_graph(self.processed_data,title)

	def plot_average_planned_downtime_events(self):
		"""Plots the graph of average planned downtime for all the eventtypes"""

		self.toggle_file_mode(self.project_class_before)

		plot = MYGRAPH()
		title = "Average Planned Downtime Per Event"
		plot.generate_average_dt_graph(self.processed_data,self.event_types,title)

	def plot_average_cil_planned_downtime_events(self):
		"""Plots the graph of average cil downtime """

		self.toggle_file_mode(self.project_class_before)

		plot = MYGRAPH()
		title = "Average CIL Downtime Per Workpoint"
		plot.generate_average_dt_graph(self.location_processed_data,self.cil_locations,title)

	def plot_cil_per_month(self):
		"""Plots the graph monthly cil downtime"""

		self.toggle_file_mode(self.project_class_before)

		#process the data to be used
		info = FILEHANDLER()
		processed_data = info.process_monthly_event_data(self.monthly_events,"type","cil")

		plot = MYGRAPH()
		title = "Monthly CIL Downtime Graph"
		plot.generate_monthly_event_graph(processed_data,"cil",title)		 			

	def create_events_list_after(self):
		"""Displays a list of all downtime event types in the project being analyzed"""

		if not self.project_class_after:
			func.display_msg("You have not loaded result file!")			
		else:
			self.toggle_file_mode(self.project_class_after)

			text = ""
			if self.event_types is not None:
				count = 0

				for x in self.event_types:
					count += 1
					text += "{}. {}\n".format(count,x.title())

			#close the current display
			if self.current_display:
				self.current_display.destroy()

			#create display label
			title = "PLANNED DOWNTIME EVENTS"
			event_display = self.create_display(font_size=16,text=text, text_color="black",title=title)

			self.current_display = event_display
	
	def create_cil_location_after(self):
		"""Displays a list of all locations the downtime events occured"""

		if not self.project_class_after:
			func.display_msg("You have not loaded result file!")			
		else:
			self.toggle_file_mode(self.project_class_after) 

			text = ""
			if self.cil_locations is not None:
				count = 0

				for x in sorted(self.cil_locations):
					count += 1
					text += "{}. {}\n".format(count,x.title())

			#close the current display
			if self.current_display:
				self.current_display.destroy()

			#create display label
			title = "CIL WORKPOINTS"
			location_display = self.create_display(font_size=16,text=text, text_color="black",title=title)	
			self.current_display = location_display

	def plot_uptime_and_downtime_after(self):
		"""Plots the graph of uptime and downtime events"""

		if not self.project_class_after:
			func.display_msg("You have not loaded result file!")			
		else:
			self.toggle_file_mode(self.project_class_after)

			plot = MYGRAPH()
			title = "Monthly Uptime And Downtime Graphs"
			plot.generate_uptime_and_downtime_graph(self.processed_data,title)

	def plot_planned_and_unplanned_downtime_after(self):
		"""Plots the graph of planned and unplanned downtime events"""

		if not self.project_class_after:
			func.display_msg("You have not loaded result file!")			
		else:
			self.toggle_file_mode(self.project_class_after)

			plot = MYGRAPH()
			title = "Monthly Planned And Unplanned Downtme Graphs"
			plot.generate_planned_and_unplanned_dt_graph(self.processed_data,title)

	def plot_average_planned_downtime_events_after(self):
		"""Plots the graph of average planned downtime for all the eventtypes"""

		if not self.project_class_after:
			func.display_msg("You have not loaded result file!")			
		else:
			self.toggle_file_mode(self.project_class_after)

			plot = MYGRAPH()
			title = "Average Planned Downtime Per Event"
			plot.generate_average_dt_graph(self.processed_data,self.event_types,title)

	def plot_average_cil_planned_downtime_events_after(self):
		"""Plots the graph of average cil downtime """

		if not self.project_class_after:
			func.display_msg("You have not loaded result file!")			
		else:
			self.toggle_file_mode(self.project_class_after)

			plot = MYGRAPH()
			title = "Average CIL Downtime Per Workpoint"
			plot.generate_average_dt_graph(self.location_processed_data,self.cil_locations,title)

	def plot_cil_per_month_after(self):
		"""Plots the graph monthly cil downtime"""

		if not self.project_class_after:
			func.display_msg("You have not loaded result file!")			
		else:
			self.toggle_file_mode(self.project_class_after)

			#process the data to be used
			info = FILEHANDLER()
			processed_data = info.process_monthly_event_data(self.monthly_events,"type","cil")

			plot = MYGRAPH()
			title = "Monthly CIL Downtime Graph"
			plot.generate_monthly_event_graph(processed_data,"cil",title)		 			




	