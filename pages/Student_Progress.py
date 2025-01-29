# Student_Progress.py

import os
from datetime import datetime as dt

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import student as sd
import numpy as np
from pprint import pprint


# page configuration
st.set_page_config(
    page_title="Student Progress",
    initial_sidebar_state="auto",
    # page_icon="_data/logo.jpg"
)


conn = st.connection("gsheets", type=GSheetsConnection)
# automatically cached, set to 10 mins
students = conn.read(worksheet="students", ttl="10m")
progress_report = conn.read(worksheet="progress_report", ttl="10m")
diagnostic = conn.read(worksheet="diagnostic", ttl="10m")
constants = conn.read(worksheet="CONSTANTS", ttl="10m")


# auxilliary functions
def get_constants(column):
	constants = pd.unique(column.dropna())
	return constants

def format_lists(arr1, arr2):
	formatted = arr1
	if ("other (specify below)" in arr1):
		formatted.remove("other (specify below)")
	if (arr2 != ""):
		formatted += [el.strip() for el in arr2.split(',')]
	return formatted



#page content
st.title("Student Progress")

col1, col2 = st.columns([0.7, 0.3])
with col1:
	tutor_name = st.text_input(
		label="tutor_name",
		value="Jake the Dog",
		help="""
			Please input your name here. Note that other tutors will see
			your name in the students' profile. If you do not want to 
			input your name, you may also use a pseudonym. We just need 
			a way to differentiate between the tutors.
		"""
	)
with col2:
	tutoring_date = st.date_input(
		label="tutoring_date",
		value="today",
		format="DD/MM/YYYY",
		help="Please input when you tutored the student.",
	)
student_name = st.selectbox(
	label="student_name",
	options=["Choose a student"] + sorted(students["fullname"].unique()),
)
st.divider()
st.warning("""
	Please note that this page is being cached every 10 minutes	so you
	might experience unusual behavior with the form at this interval. 
	Do not worry as your answers are regularly saved, but will only be 
	considered final once you click ':primary[Submit Report]' (in case 
	you are submitting a report).
""")

