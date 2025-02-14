# Welcome.py

import streamlit as st


# page configuration
st.set_page_config(
    page_title="GABAY Erya Insertion",
    initial_sidebar_state="auto",
    # page_icon="_data/logo.jpg"
)


links = {
	"groupings": "https://docs.google.com/spreadsheets/d/1GYbTAZzL3GLPpZfMej1-IEEzFMb3r84CZOP-TwMCDZQ/edit?usp=sharing",
	"ma": {
		"ma_modules": [
			"M1: Reading and Writing Numbers and Equations",
			"M2: Comparison of Numbers",
			"M3: Addition and Subtraction",
			"M4: Multiplication and Division",
			"M5: PEMDAS"
		],
		"ma_links": [
			"https://docs.google.com/document/d/1qD18ZlJI_iWIjG2MCOMOV62X_nuH2hEPzuN3S7Meg_A/edit?usp=sharing",
			None,
			None,
			None,
			None
		]
	},
	"en": {
		"en_modules": [
			"E1: Nouns and Pronouns",
			"E2: Adjectives and Adverbs",
			"E3: Verbs and Tenses",
			"E4: Subject-Verb Agreement and Sentence Construction",
			"E5: Prepositions and Conjunctions"
		],
		"en_links": [
			"https://docs.google.com/document/d/1xXXmdzd5i3NvfVRDgDX5e8eJu61bwz7-/edit?usp=sharing&ouid=107576044519208689840&rtpof=true&sd=true",
			None,
			None,
			None,
			None
		]
	},
	"contact": {
		"rolen": "https://fb.com/rolen08"
	}
}

# page content
st.title("Tutor and Student Progress Report")
st.write("""
	Hello tutors! 
	
	Please use take the time to **read the progress reports** (if there are any) before the session, and **answer the progress report** after the session. Your input would be invaluable in the development of future modules and insertions. Thank you so much!
""")
st.write(f"""If you have any concerns regarding this webapp, please directly message [Rolen Muana]({links['contact']['rolen']}).""")
st.text(" ")

with st.expander(label="I want to check the TUTOR GROUPINGS", expanded=False, icon=":material/diversity_3:"):
	st.write(f"""
		Gorabels po, check them [though this link]({links['groupings']}). 
		
		If you have any concerns, please contact Ivy Pulido, Kate Aizpuru, Dory Robles, or Seya Nato. 
	""")


with st.expander(label="I want to check the TUTORS' KITS / MODULES", expanded=False, icon=":material/folder_open:"):
	st.write(f"""
		Ge lang lods, the following are the available modules. Please 
		note that we will constantly update them as we proceed with 
		the sessions.

		If you have any concerns, please contact Love Caranza. 
	""")
	
	st.dataframe(
		data=links['ma'],
		column_config={
			"ma_modules": st.column_config.TextColumn(
				label="modules",
				width="small"
			),
			"ma_links": st.column_config.LinkColumn(
				label="links",
				width="medium"
			)
		},
		hide_index=True,
		use_container_width=True
	)
	
	st.dataframe(
		data=links['en'],
		column_config={
			"en_modules": st.column_config.TextColumn(
				label="modules",
				width="small"
			),
			"en_links": st.column_config.LinkColumn(
				label="links",
				width="medium"
			)
		},
		hide_index=True,
		use_container_width=True
	)


with st.expander(label="I want to submit a STUDENT PROGRESS REPORT", expanded=False, icon=":material/lab_profile:"):
	st.write("""
		Tama yan! Please proceed to the `Student Progrress` page (on the sidebar) and input the necessary information on the fields provided. Please ensure that you inputted the correct `tutor_name` and `tutoring_date` before submitting the report. Note that each report may be seen by the student's tutor for the next insertion. 
	""")

