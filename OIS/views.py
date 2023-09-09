import email
import json
import os
from select import select
import tempfile
from types import NoneType
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import django.contrib.staticfiles
from .form import SubCatMasterForm, UOMMasterForm, CatMasterForm, UserCompMasterForm
from .models import SubCatMaster, UOMMaster, CategoryMaster,UserCompMaster
from django.views.decorators.csrf import csrf_exempt
import sqlite3
from django.contrib.auth.models import User
from django.template import loader
# Create your views here.
class ViewClass:
    max=0
    file=0
    uid=0
    def __init__(self):
        max=0#max id for uom #used for incremental purpose

    def billscreen(request):
        page=loader.get_template("BillScreen.html")
        #print(f'uid is {request.POST["uid"]}')
        context={
            'uid':'3'#request.POST['uid']
        }
        return HttpResponse(page.render(context,request))

    def categorymaster(request):
        page=loader.get_template("Category Master.html")
        print(f'uid is {request.POST["uid"]}')
        context={
            'uid':request.POST['uid']
        }
        return HttpResponse(page.render(context,request))

    def companymaster(request):
        return render(request,"Company master.html")

    def login(req):
        return render(req,"Login.html")

    def productmaster(req):
        page=loader.get_template("Productmaster.html")
        print(f'uid is {req.POST["uid"]}')
        context={
            'uid':req.POST['uid']
        }
        return HttpResponse(page.render(context,req))

    def subcategory(req):
        page=loader.get_template("Subcat.html")
        print(f'uid is {req.POST["uid"]}')
        userid=req.POST['uid']
        file=f'userdb//dbof{userid}//user{userid}.sqlite3'
        dbcon=sqlite3.connect(file)
        cursur=dbcon.cursor()
        result=cursur.execute("SELECT category_name FROM category")
        dbcon.commit()
        data=[i[0] for i in result]
        print(data)
        cursur.close()
        dbcon.close()
        dbcon=sqlite3.connect("db.sqlite3")
        cursor=dbcon.cursor()
        subcatlist=cursor.execute("SELECT * FROM OIS_defcatsubcat")
        dbcon.commit()
        subcatlist=[i for i in subcatlist]
        subcatlist={
            subcatlist[0][1]:subcatlist[0][2].split(","),
            subcatlist[1][1]:subcatlist[1][2].split(","),
            subcatlist[2][1]:subcatlist[2][2].split(","),
            subcatlist[3][1]:subcatlist[3][2].split(","),
            subcatlist[4][1]:subcatlist[4][2].split(","),
            subcatlist[5][1]:subcatlist[5][2].split(","),
        }
        print([i for i in subcatlist.values()])
        context={
            'uid':req.POST['uid'],
            'datalist':data,
            'subcatlist':json.dumps(subcatlist),
        }
        return HttpResponse(page.render(context,req))

    def uom(req):
        page=loader.get_template("UOM.html")
        #print(f'uid is {req.POST["uid"]}')
        context={
            'uid':'3'#req.POST['uid']
        }
        return HttpResponse(page.render(context,req))

    def usermaster(req):
        return render(req,"UserMaster.html")

    def nav(req):
        return render(req,"nav.html")

    def index(req):
        return render(req,"homepage.html")


    #data model views
    def userform(req):
        if req.method == 'POST':
            form=UserCompMasterForm(req.POST)
            print(req.POST)
            if form.is_valid() and req.POST.get('isadmin')=='0':
                form.save()
                print("data saved")
                user=UserCompMaster.objects.get(email=req.POST['email'])
            else:
                User.objects.create_superuser(username=req.POST['name'], 
                password=req.POST['password'], email=req.POST['email'], is_staff=True, is_active=True, is_superuser=True)
                print("admin added succesfully")
            page=loader.get_template('Login.html')
            context ={"userid":user.id,}
            return HttpResponse(page.render(context, req))
            #return HttpResponseRedirect('/login/')

    def userretrive(req):
        userid=req.POST['userid']
        password=req.POST['password']
        try:
            user=UserCompMaster.objects.get(email=userid)   
        except UserCompMaster.DoesNotExist:
            return HttpResponse("user not found",content_type='text/plain')
        if user:
            if user.password == password:
                if user.userfirst:
                    #creating seperate database file individual user
                    os.mkdir(f'userdb//dbof{user.id}')
                    file=f'userdb//dbof{user.id}//user{user.id}.sqlite3'
                    uid=str(user.id)
                    with open(file,'w') as f:
                        pass
                    dbcon=sqlite3.connect('db.sqlite3')
                    cursur=dbcon.cursor()
                    cursur.execute(f"UPDATE OIS_usercompmaster SET userfirst=0 WHERE id={user.id}")
                    dbcon.commit()
                    cursur.close()
                    dbcon.close()
                    #return HttpResponseRedirect('/companymaster/')
                    page=loader.get_template('Company master.html')
                    context ={
                        "userid":user.id,
                    }
                    return HttpResponse(page.render(context, req))
                else:
                    page=loader.get_template('Dashboard.html')
                    context={"userid":user.id,}
                    return HttpResponse(page.render(context,req))
            else:
                return HttpResponse("password incorrect")

    def commasterform(req):
        if req.method == 'POST':
            print(req.POST)
            compname=req.POST.get('companyname')
            address=req.POST.get('address')+", "+req.POST.get('address2')
            pincode=req.POST.get('pincode')
            state=req.POST.get('state')
            city=req.POST.get('city')
            gstin=req.POST.get('gstin')
            uid=req.POST.get('uid')
            data=[compname, address, pincode, state, city, gstin,uid]
            dbcon=sqlite3.connect('db.sqlite3')
            cursur=dbcon.cursor()
            cursur.execute('UPDATE OIS_usercompmaster SET companyname=?,address=?,pincode=?,state=?,city=?,gstin=? WHERE id=?',data)
            dbcon.commit()
            cursur.close()
            dbcon.close()
            return HttpResponseRedirect('/dashboard/')

    @csrf_exempt
    def catmasterform(req):
        if req.method == 'POST':
            data=json.loads(req.body.decode('utf-8'))
            print(data)
            userid=data[0]
            del data[0]
            file=f'userdb//dbof{userid}//user{userid}.sqlite3'
            try:
                dbcon=sqlite3.connect(file)
            except(Exception):
                os.mkdir(f'userdb//dbof{userid}')
                file=f'userdb//dbof{userid}//user{userid}.sqlite3'    
                with open(file,'w') as f:
                    pass
                dbcon=sqlite3.connect(file)
                cursur=dbcon.cursor()
                cursur.execute('CREATE TABLE category (id INTEGER PRIMARY KEY AUTOINCREMENT, category_name TEXT UNIQUE NOT NULL,active INTEGER )')
                dbcon.commit()
                cursur.close()
            try:
                cursur=dbcon.cursor()
                cursur.execute("INSERT INTO category (category_name,active) VALUES(?,?)",data)
                dbcon.commit()
                
            except(sqlite3.IntegrityError):
                print("Integrity error occured")
                cursur.execute("UPDATE category set active=? WHERE category_name=?",[data[1],data[0]])
                dbcon.commit()
            cursur.close()
            dbcon.close()
            return HttpResponseRedirect('/')

    @csrf_exempt
    def subcatmasterform(req):
        if req.method == 'POST':
            data=json.loads(req.body)
            print(data)
            userid=data.pop(0)
            file=f'userdb//dbof{userid}//user{userid}.sqlite3'
            dbcon=sqlite3.connect(file)
            cursur=dbcon.cursor()
            try:
                cursur.execute("INSERT INTO catandsubcats (category_name,subcategory_name,active) VALUES(?,?,?)",data)
                dbcon.commit()
                cursur.close()
                dbcon.close() 
            except(sqlite3.IntegrityError):
                cursur.execute("UPDATE catandsubcats set active=? WHERE subcategory_name=?",[data[-1],data[-2]])
                dbcon.commit()
                cursur.close()
                dbcon.close()
            except(sqlite3.OperationalError):    
                cursur.execute("CREATE TABLE catandsubcats (id INTEGER PRIMARY KEY AUTOINCREMENT, category_name TEXT NOT NULL,subcategory_name TEXT UNIQUE NOT NULL,active INTEGER)")
                cursur.execute("INSERT INTO catandsubcats (category_name,subcategory_name,active) VALUES(?,?,?)",data)
                dbcon.commit()
                cursur.close()
                dbcon.close() 
            finally:
                print("data saved")
            return HttpResponseRedirect('/')
    
    @csrf_exempt
    def uommasterform(req):
        if req.method == 'POST':
            data=json.loads(req.body.decode("utf-8"))
            print(data)
            dbcon=sqlite3.connect('db.sqlite3')
            cursur=dbcon.cursor()
            res=cursur.execute('select MAX(id) from OIS_uommaster')
            for i in res:
                try:
                    max=int(i[0])
                except:
                    max=0
            for i in range(len(data)):
                max+=1
                data[i][0]= max
            print("modified data is")
            print(data)
            cursur.executemany("INSERT INTO OIS_uommaster VALUES(?,?,?)",data)
            dbcon.commit()
            cursur.close()
            dbcon.close()
        return HttpResponseRedirect('/uom')

    def prodmasterform(req):
        if req.method == 'POST':
            print(req.POST)
            return HttpResponseRedirect('/billscreen')

    def dashboardform(req):
        return render(req,"Dashboard.html")

    def logout(req):
        #return HttpResponse('<scripts>alert("done")</scripts>', content_type="application/x-javascript")
        return HttpResponseRedirect("/")