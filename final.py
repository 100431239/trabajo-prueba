import pandas as pd
import sqlite3
import streamlit as st

# The layout is changed to fill the whole webpage
st.set_page_config(layout='wide')

# Header image and title are loaded, the title has formated color (extra)
st.image("header.PNG")
st.markdown('<h1 style="color:#1c7edc;">Partner search app</h1>', unsafe_allow_html=True)

# FR2.5: Connect to the ecsel_database.db and extract the list of countries in a dataframe
conn = sqlite3.connect('ecsel_database.db')
countries_df = pd.read_sql_query('SELECT * FROM Countries', conn)
countries_df = pd.DataFrame(countries_df)
acros = list(countries_df["Acronym"])

# FR2.6: Ask the user to input a country acronym
selected_country_acronym = st.selectbox("Please select a country acronym from the dropdown menu:", acros)
country_name = countries_df.loc[countries_df["Acronym"] == selected_country_acronym, "Country"].values[0]



# FR2.8: Generate a new dataframe of participants with the total amount of received grants per partner in the
# selected country and include the year information
participants_df = pd.read_sql_query(
    f"SELECT shortName, name, activityType, organizationURL, strftime('%Y', startDate) as year, SUM(ecContribution) AS Total_Grants_Received "
    f"FROM Participants p JOIN Projects pr ON p.projectID = pr.projectID WHERE Country = '{selected_country_acronym}' GROUP BY shortName, name, activityType, "
    f"organizationURL, year",  conn)

# FR2.9: Display the generated dataset, in descending order by received grants
st.markdown('<h2 style="color:#1c7edc;">Participants in {}</h2>'.format(country_name), unsafe_allow_html=True)
st.write(participants_df.sort_values("Total_Grants_Received", ascending=False))

# FR2.10: Generate a new project dataframe with the project coordinators from the selected country
project_coordinators_df = pd.read_sql_query(
    f"SELECT shortName, name, activityType, projectAcronym "
    f"FROM Participants WHERE Country = '{selected_country_acronym}' AND role = 'coordinator' "
    f"GROUP BY shortName, name, activityType, projectAcronym", conn)

# FR2.11: Display the generated coordinator dataset, in ascending order by shortName
st.markdown('<h2 style="color:#1c7edc;">Project coordinators in {}</h2>'.format(country_name), unsafe_allow_html=True)
st.write(project_coordinators_df.sort_values("shortName", ascending=True))

# FR2.12: Save the generated datasets (participants, and project coordinators) in a CSV file
participants_csv = participants_df.to_csv(index=False)
project_coordinators_csv = project_coordinators_df.to_csv(index=False)

# FR2.12: Display two download buttons to download the CSV files
st.download_button("Download Participants CSV", data=participants_csv, file_name='participants_country.csv', mime='text/csv')
st.download_button("Download Project Coordinators CSV", data=project_coordinators_csv, file_name='project_coordinators.csv', mime='text/csv')


# Extra: Display a bar chart with evolution of received grants of the partners in a country according to their activityType
st.markdown('<h2 style="color:#1c7edc;">Evolution of received grants according to activityType and year</h2>', unsafe_allow_html=True)
activity_type_grants_by_year = participants_df.groupby(["year", "activityType"])["Total_Grants_Received"].sum().unstack().fillna(0)
st.bar_chart(activity_type_grants_by_year)


# Extra: Displaying list/stats of projects according to the project keywords
keywords = st.multiselect("Select project keywords to filter:", options=['AI', 'IoT', 'Big Data', 'Cloud', 'Security'])
filtered_projects_df = pd.read_sql_query("SELECT * FROM Projects", conn)

if keywords:
    filtered_projects_df = filtered_projects_df[filtered_projects_df["objective"].apply(lambda x: any(kw in x for kw in keywords))]

st.markdown('<h2 style="color:#1c7edc;">Filtered Projects List</h2>', unsafe_allow_html=True)
st.write(filtered_projects_df)

# Closing the connection
conn.close()
