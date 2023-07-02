"""This class will handle every file operation after it has been uploaded."""
import os
import shutil
import csv
from myapp.helpers import myfunc as func
from datetime import datetime

class FILEHANDLER:
	
	file_name = None
	file_path = None
	before_path = "myapp/documents/before/"
	after_path = "myapp/documents/after/"
	folder_id = 0

	def __init__(self,folder_id=0):
		"""Initialize the file handler class with folder id"""
		self.folder_id = folder_id

		if self.folder_id == 1:
			self.file_path = self.before_path
		elif self.folder_id == 2:
			self.file_path = self.after_path	
	
	def validate_file(self, filename):
		""" Check that file was selected """ 
		if filename is None or filename == '':
			from myapp.helpers import myfunc
			myfunc.display_msg("No file was selected. Please select a file.")
			return False
		else:
			return True

	def mod_file_name(self,filepath,projectname=None):
		""" Extract the filename from the file path
			Assign a new filename to file based on the number of existing project files 
			Then create an empty file with the new filename 
			Takes the path of the uploaded file as arg 
			Returns the new filepath
		"""
		if projectname:
			filename = filepath.split("/")[-1]					
			new_file_name = "{}_{}".format(projectname,filename)
			new_file_path = "{}{}".format(self.file_path,new_file_name)
		else:	
			filename = filepath.split("/")[-1]
			count = len(os.listdir(self.file_path))		
			new_file_name = "project{}_{}".format(count+1,filename)
			new_file_path = "{}{}".format(self.file_path,new_file_name)

		self.create_project_file(new_file_path)
		self.file_name = new_file_name
				
		return new_file_path

	def create_project_file(self,filepath):
		""" Create a new empty file in the appropriate directory with the modified filename. Takes a relative filepath as arg """		
		with open(filepath, 'w') as fp:
			pass

	def save_file(self,file_patth,projectname=None):
		""" Save the uploaded file by copying its content into the newly created empty file in the appropriate directory
			Return the project name (prefix attached to the original filename), filename
		"""		
		if self.validate_file(file_patth) and self.folder_id == 1:			
			save_to = self.mod_file_name(file_patth)
			shutil.copy(file_patth,save_to)
			
			projectname = self.file_name.split("_")[0]			
			return (projectname, self.file_name)
		elif self.validate_file(file_patth) and self.folder_id == 2:
			save_to = self.mod_file_name(file_patth,projectname)
			shutil.copy(file_patth,save_to)
			
			projectname = self.file_name.split("_")[0]			
			return (projectname, self.file_name)
		else:	
			return (None, None)	
		
	def use_saved_file(self,file_patth):
		""" Sets the file_name attr from the selected project file
			Returns the project name, filename
		"""
		if self.validate_file(file_patth):
			self.file_name = file_patth.split("/")[-1] #e.g project1_xyz.csv
			projectname = self.file_name.split("_")[0] #e.g project1			
			return (projectname, self.file_name)
		else:
			return (None, None)	

	def read_file(self,filepath):
		"""Reads a spreadsheet/csv file and returns a dictionary of its content"""

		DictReader_obj = []
		
		with open(filepath) as f:		    
		    DictReader_objx = csv.DictReader(f)
		    DictReader_obj = list(DictReader_objx)

		processed_data = self.fill_content(DictReader_obj)

		return processed_data 

	def get_month_by_number(self,month):
		"""Accepts a month number and returns the name of the month""" 
		
		if month == 1:
			return 'JAN'
		elif month == 2:
			return 'FEB'
		elif month == 3:
			return 'MAR'
		elif month == 4:
			return 'APR'
		elif month == 5:
			return 'MAY'
		elif month == 6:
			return 'JUN'
		elif month == 7:
			return 'JUL'
		elif month == 8:
			return 'AUG'
		elif month == 9:
			return 'SEP'
		elif month == 10:
			return 'OCT'
		elif month == 11:
			return 'NOV'
		elif month == 12:
			return 'DEC'											
		return None

	def get_event_duration_in_months(self,data: list,date_format:str):
		"""Spans through all events to get the duration covered in months
		   Returns a dict of month name and number for all the months covered, sorted in ascending order of months. 	
		"""
 
		start_date = []
		for x in data:
			if x["start_date"]:
				month_number = datetime.strptime(x["start_date"],date_format).month		 			
				start_date.append(month_number)			

		start_date = set(start_date)
		start_date = sorted(start_date)

		months = {}		
		for x in start_date:			
			months[x] = self.get_month_by_number(x)
			
		return months

	def group_events_by_month(self,data:list,months:dict,date_format:str):
		"""Groups all the events by the month in whch they occured.
		   First three letters of each month are used to form the keys in the returned data			
		   Returns: an obj in the form {"JAN":list1,"FEB":list2,"MAR":list3...} 
		"""

		monthly_events = []

		for i in months:
			mr = {}
			events = []
			for x in data:
				if x["start_date"]:
					month_number =	datetime.strptime(x["start_date"],date_format).month			
					if  month_number == i:
						events.append(x)
			mr["month"] = months[i]
			mr["events"] = events
			monthly_events.append(mr)

		return monthly_events

	def get_list_of_event_types(self,events: list):
		"""Spans through all events and list their types and locations"""
		event_types = []
		event_locations = []

		for x in events:
			if x["class"] and x["class"].split()[0].lower() == "planned":
				if x["type"] and x["type"].lower() not in event_types:					
					event_types.append(x["type"].lower())
				if x["type"].lower() == "cil":
					if x["location"] and x["location"].lower() not in event_locations:	
						event_locations.append(x["location"].lower())

		return (event_types,event_locations)			

	def compute_time_for_monthly_events(self,monthly_events: list):
		"""Computes the total time each event occured in each month"""

		processed_data = []		

		#get all event types		
		all_events = []
		for x in monthly_events:
			all_events.extend(x["events"])
		event_types, event_locations = self.get_list_of_event_types(all_events)
		
		#compute time for each event
		for item in monthly_events:			
			total_uptime = 0
			total_downtime = 0
			planned_downtime = 0
			unplanned_downtime = 0
			event_type_time = {}
			mr = {}

			for i in event_types:
				formated = func.enslave_strings(i)
				event_type_time[formated] = 0			
			
			mr['month'] = item['month']
						
			for x in item['events']:
				downtime = int(x['downtime'])
				uptime = int(x['uptime'])

				total_downtime += downtime
				total_uptime += uptime

				event_class = ""
				if x["class"]:
					event_class = x["class"].split()[0].lower()

				if event_class == 'planned':
					planned_downtime += int(x['downtime'])
					formated = func.enslave_strings(x["type"])
					event_type_time[formated] += int(x['downtime'])				
				else:
					unplanned_downtime += int(x['downtime'])
			
			mr['total_uptime'] = total_uptime			
			mr['total_downtime'] = total_downtime
			mr['planned_downtime'] = planned_downtime
			mr['unplanned_downtime'] = unplanned_downtime
			
			#merge mr with event_type_time
			mr.update(event_type_time)

			processed_data.append(mr)

		return processed_data

	def process_cil_location_data(self,monthly_events:list,locations:list):
		"""Generates processed data based on locations.e.i. locations are used as keys to the downtime values"""
		processed_data = []

		for item in monthly_events:	
			#initialize the downtime 
			mr = {}
			mr["month"] = item["month"]
			for x in locations:
				mr[func.enslave_strings(x)] = 0
			
			for event in item["events"]:				 
				if event["type"].lower() == "cil" and event["location"].lower() in locations:
					mr[func.enslave_strings(event["location"])] += int(event["downtime"])

			processed_data.append(mr)

		return processed_data

	def process_monthly_event_data(self,monthly_events:list,scope:str,option:str):
		"""Generates monthly downtime data for the given option"""
		processed_data = []
		
		for item in monthly_events:	
			#initialize the downtime 
			mr = {}
			mr["month"] = item["month"]
			mr[func.enslave_strings(option)] = 0
			
			for event in item["events"]:				
				if event[scope].lower() == option:					
					mr[func.enslave_strings(event[scope])] += int(event["downtime"])					

			processed_data.append(mr)

		return processed_data				

	def fill_content(self,data: list):
		"""Removes rows with no values for either start_date, uptime, downtime; and adds the string "blank" to other columns"""
		new_list = []

		for x in data:				
			if not x["class"] or x["class"] == '':
				x["class"] = "blank"
			if not x["type"] or x["type"] == '':
				x["type"] = "blank"
			if not x["location"] or x["location"] == '':
				x["location"] = "blank"
			if x["start_date"] or x["start_date"] != '':
				if x["uptime"] or x["uptime"] != '':				
					if x["downtime"] or x["downtime"] != '':				
						new_list.append(x)						   

		return new_list	


