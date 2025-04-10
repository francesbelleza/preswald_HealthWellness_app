from preswald import text, plotly, connect, get_df, table, query
import pandas as pd
import plotly.express as px

text("# Welcome to Preswald!")
text("This is your first app. 🎉")

# Load the CSV
connect() # load in all sources, which by default is the sample_csv
df = get_df('health_activity_data.csv')

# get only ppl with heart disease
sql = "SELECT*FROM health_activity_data WHERE Heart_Disease = 'Yes'"
df_heart = query(sql, "health_activity_data")
table(df_heart)

####visuals i want to add: bargraph & scatterplot

# datapoints im using
sql = """
SELECT Hours_of_Sleep,Heart_Rate,Blood_Pressure,Exercise_Hours_per_Week,
Smoker,Alcohol_Consumption_per_Week,Diabetic
FROM health_activity_data
WHERE Heart_Disease = 'YES'
"""
df_heart_risk = query(sql, "health_activity_data")

#bar graph data
bar_data = df_heart_risk[['Hours_of_Sleep','Heart_Rate','Blood_Pressure', 'Exercise_Hours_per_Week',
'Smoker','Alcohol_Consumption_per_Week','Diabetic']].melt()
bar_data = bar_data.groupby(['variable', 'value']).size().reset_index(name='count')
fig = px.bar(bar_data, x="variable", y="count", color="value",
             title="Heart Disease x Lifestyle Factors",
             labels={"variable": "Lifestyle Factor", "count": "Number of People", "value": "Status"})
plotly(fig)

# Create a historgram plot for age x heart disease
fig = px.histogram(df_heart, x="Age", nbins=10,
                   title="Age Distribution of People with Heart Disease",
                   labels={"Age": "Age"})
fig.update_layout(template="plotly_white")
plotly(fig)

# pie chart for gender x heart disease
sql = """
SELECT Gender, COUNT(*) as count
FROM health_activity_data
WHERE Heart_Disease = 'Yes'
GROUP BY Gender
"""
df_gender = query(sql, "health_activity_data")

fig = px.pie(df_gender, names="Gender", values="count",
             title="Gender x Heart Disease")
fig.update_layout(template="plotly_white")
plotly(fig)



# Add labels for each point
fig.update_traces(textposition='top center', marker=dict(size=12, color='lightblue'))

# Style the plot
fig.update_layout(template='plotly_white')

# Show the plot
plotly(fig)

# Show the data
table(df)
