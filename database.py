import pandas as pd
import numpy as np

project_database= pd.DataFrame(
    columns=['id','pname','description','type',
             'time','reward','required_personal',
             'maxnum','contact_name','contact_id',
             'contact_phone']
    )
project_database.to_csv('project_database.csv', index=False)