if (student_name != "Choose a student"):
	
	student_row = students[students["fullname"] == student_name].fillna('')
	student_row = student_row.to_dict("records")[0]
	student = sd.Student(student_row)
	
	student_reports = student.get_reports(progress_report)
	
	basic_info, tutor_reports, submit_report = st.tabs(["Basic Information", "Tutor Reports", "Submit Report"])
	
	with basic_info:
		
		bi11, bi12, bi13 = st.columns([0.5, 0.35, 0.15])
		with bi11:
			fullname = st.text_input(
				label="Fullname",
				value=student.fullname,
				disabled=True
			)
		with bi12:
			nickname = st.text_input(
				label="Nickname/s",
				value=student.nickname,
				disabled=True
			)
		with bi13:
			learning_group = st.text_input(
				label="Group",
				value=student.learning_group,
				help="This is the assigned learning group for second semester insertions.",
				disabled=True
			)
		
		bi21, bi22, bi23 = st.columns([0.2, 0.1, 0.7])
		with bi21:
			school = st.text_input(
				label="School",
				value=student.school,
				disabled=True
			)
		with bi22:
			grade_level = st.text_input(
				label="Grade",
				value=str(student.grade_level),
				disabled=True
			)
		with bi23:
			notes = st.text_input(
				label="Notes",
				value=student.notes,
				disabled=True
			)
		
	with tutor_reports:
		
		show_dates = st.multiselect(
			label="Show reports for insertion dates...",
			options=student.present_dates,
			default=(None if (student.present_dates.size == 0) else student.present_dates[0]),
			help="The date options are arranged such that the latest one is at the top."
		)
		st.divider()
		student_dates_report = student_reports.loc[student_reports["date"].isin(show_dates)]
		
		key_iter = 0
		for row in student_dates_report.itertuples():
		
			key_iter += 1
			entry = sd.Entry(row, form="tuple")
			
			st.info(
				f"Report by :primary[{entry.tutor}] for the insertion on :primary[{entry.date.strftime('%b %d %Y')}].",
				icon=":material/emoji_objects:"
			)
			
			tr11, tr12, tr13 = st.columns([0.2, 0.5, 0.3])
			with tr11:
				st.text_input(
					label="Subject",
					value=entry.subject,
					key=f"tr_subject{key_iter}",
					disabled=True
				)
			with tr12:
				st.text_input(
					label="Module taken",
					value=entry.module_taken,
					key=f"tr_module{key_iter}",
					disabled=True
				)
			with tr13:
				st.text_input(
					label="Tutoring group",
					value=row.tutoring_group,
					key=f"tr_group{key_iter}",
					disabled=True
				)
				
			st.text_area(
				label="What are some of the student's strengths while taking this module?",
				value=", ".join(entry.strengths),
				key=f"tr_strengths{key_iter}",
				height=68,
				disabled=True
			)
			
			st.text_area(
				label="What interventions do you think will help the student for the next sessions?",
				value=", ".join(entry.interventions),
				key=f"tr_interventions{key_iter}",
				height=68,
				disabled=True
			)
			
			st.text_area(
				label="Miscellaneous notes",
				value=entry.misc_notes,
				key=f"tr_miscnotes{key_iter}",
				height=68,
				disabled=True
			)
			
			st.text(" ")
			st.dataframe(
				data=entry.learning_behavior,
				use_container_width=True,
				column_order=["descriptor", "notes"],
				key=f"tr_behavior{key_iter}",
				column_config={
					"descriptor": st.column_config.TextColumn(
						label="descriptor",
						width="medium",
						disabled=True,
					),
					"notes": st.column_config.TextColumn(
						label="notes",
						width="small",
						disabled=True,
					)
				}
			)
			
			progress_formatted = (":green[proceed to the next module]" if entry.proceed else ":orange[review the current module]")
			st.write(f"The tutor recommended to **{progress_formatted}** for the next session.")
			
			st.divider()
				
		st.info(f"End of reports for {student.fullname}.", icon=":material/error:")
		
	
	with submit_report:
		st.info("""
			This is where you input your report at the end of the session. 
			Please make sure that the :primary[tutoring_date] is accurate and 
			that :primary[tutor_name] is filled-in for future reference.""", 
			icon=":material/error:"
		)	
		st.text(" ")
			
		lr11, lr12, lr13 = st.columns([0.2, 0.5, 0.3])
		with lr11:
			subject = st.selectbox(
				label="Subject",
				options=["English", "Math"]
			)
		with lr12:
			module = st.selectbox(
				label="Module taken",
				options=(get_constants(constants["english_modules"]) if subject == "English" else get_constants(constants["math_modules"]))
			)
		with lr13:
			tutoring_group = st.text_input(
				label="Tutoring Group",
				value="Adventure Time",
				disabled=True
			)
			
		strengths = st.multiselect(
			label="What are some of the student's strengths while taking this module?",
			options=pd.unique(constants["strengths_options"].dropna()),
			help="Please choose all that apply based on your interaction with the student."
		)
		other_strengths = ""
		if ("other (specify below)" in strengths):
			other_strengths = st.text_input(
				label="other strengths:",
				help="""
					Please try to be as specific as you can. If you have 
					multiple responses, please separate them by commas.
				"""
			)

		fields = {
			"attention": "none", 
			"topic_reception": "none", 
			"task_reception": "none", 
			"questions": "none", 
			"answers": "none"
		}
		learning_behavior = {field: {"descriptor": "", "notes": ""} for field in fields.keys()}
		for field in fields.keys():
			lr3a, lr3b = st.columns([0.55, 0.45])
			with lr3a:
				learning_behavior[field]["descriptor"] = st.selectbox(
					label=field,
					options=pd.unique(constants[field].dropna())
				)
			with lr3b:
				learning_behavior[field]["notes"] = st.text_area(
					label=f"notes on {field}",
					help=fields[field],
					height=68
				)
		
		lr41, lr42 = st.columns([0.75, 0.25])
		with lr41:
			interventions = st.multiselect(
				label="What interventions do you think will help the student for the next sessions?",
				options=pd.unique(constants["interventions"].dropna())
			)
			other_interventions = ""
			if ("other (specify below)" in interventions):
				other_interventions = st.text_input(
					label="other interventions:",
					help="""
						Please try to be as specific as you can. If you have 
						multiple responses, please separate them by commas.
					"""
				)
		with lr42:
			proceed = st.radio(
				label="Should the student move-on to the next module?",
				options=["Yes", "No"],
				horizontal=True,
				help="Please consider all aspects of your report for this decision."
			)
		
		additionals = st.text_area(
			label="Miscellaneous notes",
			help="""
				Please include here any additional notes that you were 
				not able to include in the previous parts. For comments 
				about the general learning environment, module materials, 
				and tutoring implementation, please put them on the 
				Insertion Evaluations tab *unless they are related to 
				this specific student*.
			"""
		)
		
		st.text(" ")
		st.info(f"""
			Please confirm that this is a report by {tutor_name} for the 
			Erya Insertion on {tutoring_date.strftime('%b %d %Y')}. The 
			information above will be included in the student profile 
			of {student_name}.""", 
			icon=":material/error:"
		)	
		submit = st.button(
			label=f"Submit Report",
			use_container_width=True,
			type="primary"
		)
		
		if (submit):
			report = {
				"strengths": format_lists(strengths, other_strengths),
				"learning_behavior": learning_behavior,
				"interventions": format_lists(interventions, other_interventions),
				"misc_notes": additionals,
				"proceed": (proceed == "Yes"),
			}
			row = {
				"student_id": student.id,
				"date": tutoring_date,
				"tutor": tutor_name,
				"subject": subject,
				"module_taken": module,
				"tutoring_group": tutoring_group,
				"report": repr(report),
			}
			
			entry = sd.Entry(row, form="dict")
			try:
				curr_df = conn.read(worksheet="progress_report")
				conn.update(worksheet="progress_report", data=entry.add_to(curr_df))
				st.info("""
					Yay! Report submitted. Thank you for offering your 
					time for our Erya kids.""", 
					icon=":material/celebration:"
				)
			except:
				st.error("""
					Sorry, but something went wrong. Please try submitting 
					again. If this error still persists, contact ERDA.""", 
					icon=":material/sentiment_dissatisfied:"
				)
