# student.py

import hashlib
import os
from datetime import datetime

import numpy as np
import pandas as pd


# auxilliary functions
def get_id(seed):
	h = hashlib.sha256()
	h.update(seed.encode())
	return h.hexdigest()[:10]


class Entry:
	def __init__(self, context, form="dict"):
		
		# tuples are for objects taken from the gsheet file, 
		# dict are the ones generated in the report. 
		# date has to be handled by-case because we expect
		# different formats dependong on the source
		if (form == "tuple"):
			self.entry = context._asdict()
			self.date = datetime.strptime(self.entry["date"], '%Y-%m-%d')
		elif (form == "dict"):
			self.entry = context
			self.date = self.entry["date"]
		
		self.df = pd.DataFrame(data=self.entry, index=[0])
		
		self.student_id = str(self.entry["student_id"])
		self.tutor = str(self.entry["tutor"])
		self.subject = str(self.entry["subject"])
		self.module_taken = str(self.entry["module_taken"])
		self.tutoring_group = str(self.entry["tutoring_group"])
		self.report = eval(self.entry["report"])
		
		self.generals = pd.DataFrame(
			data={
				"strengths": {"descriptor": ", ".join(list(self.report["strengths"]))},
				"interventions": {"descriptor": ", ".join(list(self.report["interventions"]))},
				"miscellaneous_notes": {"descriptor": str(self.report["misc_notes"])}
			}
		).T
		self.learning_behavior = pd.DataFrame(
			data=self.report["learning_behavior"]
		).T
		self.proceed = bool(self.report["proceed"])


	def add_to(self, curr_df):
		new_df = pd.concat([curr_df, self.df])
		return new_df
		


class Student:
	def __init__(self, context):
		self.fullname = str(context["fullname"])
		self.nickname = str(context["nickname"])
		self.grade_level = int(context["grade_level"])
		self.school = str(context["school"])
		self.math_status = str(context["math_status"])
		self.english_status = str(context["english_status"])
		self.notes = str(context["notes"])
		self.id = get_id("_".join([self.fullname, str(self.grade_level), self.school]))
	
	def get_reports(self, all_reports):
		self.reports = all_reports[all_reports["student_id"] == self.id].sort_values(by=["date", "subject"], ascending=False)
		self.present_dates = pd.unique(self.reports["date"].dropna())
		return self.reports
		
		
		
