import pandas as pd
user_info = pd.DataFrame(
    columns=['id','name','academy','licence_number','contact_information','avatar']
)
user_info.set_index('id')
user_info.to_csv('users_info.csv', index=False)