from django.shortcuts import render
from web import models
# Create your views here.
from django.http import JsonResponse
# @RestController

def foodListData(request):
    page=request.GET['page'] # params:{page:1}
    # 문자열 => str
    curpage=int(page)
    # 데이터베이스 연동
    food_list,totalpage=models.foodListData(curpage)
    # Tuple (...) => Dict변경 (JSON)

    fd=[]
    for f in food_list:
        ff={"fno":f[0],"name":f[1],"poster":f[2]}
        fd.append(ff)
    BLOCK=10
    startPage=((curpage-1)//BLOCK*BLOCK)+1
    endPage = ((curpage - 1) // BLOCK * BLOCK) + BLOCK

    if endPage>totalpage:
        endPage=totalpage

    list={
        "fd":fd,
        "curpage":curpage,
        "totalpage":totalpage,
        "startPage":startPage,
        "endPage":endPage
    }
    # food_list:{}
    return JsonResponse(list)





