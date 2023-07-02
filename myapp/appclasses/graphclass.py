"""This is the graph class module"""
from myapp.helpers import myfunc as func
import hmac,hashlib
import csv
import random
import calendar
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np
from myapp.appclasses.fileclass import FILEHANDLER


class MYGRAPH(object):
	"""Class used to generate different graph for the machine/equipment data"""

	def __init__(self):
		"""Initialize the MYGRAPH class. No argument required"""
		super(MYGRAPH, self).__init__()
		pass
		
	def generate_uptime_and_downtime_graph(self,data,title=""):
		"""Genearates the graph of uptime and downtime events from processed data"""

		data = data[:6]
		width = 0.25
		x = [x['month'] for x in data]
		
		uptime = [x['total_uptime'] for x in data]
		
		downtime = [x['total_downtime'] for x in data]		
		upt_percent = ['{}%'.format(round(x['total_uptime']/(x['total_uptime']+x['total_downtime'])*100)) for x in data]
		dwnt_percent = ['{}%'.format(round(x['total_downtime']/(x['total_uptime']+x['total_downtime'])*100)) for x in data] 
		
		x_axis = np.arange(len(x))

		A = plt.bar(x_axis - width, uptime, width, label = 'Uptime', color=['brown'])
		B = plt.bar(x_axis, downtime, width, label = 'Downtime', color=['blue'])
		
		def annotations(bars,text,index = 0):
			count = 0
			for bar in bars:
				height = bar.get_height()
				plt.annotate('{}'.format(text[count]),
					xy=(bar.get_x() + bar.get_width() / 2, height),
					xytext=(0, 1),  # 1 points vertical offset
					textcoords="offset points",
					ha='center', va='bottom',
					)
				count += 1
						
		annotations(A,upt_percent)
		annotations(B,dwnt_percent)		
		plt.xticks(x_axis - width/2, x, rotation='vertical')
		plt.xlabel("Months")
		plt.ylabel("Time in mins")
		plt.title(title)
		plt.legend()
		plt.show()

		return	
	
	def generate_planned_and_unplanned_dt_graph(self,data,title=""):
		"""Genearates the graph of planned and unplanned downtime events from processed data"""

		data = data[:6]
		width = 0.4
		x = [x['month'] for x in data]
		
		uptime = [x['planned_downtime'] for x in data]
		downtime = [x['unplanned_downtime'] for x in data]
		upt_percent = ['{}%'.format(round(x['planned_downtime']/(x['planned_downtime']+x['unplanned_downtime'])*100)) for x in data]
		dwnt_percent = ['{}%'.format(round(x['unplanned_downtime']/(x['planned_downtime']+x['unplanned_downtime'])*100)) for x in data] 
		
		x_axis = np.arange(len(x))

		A = plt.bar(x_axis - width, uptime, width, label = 'Planned DT', color=['brown'])
		B = plt.bar(x_axis, downtime, width, label = 'Unplanned DT', color=['grey'])
		
		def annotations(bars,text,index = 0):
			count = 0
			for bar in bars:
				height = bar.get_height()
				plt.annotate('{}'.format(text[count]),
					xy=(bar.get_x() + bar.get_width() / 2, height),
					xytext=(0, 1),  # 1 points vertical offset
					textcoords="offset points",
					ha='center', va='bottom',
					)
				count += 1
						
		annotations(A,upt_percent)
		annotations(B,dwnt_percent)		
		plt.xticks(x_axis - width/2, x, rotation='vertical')
		plt.xlabel("Months")
		plt.ylabel("Time in mins")
		plt.title(title)
		plt.legend()
		plt.show()
		return
	
	def get_bar_colors(self,number_of_colors):

		from matplotlib import colors as mcolors 
		colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

		# Sort colors by hue, saturation, value and name.
		by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name) for name, color in colors.items())

		sorted_names = [name for hsv, name in by_hsv]

		if number_of_colors > len(sorted_names):
			return None

		random.shuffle(sorted_names)	

		return sorted_names[:number_of_colors]

	def generate_average_dt_graph(self,data,event_types,title=""):
		"""generates average planned downtime graphs for all the event types"""
		data = data[:6]		
		width = 0.4
		x = sorted(event_types)		
		color = self.get_bar_colors(len(x))

		def compute_average_time(data,event_types):
			mr = {}
			for pts in event_types:
				pt = func.enslave_strings(pts)
				mr[pt] = round(sum([x[pt] for x in data])/len(data))
			
			return mr	
		info = compute_average_time(data,x)		
		uptime = [info[func.enslave_strings(i)] for i in x]					
		
		x_axis = np.arange(len(x))

		A = plt.bar(x_axis, uptime, width, label = x, color=color)
				
		def annotations(bars,text):
			count = 0
			for bar in bars:
				height = bar.get_height()
				plt.annotate('{}'.format(text[count]),
					xy=(bar.get_x() + bar.get_width() / 2, height),
					xytext=(0, 1),  # 1 points vertical offset
					textcoords="offset points",
					ha='center', va='bottom',
					)
				count += 1
						
		annotations(A,uptime)
						
		#plt.xticks(x_axis, x, rotation='vertical')
		plt.xticks(x_axis, [], rotation='vertical')
		plt.xlabel("Work Points")
		plt.ylabel("Time in mins")
		plt.title(title)
		plt.legend()
		plt.show()	
		return		

	def generate_monthly_event_graph(self,data:list,option:str,title=""):
		"""Genearates monthly downtime graph for a chosen option"""

		data = data[:6]
		width = 0.4
		x = [x['month'] for x in data]
		
		uptime = [x[func.enslave_strings(option)] for x in data]		

		x_axis = np.arange(len(x))

		A = plt.bar(x_axis - width, uptime, width, label = option.title(), color=['brown'])		
		
		def annotations(bars,text,index = 0):
			count = 0
			for bar in bars:
				height = bar.get_height()
				plt.annotate('{}'.format(text[count]),
					xy=(bar.get_x() + bar.get_width() / 2, height),
					xytext=(0, 1),  # 1 points vertical offset
					textcoords="offset points",
					ha='center', va='bottom',
					)
				count += 1
						
		annotations(A,uptime)				
		plt.xticks(x_axis - width/2, x, rotation='vertical')
		plt.xlabel("Months")
		plt.ylabel("Time in mins")
		plt.title(title)
		plt.legend()
		plt.show()
		return	