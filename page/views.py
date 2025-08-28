from django.http.response import JsonResponse
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
import requests
import json
import pandas as pd
url = ''


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

@require_http_methods(["POST"])
def get_openid(request):
    print(json.loads(request.body))
    code = json.loads(request.body)['code']
    appid = 'wx6b268c7e68efd73a'
    secret = '419f8f5e5623d207e92276c046b353e0'
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code"
    response = requests.get(url)
    result = response.json()
    openid = result.get('openid')
    return HttpResponse(openid)
