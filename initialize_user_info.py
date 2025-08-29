import pandas as pd
#############################################
#不要运行本文件， 本文件用于初始化用户信息数据库#
#############################################
user_info = pd.DataFrame(
    columns=['id','name','academy','licence_number','contact_information','avatar']
)
user_info.set_index('id')
user_info.to_csv('users_info.csv', index=False)