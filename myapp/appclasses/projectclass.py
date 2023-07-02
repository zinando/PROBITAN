"""This is the PROJECT class module"""
import os
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
import customtkinter as ctk
from myapp.helpers import myfunc as func

class PROJECT:
	"""This is the project class that creates an instance of a file mode, either before or after file"""

	project_name = None

	def __init__(self,name,file,processed_data,event_types,cil_locations,date_format,location_processed_data,monthly_events):
		"""This initializes the class instance with attributes necessary to process the file"""
		self.name = name
		self.file = file
		self.processed_data = processed_data
		self.event_types = event_types
		self.cil_locations = cil_locations
		self.date_format = date_format		
		self.location_processed_data = location_processed_data #computs downtime based on cil location
		self.monthly_events = monthly_events 
		