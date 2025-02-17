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
	constants = np.sort(pd.unique(column.dropna()))
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

col11, col12 = st.columns([0.7, 0.3])
with col11:
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
with col12:
	tutoring_date = st.date_input(
		label="tutoring_date",
		value="today",
		format="DD/MM/YYYY",
		help="Please input when you tutored the student.",
	)
	
col21, col22, col23 = st.columns([0.2, 0.3, 0.5])
with col21: 
	grade = st.selectbox(
		label="grade",
		options=get_constants(students["grade_level"]),
		format_func=int
	)
with col22:
	school = st.selectbox(
		label="school",
		options=get_constants(students["school"])
	)
with col23:
	student_names = get_constants(students[
			(students["grade_level"] == grade) & (students["school"] == school)
		]["fullname"])
	student_name = st.selectbox(
		label="student_name",
		options=student_names
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
	
	# ~ basic_info, tutor_reports, submit_report = st.tabs(["Basic Information", "Tutor Reports", "Submit Report"])
	submit_report, tutor_reports, basic_info = st.tabs(["Submit Report", "Tutor Reports", "Basic Information"])
	
	with basic_info:
		
		bi11, bi12, bi13, bi14 = st.columns([0.45, 0.25, 0.2, 0.1])
		with bi11:
			fullname = st.text_input(
				label="fullname",
				value=student.fullname,
				disabled=True
			)
		with bi12:
			nickname = st.text_input(
				label="nickname/s",
				value=student.nickname,
				disabled=True
			)
		with bi13:
			school = st.text_input(
				label="school",
				value=student.school,
				disabled=True
			)
		with bi14:
			grade_level = st.text_input(
				label="grade",
				value=str(student.grade_level),
				disabled=True
			)
		
		bi21, bi22, bi23 = st.columns([0.2, 0.2, 0.6])
		with bi21:
			math_status = st.text_input(
				label="math_status",
				value=student.math_status,
				disabled=True
			)
		with bi22:
			english_status = st.text_input(
				label="english_status",
				value=student.english_status,
				disabled=True
			)
		with bi23:
			notes = st.text_area(
				label="notes",
				value=student.notes,
				height=68,
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
		student_dates_report = student_reports \
			.loc[student_reports["date"].isin(show_dates)] \
			.drop_duplicates(keep="last")
			
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
					label="subject",
					value=entry.subject,
					key=f"tr_subject{key_iter}",
					disabled=True
				)
			with tr12:
				st.text_input(
					label="module taken",
					value=entry.module_taken,
					key=f"tr_module{key_iter}",
					disabled=True
				)
			with tr13:
				st.text_input(
					label="tutoring group",
					value=row.tutoring_group,
					key=f"tr_group{key_iter}",
					disabled=True
				)
				
			st.text(" ")
			gen_sizes1 = (0.25, 0.75)
			f1, d1 = st.columns(gen_sizes1)
			with f1:
				st.write(":blue[field]")
			with d1: 
				st.write(":blue[descriptor]")
			
			for (key, val) in entry.generals.items():
				f1g, d1g = st.columns(gen_sizes1)
				with f1g: 
					st.write(key)
				with d1g:
					st.write(val["descriptor"])
			
			st.text(" ")
			gen_sizes2 = (0.25, 0.1, 0.75)
			f2, r2, d2 = st.columns(gen_sizes2)
			with f2:
				st.write(":blue[field]")
			with r2:
				st.write(":blue[rating]")
			with d2:
				st.write(":blue[descriptor]")
			
			for (key, val) in entry.learning_behavior.items():
				f2g, r2g, d2g = st.columns(gen_sizes2)
				with f2g:
					st.write(key)
				with r2g:
					st.write(str(val["rating"]))
				with d2g:
					st.write(val["notes"])
			
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
			tutoring_group = st.selectbox(
				label="Tutoring Group",
				options=get_constants(constants["tutoring_groups"])
			)
			
		strengths = st.multiselect(
			label="What are some of the student's strengths while taking this module?",
			options=pd.unique(constants["strengths_options"].dropna()),
			default=None,
			help="Please choose all that apply based on your interaction with the student."
		)
		other_strengths = ""
		if ("other (specify below)" in strengths):
			other_strengths = st.text_area(
				label="other strengths:",
				value="",
				help="""
					Please try to be as specific as you can. If you have 
					multiple responses, please separate them by commas.
				"""
			)
			
		interventions = st.multiselect(
			label="What interventions do you think will help the student for the next sessions?",
			default=None,
			options=pd.unique(constants["interventions"].dropna())
		)
		other_interventions = ""
		if ("other (specify below)" in interventions):
			other_interventions = st.text_area(
				label="other interventions:",
				value="",
				help="""
					Please try to be as specific as you can. If you have 
					multiple responses, please separate them by commas.
				"""
			)

		fields = {
			"participation": "Please rate the student's level of participation, with 0 being very distracted and 5 being very attentive. You are free to add  more details on your rating on the corresponding textbox.", 
			"topic_reception": "Please rate the student's willingness to do their task, with 0 signifying that they completely refused to do the task and 5 signifying that they were enthusiastic in doing the task. You are free to add  more details on your rating on the corresponding textbox.", 
			"questions/answers": "Please rate the quality of the students' questions/answers, with 0 signifying that they did not ask/answer questions and 5 signifying that their questions/answers were relevant to the topic. You are free to add  more details on your rating on the corresponding textbox. Please note any important questions/requests that they made."
		}
		learning_behavior = {field: {"rating": None, "notes": None} for field in fields.keys()}
		for (field, helpnotes) in fields.items():
			lr4a, lr4b = st.columns([0.45, 0.55])
			with lr4a:
				learning_behavior[field]["rating"] = st.slider(
					label=field,
					value=0,
					min_value=0,
					max_value=5,
					step=1,
					help=helpnotes
				)
			with lr4b:
				learning_behavior[field]["notes"] = st.text_area(
					label=f"notes on {field}",
					value="",
					height=68
				)
		
		lr51, lr52 = st.columns([0.65, 0.35])
		with lr51:
			additionals = st.text_area(
				label="What other things should the next tutor know about the student?",
				height=68,
				help="""
					Please include here any additional notes that you were 
					not able to include in the previous parts. For comments 
					about the general learning environment, module materials, 
					and tutoring implementation, please put them on the 
					Insertion Evaluations tab *unless they are related to 
					this specific student*.
				"""
			)
		with lr52:
			proceed = st.radio(
				label="Should the student move-on to the next module?",
				options=["Yes", "No"],
				horizontal=True,
				help="Please consider all aspects of your report for this decision."
			)

		
		st.text(" ")
		st.info(f"""
			Please confirm that this is a report by :primary[{tutor_name}] 
			for the Erya Insertion on :primary[{tutoring_date.strftime('%b %d %Y')}].
			The information above will be included in the student profile of 
			:primary[{student_name}].""", 
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
