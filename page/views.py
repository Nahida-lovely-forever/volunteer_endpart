from django.http.response import JsonResponse
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings
import requests
import json
import pandas as pd
import ast 
import os
import base64
url = ''

# 前端获得全部项目数据 
@require_http_methods(["GET"])
def get_projects(request):
    project_database = pd.read_csv('.//project_database.csv')
    list_zhi=[]
    list_xue=[]
    list_qi=[]
    with open('project_participants.json', 'r', encoding='utf-8') as f:
        project_participants = json.load(f)
    for index, row in project_database.iterrows():
        if row['classification'] == '志愿者招募':
            current_project = project_database.iloc[index].to_dict()
            current_project['project_participants'] = project_participants[current_project['project_id']]
            list_zhi.append(current_project)
        elif row['classification'] == '学术支持':
            current_project = project_database.iloc[index].to_dict()
            current_project['project_participants'] = project_participants[current_project['project_id']]
            list_zhi.append(current_project)
        elif row['classification'] == '其他':
            current_project = project_database.iloc[index].to_dict()
            current_project['project_participants'] = project_participants[current_project['project_id']]
            list_zhi.append(current_project)
    data = [
        list_zhi,list_xue,list_qi
    ]
    return JsonResponse(data, safe=False)


# 前端创建新项目数据传回后端
@require_http_methods(["POST"])
def create_project(request):
    project_database = pd.read_csv('./project_database.csv')
    with open('./num_variable.txt', 'r') as f:
        project_id = int(f.read())
    data = json.loads(request.body)
    project_database.loc[id] = [
        project_id,
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
        0
    ]
    project_database.to_csv('project_database.csv', index=False)
    with open('project_participants.json', 'r', encoding='utf-8') as f:
        project_participants = json.load(f)
    project_participants[project_id] = []
    with open('project_participants.json', 'w', encoding='utf-8') as f:
        json.dump(project_participants, indent=4)
    project_id += 1
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

# 前端用户删除创建的项目    要给参加用户发通知
@require_http_methods(["POST"])
def drop_project(request):
    project_id = json.loads(request.body)['project_id']
    project_database = pd.read_csv('./project_database.csv')
    project_database = project_database[project_database['id'] != project_id]
    project_database.to_csv('./project_database.csv', index=False)
    with open('project_participants.json', 'r', encoding='utf-8') as f:
        project_participants = json.load(f)
    del project_participants[project_id]
    with open('project_participants.json', 'w', encoding='utf-8') as f:
        json.dump(project_participants, indent=4)
    return HttpResponse(1)

# 获取用户头像
@require_http_methods(["POST"])
def get_user_avatar(request):
    base64_data = str(json.loads(request.body)['image'])
    users_info=pd.read_csv('./users_info.csv')
    users_info.loc[users_info['id'] == request.GET.get('user_id'), 'avatar'] = base64_data
    users_info.to_csv('./users_info.csv', index=False)
    return HttpResponse(base64_data)


# 获取用户基本信息
@require_http_methods(["GET"])
def get_basic_info(request):
    user_id = request.GET.get("user_id")
    user_info=pd.read_csv('./users_info.csv')
    user_info_dict = user_info.set_index('id').T.to_dict()
    if user_id in user_info_dict:
        res_dict = {}
        res_dict["name"] = user_info_dict[user_id]["name"]
        res_dict["academy"] = user_info_dict[user_id]["academy"]
        res_dict["licence_number"] = user_info_dict[user_id]["licence_number"]
        res_dict["contact_information"] = user_info_dict[user_id]["contact_information"]
        res_dict["avatar"] = user_info_dict[user_id]["avatar"]
        return JsonResponse(res_dict)
    else:
        return JsonResponse({})
    
# 前端用户填写基本信息传入后端
@require_http_methods(["POST"])
def basic_infomation(request):
    data = json.loads(request.body)
    users_info=pd.read_csv('./users_info.csv')
    users_info.loc[len(users_info)] = [
        data.get("user_id"),
        data.get("name"),
        data.get("academy"),
        data.get("licence_number"),
        data.get("contact_infomation"),
        data.get("avatar"),
    ]
    users_info=users_info.drop_duplicates(subset=['id'], keep='last')
    users_info.to_csv('./users_info.csv', index=False)
    return HttpResponse(1)

