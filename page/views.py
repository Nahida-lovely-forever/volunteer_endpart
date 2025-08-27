from django.http.response import JsonResponse
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
import json

url = ''


@require_http_methods(["GET"])
def get_projects(request):
    data = [
        [
            {
                "title": "统计与数据科学学院更名暨大数据研究院成立大会",
                "time": "7月10日",
                "location": "上海财经大学创业中心一楼报告厅",
                "reward": "校级学术二课"
            },
            {
                "title": "上海图书馆淮海路馆志愿者招募",
                "time": "6月28日  9:00-16:30",
                "location": "上海市徐汇区淮海中路1555号",
                "reward": "第二课堂志愿服务时长记录8h"
            },
            {
                "title": "上海图书馆淮海路馆志愿者招募",
                "time": "6月29日  9:00-16:30",
                "location": "上海市徐汇区淮海中路1555号",
                "reward": "第二课堂志愿服务时长记录8h"
            }
        ],
        [],
        []
    ]
    return JsonResponse(data, safe=False)


@require_http_methods(["POST"])
def create_project(request):
    print(json.loads(request.body))
    return HttpResponse(1)
