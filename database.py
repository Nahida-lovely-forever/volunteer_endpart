import pandas as pd
import numpy as np

project_database= pd.DataFrame(
    columns=['id','title','project_description','classification',
             'date','time','reward','candidate_description',
             'max_number','contact_name','contact_licence_number',
             'contact_phone_number', 'current_participant_number']
    )
project_database.to_csv('project_database.csv', index=False)