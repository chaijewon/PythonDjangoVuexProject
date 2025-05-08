from django.db import models

# Create your models here.
import oracledb as db

def getConnection():
    try:
         conn=db.connect("hr/happy@localhost:1521/XE")
    except Exception as e:
         print(e)
    return conn
def disConnection(conn,cur):
    try:
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
def foodListData(page):
    try:
         rowSize=12
         start=(rowSize*page)-(rowSize-1)
         end=rowSize*page

         #연결
         conn=getConnection()
         cur=conn.cursor() #cursor = PreparedStatement
         #SQL문장 전송
         sql=f"""
                SELECT fno,name,poster,num 
                FROM (SELECT fno,name,poster,rownum as num
                FROM (SELECT fno,name,poster 
                FROM project_food ORDER BY fno ASC))
                WHERE num BETWEEN {start} AND {end}
              """
         cur.execute(sql)
         food_list=cur.fetchall()
         cur.close()
         sql="SELECT CEIL(COUNT(*)/12.0) FROM project_food"
         cur=conn.cursor()
         cur.execute(sql)
         total=cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        disConnection(conn,cur)
    # 데이터베이스 값을 읽는 경우 => dict (100,)
    # 파이썬은 리턴값을 여러개 전송이 가능
    return food_list,total[0]

#상세보기
def foodDetailData(fno):
    try:
         conn=getConnection()
         cur=conn.cursor()
         sql=f"""
               SELECT fno,name,poster,score,
               address,phone,
               parking,time,type,theme,content
               FROM project_food 
               WHERE fno={fno}
              """
         cur.execute(sql)
         food_detail=cur.fetchone() #(1,1,2,2,2,2,2)
         #clob처리 => String(CLOB => InputStream)
         #9i 10g ... 21c
         content=''.join(food_detail[-1].read())
         theme=''.join(food_detail[-2].read())
    except Exception as e:
        print(e)
    finally:
        disConnection(conn,cur)

    return food_detail,content,theme

