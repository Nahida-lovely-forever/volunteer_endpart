import pandas as pd
####################################
#不要运行本文件,本文件用于初始化数据库#
####################################
project_database= pd.DataFrame(
    columns=['user_id','title','project_description','classification',
             'date','time','reward','candidate_description',
             'max_number','contact_name','contact_licence_number',
             'contact_infomation', 'project_creator_id', 
             'current_participant_number',]
    )
project_database.to_csv('project_database.csv', index=False)

