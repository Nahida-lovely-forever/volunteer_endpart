from django.http.response import JsonResponse
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
import requests
import json
import pandas as pd
url = ''

# 前端获得全部项目数据
@require_http_methods(["GET"])
def get_projects(request):
    project_database = pd.read_csv('.//project_database.csv')
    list_zhi=[]
    list_xue=[]
    list_qi=[]
    for index, row in project_database.iterrows():
        if row['classification'] == '志愿者招募':
            list_zhi.append(project_database.iloc[index].to_dict())
        elif row['classification'] == '学术支持':
            list_xue.append(project_database.iloc[index].to_dict())
        elif row['classification'] == '其他':
            list_qi.append(project_database.iloc[index].to_dict())
    data = [
        list_zhi,list_xue,list_qi
    ]
    return JsonResponse(data, safe=False)


# 前端创建新项目数据传回后端
@require_http_methods(["POST"])
def create_project(request):
    project_database = pd.read_csv('./project_database.csv')
    with open('./num_variable.txt', 'r') as f:
        id = int(f.read())
    data = json.loads(request.body)
    project_database.loc[id] = [
        id,
        data.get("title"),
        data.get("project_description"),
        data.get("classification"),
        data.get("date"),
        data.get("time"),
        data.get("reward"),
        data.get("candidate_description"),
        data.get("max_number"),
        data.get("contact_name"),
        data.get("contact_licence_number"),
        data.get("contact_infomation"), 
        data.get("project_creator_id"),
        0,
        []
    ]
    project_database.to_csv('project_database.csv', index=False)
    id += 1
    with open('./num_variable.txt', 'w') as f:
        f.write(str(id))
    return HttpResponse(1)

# 前端传入code，后端传回openid用户唯一标识id
@require_http_methods(["POST"])
def get_openid(request):
    code = json.loads(request.body)['code']
    appid = 'wx6b268c7e68efd73a'
    secret = '419f8f5e5623d207e92276c046b353e0'
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code"
    response = requests.get(url)
    result = response.json()
    openid = result.get('openid')
    return HttpResponse(openid)

# 前端用户删除创建的项目
@require_http_methods(["POST"])
def drop_project(request):
    project_id = json.loads(request.body)['project_id']
    project_database = pd.read_csv('./project_database.csv')
    project_database = project_database[project_database['id'] != project_id]
    project_database.to_csv('./project_database.csv', index=False)
    return HttpResponse(1)

# 判断用户是否登录
@require_http_methods(["POST"])
def get_basic_info(request):
    print(json.loads(request.body))
    user_id = json.loads(request.body)['user_id']
    user_info=pd.read_csv('./users_info.csv')
    user_info_dict = user_info.set_index('id').T.to_dict()
    print(user_info_dict)
    if user_id in user_info_dict:
        return JsonResponse(user_info_dict[user_id], safe=False)
    else:
        return JsonResponse({}, safe=False)
    
# 前端用户填写基本信息传入后端
@require_http_methods(["POST"])
def basic_infomation(request):
    data = json.loads(request.body)
    
    users_info=pd.read_csv('./users_info.csv')
    
    users_info.loc[len(users_info)] = [
        data.get("user_id"),
        data.get("name"),
        data.get("academy"),
        int(data.get("licence_number")),
        int(data.get("contact_infomation")),
        ""
    ]
    users_info=users_info.drop_duplicates(subset=['id'], keep='last')
    users_info.to_csv('./users_info.csv', index=False)
    return HttpResponse(1)

#某人参加某一项目

#某人退出某一项目

#列出某人曾经参与过的项目

#列出某人曾经创建过的项目

#将某一项目归档

