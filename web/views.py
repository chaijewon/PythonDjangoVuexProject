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
    #[]
    list={
        "fd":fd,
        "curpage":curpage,
        "totalpage":totalpage,
        "startPage":startPage,
        "endPage":endPage
    }
    # food_list:{}
    return JsonResponse(list)

def foodDetailData(request):
    no=request.GET['fno']
    fno=int(no)
    fd,content,theme=models.foodDetailData(fno)
    """
     fno,name,poster,score,
     address,phone,
     parking,time,type,theme,content 
    """
    f = {
      "fno":fd[0],
      "name":fd[1],
      "poster":fd[2],
      "score":fd[3],
      "address":fd[4],
      "phone":fd[5],
      "parking":fd[6],
      "time":fd[7],
      "type":fd[8],
      "theme":theme,
      "content":content
    }
    return JsonResponse(f)
