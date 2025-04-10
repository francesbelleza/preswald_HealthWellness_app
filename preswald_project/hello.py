from preswald import text, plotly, connect, get_df, table, query
import pandas as pd
import plotly.express as px

# TO DO:
#   add x y labels

text("# welcome to signl🫀")
text("Designed for healthcare professionals, Signl highlights patterns "
     "in daily habits that may support more informed, human-centered care. "
     "Instead of isolated data points, Signl offers a friendly lens into routines, "
     "behaviors, and rhythms — giving clinical teams a clearer picture of the "
     "lifestyle factors that shape heart health.")

# Load the CSV
connect() # load in all sources, which by default is the sample_csv
df = get_df('health_activity_data_csv')

######## gender & heart disease
sql = """
SELECT ID, Gender
FROM health_activity_data_csv
WHERE Heart_Disease = 'Yes'
"""
df_gender = query(sql, "health_activity_data_csv")

### pie chart
gender_counts = df_gender['Gender'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'count']

text("## heart disease: gender breakdown")
fig = px.pie(gender_counts,
             names = 'Gender',
             values = 'count')
fig.update_layout(template = 'plotly_white')
plotly(fig)

####### blood pressure, age, gender
sql = """
SELECT Blood_Pressure, Gender, Age
FROM health_activity_data_csv
WHERE Heart_Disease = 'Yes'
"""
df_bp = query(sql, "health_activity_data_csv")

### histogram
# need to just take top part of blood pressure
df_bp['top_part'] = df_bp['Blood_Pressure'].str.split('/').str[0]
df_bp['top_part'] = pd.to_numeric(df_bp['top_part'], errors='coerce')
df_bp['Age'] = pd.to_numeric(df_bp['Age'], errors='coerce')

text("## blood pressure by gender")
fig = px.histogram(df_bp, x='top_part', color='Gender',
                   barmode='group', nbins=20,
                   labels={'top_part': 'Blood Pressure', 'Gender': 'Gender'})
fig.update_layout(template='plotly_white', bargap=0.15)
plotly(fig)

######## hours sleep & heart rate
sql = """
SELECT Hours_of_Sleep, Heart_Rate
FROM health_activity_data_csv
WHERE Heart_Disease = 'Yes'
"""
df_sleep_hr = query(sql, "health_activity_data_csv")

### histogram
df_sleep_hr['Hours_of_Sleep'] = pd.to_numeric(df_sleep_hr['Hours_of_Sleep'], errors='coerce')
df_sleep_hr['Heart_Rate'] = pd.to_numeric(df_sleep_hr['Heart_Rate'], errors='coerce')
df_sleep_hr = df_sleep_hr.dropna(subset=['Hours_of_Sleep', 'Heart_Rate'])

text("## breakdown of sleep length")
fig_sleep = px.histogram(df_sleep_hr, x='Hours_of_Sleep',
                         nbins=20,
                         labels={'Hours_of_Sleep': 'Hours of Sleep'})
fig_sleep.update_layout(template='plotly_white', bargap=0.2)
plotly(fig_sleep)

text("## breakdown of heart rate")
fig_hr = px.histogram(df_sleep_hr, x='Heart_Rate',
                      nbins=20,
                      labels={'Heart_Rate': 'Heart Rate'})
fig_hr.update_layout(template='plotly_white', bargap=0.2)
plotly(fig_hr)

######## diabetic & non-diabetic
sql = """
SELECT Diabetic
FROM health_activity_data_csv
WHERE Heart_Disease = 'Yes'
"""
df_diabetic = query(sql, "health_activity_data_csv")

### histogram
diabetic_counts = df_diabetic['Diabetic'].value_counts().reset_index()
diabetic_counts.columns = ['Diabetic', 'count']

text("## diabetic v. non-diabetic")
fig = px.pie(diabetic_counts, names='Diabetic', values='count')
fig.update_layout(template='plotly_white')
plotly(fig)

text("###*'Helping care teams notice the quiet signals in lifestyle data.'*")
