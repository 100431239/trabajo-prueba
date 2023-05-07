import pandas as pd
import sqlite3

#FR2.1: Read the 3 previous EXCEL files and generate 3 dataframes corresponding to the EXCEL tables.
projects_df = pd.read_excel('projects.xlsx')
participants_df = pd.read_excel('participants.xlsx')
countries_df = pd.read_excel('countries.xlsx')

#FR2.2: Save in disk the generated a new database (ecsel_database.db)
conn = sqlite3.connect('ecsel_database.db')

#FR2.3: Add 3 new tables in the database (ecsel_database.db), corresponding to the 3 dataframes (only if thew don't exist previously).
projects_df.to_sql('Projects', conn, if_exists='replace', index=False)
participants_df.to_sql('Participants', conn, if_exists='replace', index=False)
countries_df.to_sql('Countries', conn, if_exists='replace', index=False)

#Creating the foreign key constraint between Projects and Participants
conn.execute('''CREATE TRIGGER IF NOT EXISTS fk_Participants_Projects
                    BEFORE INSERT ON Participants
                    FOR EACH ROW
                    BEGIN
                    SELECT CASE
                    WHEN ((SELECT projectID FROM Projects WHERE projectID = NEW.ProjectID) IS NULL)
                    THEN RAISE(ABORT, 'Foreign Key Violation: ProjectID does not exist')
                    END;
                END;''')

#Creating the foreign key constraint between Participants and Countries
conn.execute('''CREATE TRIGGER IF NOT EXISTS fk_Participants_Countries
                    BEFORE INSERT ON Participants
                    FOR EACH ROW
                    BEGIN
                    SELECT CASE
                    WHEN ((SELECT Acronym FROM Countries WHERE Acronym = NEW.Country_Acronym) IS NULL)
                    THEN RAISE(ABORT, 'Foreign Key Violation: Country Acronym does not exist')
                    END;
                END;''')

#Committing the changes and closing the connection
conn.commit()
conn.close()