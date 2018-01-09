#!/usr/bin/python3

from flask import Flask, render_template, request
import requests,bs4,sqlite3
import matplotlib.pyplot as plt
import math
import turtle
from triangle import triangle
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('search.html')
@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    else:
        name = request.form['id'] 
        if name == 'puzzle':
            return render_template('puzzle.html')
        elif name == 'mooc':
            return render_template('mooc.html')
        elif name == 'triangle':
            return render_template('triangle.html')
        else:
            return render_template('search.html')

@app.route("/filters",methods=['POST', 'GET'])
def filters():
    if request.method == 'GET':
        return render_template('search.html')
    else:
        score=request.form['score']
        if int(score) not in range(1,10):
            return render_template('validator.html')
        else:
            url="http://oscar-lab.org/puzzle.html"
            req=requests.get(url)
            soup=bs4.BeautifulSoup(req.text)
            tbody=soup.table.tbody
            con = sqlite3.connect("puzzle.db")
            cursor = con.cursor()
            cursor.execute("drop table if exists puzzle")
            cursor.execute("create table if not exists puzzle (id integer primary key,IDs text,Score text,Title text)")

            for tr in tbody.find_all("tr"):
                if tr.find_all("td")[1].text==str(score):
                    IDs=tr.find_all("td")[0].text
                    Score=tr.find_all("td")[1].text
                    Title=tr.find_all("td")[2].a.text
                    print("%s\n%s\n%s" % (IDs,Score,Title))
                    cursor.execute("insert into puzzle (IDs, Score, Title) values (?, ?, ?)", (IDs, Score, Title))
        
            con.commit()
            con.close()
            return render_template('finish.html')

@app.route("/mooc",methods=['POST', 'GET'])
def mooc():
    if request.method == 'GET':
        return render_template('search.html')
    else:
        classname = request.form['classes']
        url="https://deathwingi.github.io/"
        req=requests.get(url)
        soup=bs4.BeautifulSoup(req.text)
        table=soup.body.table
        flag=False
        for tr in table.find_all("tr"):
            if tr.find_all("td")[4].text==classname:
                flag=True
        if flag ==False:
            return render_template('validator.html')
        else:  
            con = sqlite3.connect("mooc.db")
            cursor = con.cursor()
            cursor.execute("drop table if exists mooc")
            cursor.execute("create table if not exists mooc (id integer primary key,area text,time text,sno text,classes text,cnum text,cno text,cname text)")
            fname="mooc.csv"
            handle=open(fname,"w")
            line='"'+"地点"+'","'+"时间"+'","'+"学号"+'","'+"班级"+'","'+"课程号"+'","'+"课序号"+'","'+"课程名"+'"\n'
            handle.writelines(line)
            for tr in table.find_all("tr"):
                if tr.find_all("td")[4].text==classname:
                    area=tr.find_all("td")[1].text
                    time=tr.find_all("td")[2].text
                    sno=tr.find_all("td")[3].text
                    classes=tr.find_all("td")[4].text
                    cnum=tr.find_all("td")[5].text
                    cno=tr.find_all("td")[6].text
                    cname=tr.find_all("td")[7].text
                    print("%s\n%s\n%s\n%s\n%s\n%s\n%s" % (area,time,sno,classes,cnum,cno,cname))
                    cursor.execute("insert into mooc (area,time,sno,classes,cnum,cno,cname) values (?, ?, ?,?,?,?,?)", (area,time,sno,classes,cnum,cno,cname))
                    line='"'+area+'","'+time+'","'+sno+'","'+classes+'","'+cnum+'","'+cno+'","'+cname+'"\n'
                    handle.writelines(line)  
                con.commit()
            handle.close()
            classlist=['软件1510','软件1511','软件1512',
               '软件1513','软件1514','软件1515','软件1516']
            nums=[0,0,0,0,0,0,0]
            for i in range(0,7):
                for tr in table.find_all("tr"):
                    if tr.find_all("td")[4].text==classlist[i]:
                        nums[i]+=1
            fig,ax=plt.subplots()
            ax.plot(classlist,nums)
            ax.grid()
            fig.savefig("1510-1516尔雅考试人数.png")
            con.close()
        return render_template('finish.html')

@app.route("/drawTriangle",methods=['POST', 'GET'])
def drawTriangle():
    if request.method == 'GET':
        return render_template('search.html')
    else:
        a=int(request.form['a'])
        b=int(request.form['b'])
        c=int(request.form['c'])
        if a<10:
            a=a*10
            b=b*10
            c=c*10
        if(a+b>c and b+c>a and a+c>b):
            x=triangle(a,b,c)
            x.draw()
            t=turtle.Pen()
            t.forward(a)
            t.left(180-x.B)
            t.forward(c)
            t.left(180-x.A)
            t.forward(b)
            ts = turtle.getscreen()
            ts.getcanvas().postscript(file="triangel.ps")
        else:
            return render_template('validator.html')
        return render_template('drawFinish.html')

    
