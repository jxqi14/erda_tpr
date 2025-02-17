# Welcome.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# page configuration
st.set_page_config(
    page_title="GABAY Erya Insertion",
    initial_sidebar_state="auto",
    # page_icon="_data/logo.jpg"
)

conn = st.connection("gsheets", type=GSheetsConnection)
# automatically cached, set to 10 mins
constants = conn.read(worksheet="CONSTANTS", ttl="10m")

# page content
st.title("Tutor and Student Progress Report")
st.write("""
	Hello tutors! 
	
	Please use take the time to :primary[**read the progress reports**] (if there are any) before the session, and :primary[**answer the progress report**] after the session. Your input would be invaluable in the development of future modules and insertions. Thank you so much!
""")
st.text(" ")

with st.expander(label="I want to check the TUTOR GROUPINGS", expanded=False, icon=":material/diversity_3:"):
	st.write(f"""
		Gorabels po, check them [though this link]({constants.loc[0, 'extra_links']}). 
		
		If you have any concerns, please contact Ivy Pulido, Kate Aizpuru, Dory Robles, or Seya Nato. 
	""")


with st.expander(label="I want to check the TUTORS' KITS / MODULES", expanded=False, icon=":material/folder_open:"):
	st.write(f"""
		Ge lang lods, the following are the available modules. Please 
		note that we will constantly update them as we proceed with 
		the sessions.

		If you have any concerns, please contact [Love Caranza]({constants.loc[2, 'extra_links']}). 
	""")
	
	st.dataframe(
		data=constants.dropna(axis="rows")[['math_modules', 'math_links']],
		column_config={
			"math_modules": st.column_config.TextColumn(
				label="modules",
				width="small"
			),
			"math_links": st.column_config.LinkColumn(
				label="links",
				width="medium"
			)
		},
		hide_index=True,
		use_container_width=True
	)
	
	st.dataframe(
		data=constants.dropna(axis="rows")[['english_modules', 'english_links']],
		column_config={
			"english_modules": st.column_config.TextColumn(
				label="modules",
				width="small"
			),
			"english_links": st.column_config.LinkColumn(
				label="links",
				width="medium"
			)
		},
		hide_index=True,
		use_container_width=True
	)


with st.expander(label="I want to submit a STUDENT PROGRESS REPORT", expanded=False, icon=":material/lab_profile:"):
	st.write("""
		Tama yan! 
		
		Please proceed to the :primary[Student Progress] page (on the sidebar) and input the necessary information on the fields provided. Please ensure that you inputted the correct :primary[tutor_name] and :primary[tutoring_date] before submitting the report. Note that each report may be seen by the student's tutor for the next insertion. 
		
		If you are not sure about the purpose and criteria for each field, please click / hover over the question mark icon beside field label. For more information, contact anyone from ERDA. Thank you!
	""")
st.write(f"""If you have any concerns regarding this webapp, please directly message [Rolen Muana]({constants.loc[1, 'extra_links']}).""")
