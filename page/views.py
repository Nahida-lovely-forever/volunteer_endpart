from django.http.response import JsonResponse
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
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
        data.get("contact_phone_number")
    ]
    project_database.to_csv('project_database.csv', index=False)
    id += 1
    with open('./num_variable.txt', 'w') as f:
        f.write(str(id))
    return HttpResponse(1)
