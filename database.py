import pandas as pd

project_database= pd.DataFrame(
    columns=['id','title','project_description','classification',
             'date','time','reward','candidate_description',
             'max_number','contact_name','contact_licence_number',
             'contact_infomation', 'project_creator_id', 
             'current_participant_number', 'project_participants']
    )
project_database.to_csv('project_database.csv', index=False)

user_info = pd.DataFrame(
    columns=['id','name','academy','licence_number','contact_information']
)
user_info.set_index('id', inplace=True)
user_info.to_csv('users_info.csv', index=False)