# 用户参加项目  #####
@require_http_methods(["POST"])
def attend_project(request):
    user_id = request.GET.get("user_id")
    project_id = request.GET.get("project_id")
    project_database = pd.read_csv('./project_database.csv',dtype={'id': str})
    participants_value=project_database.loc[project_database['id'] == project_id, 'project_participants'].values[0]
    print(participants_value)
    try:
        attendentlist = ast.literal_eval(participants_value)
    except (ValueError, SyntaxError):
        attendentlist = [] 
    ######################
    print(attendentlist)
    print(user_id)
    print(project_id)
    ######################
    if user_id not in attendentlist:
        attendentlist.append(user_id)
        
        ####################
        print(project_database)
        print(project_database.iloc[0]['id'])
        print(project_database[project_database['id'] == project_id])
        print(len(project_database[project_database['id'] == project_id]['current_participant_number']))
        print(project_database[project_database['id'] == project_id]['current_participant_number'])
        ####################

        currnum=project_database[project_database['id'] == project_id]['current_participant_number'].iloc[0]
        ####################
        print(attendentlist)
        print(currnum)
        ####################
        
        project_database.loc[project_database['id'] == project_id, 'current_participant_number'] = currnum + 1
        
        ###########################
        print(project_database.loc[project_database['id'] == project_id, 'current_participant_number'])
        #######################
        
        project_database.loc[project_database['id'] == project_id, 'project_participants'] = attendentlist
        #######
        print(project_database.loc[project_database['id'] == project_id, 'project_participants'])
        print(project_database)
        #######
    else:
        pass
    project_database.to_csv('./project_database.csv', index=False)
    return HttpResponse(1)

















#某人退出某一项目
@require_http_methods(["POST"])
def quit_project(request):
    user_id = request.GET.get("user_id")
    project_id = request.GET.get("project_id")
    project_database = pd.read_csv('./project_database.csv',dtype={'id': str})
    participants_value=project_database.loc[project_database['id'] == project_id, 'project_participants'].iloc[0]
    if isinstance(participants_value, str):
        attendentlist = ast.literal_eval( participants_value)  # Safely convert string to list
    else:
        attendentlist =  participants_value
    if user_id in attendentlist:
        attendentlist.remove(user_id)
        currnum=project_database[project_database['id'] == project_id]['current_participant_number'].iloc[0]
        project_database.loc[project_database['id'] == project_id, 'current_participant_number'] = currnum - 1
        project_database.loc[project_database['id'] == project_id, 'project_participants'] = attendentlist
    else:
        pass
    project_database.to_csv('./project_database.csv', index=False)
    return HttpResponse(1)

#列出某人曾经参与过的项目
@require_http_methods(["GET"])
def list_attended_projects(request):
    user_id = request.GET.get("user_id")
    project_database = pd.read_csv('./project_database.csv',dtype={'id': str})
    attended_projects = project_database[project_database['project_participants'].apply(lambda x: user_id in ast.literal_eval(x) if isinstance(x, str) else x)]
    return JsonResponse(attended_projects.to_dict(orient='records'), safe=False)

#列出某人曾经创建过的项目
@require_http_methods(["GET"])
def list_created_projects(request):
    user_id = request.GET.get("user_id")
    project_database = pd.read_csv('./project_database.csv',dtype={'id': str})
    created_projects = project_database[project_database['project_creator_id'] == user_id]
    return JsonResponse(created_projects.to_dict(orient='records'), safe=False)

#将某一项目归档
@require_http_methods(["POST"])
def archive_project(request):
    project_id = request.GET.get("project_id")
    project_database = pd.read_csv('./project_database.csv',dtype={'id': str})
    project_database.loc[project_database['id'] == project_id, 'status'] = 'archived'
    project_database.to_csv('./project_database.csv', index=False)
    return HttpResponse(1)
