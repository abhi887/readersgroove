import sqlalchemy
import requests
import builtins
import os

from flask import Flask,render_template,request,g
from jinja2 import FileSystemLoader, Environment
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker,Session

#check enviornment variable as DATABASE_URL
#if not os.getenv("DATABASE_URL"):
 #   raise RuntimeError("DATABASE_URL is not set.")

DATABASE_URL1="postgres://pvafpuicceyeuo:9a6e52cb4957fe1966be29c94401bf235315aece1e9d0de4985678d94b5ca971@ec2-54-225-116-36.compute-1.amazonaws.com:5432/da86qhnm34n7bf"
DATABASE_URL2="postgres://hbyzaoahbxtegi:4bcf0e4d660fbc7bdafd746acfd8ef37c84669841fb51de297788cd5f3e88b89@ec2-50-19-109-120.compute-1.amazonaws.com:5432/dc83bdr6ov3m0e"

#create engine
engine=create_engine(DATABASE_URL1)
#engine=create_engine(os.getenv("DATABASE_URL"))
db=scoped_session(sessionmaker(bind=engine))

engine2=create_engine(DATABASE_URL2)
db2=scoped_session(sessionmaker(bind=engine2))

app=Flask(__name__)

#configuring app
app.config["SESSION_PERMENANT"]=False
app.config["SESSION_TYPE"]="filesystem"
app.static_folder='static'
Session(app)
global usrnm

env = Environment(loader=FileSystemLoader(searchpath='/templates'))
bookhtml = env.get_template('book.html')
emptyresulthtml = env.get_template('emptyresult.html')
loginhtml= env.get_template('login.html')
reloginhtml = env.get_template('relogin.html')
resignuphtml = env.get_template('resignup.html')
resulthtml = env.get_template('result.html')
signuphtml = env.get_template('signup.html')
userlghtml = env.get_template('userlg.html')


@app.route("/")
def index():
    return loginhtml

@app.route("/signup",methods=["GET","POST"])
def signup():
    try:
        return render_template("signup.html")
    except sqlalchemy.exc.OperationalError:
        return render_template("relogin.html", cerror=True)
        #return "Sorry but our site is currently not available. try again later."

@app.route("/ssignup",methods=["PUT","POST"])
def ssignup():
    try:
        #render_template("signup.html")
        dob=request.form.get("dob")
        sex=request.form.get("sex")
        email=request.form.get("email")
        fname=request.form.get("fname")
        lname=request.form.get("lname")
        password=request.form.get("password")
        check2=True
        if dob=='':
            check2=False
        elif sex=='':
            check2 = False
        elif email=='':
            check2 = False
        elif fname=='':
            check2 = False
        elif lname=='':
            check2 = False
        elif password=='':
            check2 = False
        if check2 == False:
            return render_template("resignup.html",signuped="Please fill in all the fields")
        check = list(db.execute("select email from persona where email=:email", {"email": email}))
        if check[0][0]== None:
            nessenid = list(db.execute("select max(nessid) from nessen;"))
            db.execute("insert into nessen values(default,:dob,:sex);", {"dob": dob, "sex": sex})
            db.execute("insert into persona values(:fname,:lname,:email,:nessenid)",{"email":email,"fname":fname,"lname":lname,"nessenid":nessenid[0][0]})
            db.execute("insert into secper values(:nessenid,:email,:password)",{"nessenid":nessenid[0][0],"email":email,"password":password})
            db.commit()
            return render_template("resignup.html",signuped="Congratulations ! you are now signed up on the Readers Groove.</br>Login using your credentials to countinue")
            #return "Congratulations ! you are now signed up on the Readers Groove."
        else :
            return render_template("resignup.html",wemail=email,signuped=None)
    except sqlalchemy.exc.OperationalError: # for connection error
        return render_template("relogin.html", cerror=True)
        #return "Sorry but our site is currently not available. try again later."
@app.route("/login")
def login():
    try:
        return render_template("login.html")
    except sqlalchemy.exc.OperationalError:
        return render_template("relogin.html", cerror=True)

@app.route("/slogin",methods=["POST","GET"])
def slogin():
    if request.method=='GET':
        return render_template("login.html")
    try:
        global usrnm,email
        email=request.form.get("username")
        pschek=list(db.execute("select pass from secper where email=:email",{"email":email}))
        fname=list(db.execute("select fname from persona where email=:email",{"email":email}))
        lname=list(db.execute("select lname from persona where email=:email",{"email":email}))
        usrnm = (fname[0][0]+" "+lname[0][0])
        if request.form.get("password")==pschek[0][0]:
            return render_template("userlg.html",fname=fname[0][0],usrnm=(f"{fname[0][0]} {lname[0][0]}"))
            #return "Congratulations ! you are now logged in."
        else:
            return render_template("relogin.html")
    except sqlalchemy.exc.OperationalError:
        return render_template("relogin.html",cerror=True)

@app.route("/search",methods=["POST","GET"])
def search():
    if request.method =='GET':
        return render_template("login.html")
    try:
        try:
            # STARTING A SECOND DATABASE INSTANCE
            #engine = create_engine(DATABASE_URL2)
            #db = scoped_session(sessionmaker(bind=engine))
            # SECOND DATABASE INSTANCE OVER
            search=request.form.get("search")
            if search=="":
                return render_template("emptyresult.html",usrnm='')
            frtitle = list(db2.execute("select title,author,year,isbn from authtit,book where title ilike :search and authtit.authtit_id=book.authtit_id;",{"search":search+'%'}))
            results=(frtitle)
            if frtitle==[]:
                fryear = list(db2.execute("select title,author,year,isbn from authtit,book where year ilike :search and authtit.authtit_id=book.authtit_id;",{"search":search+'%'}))
                results=(fryear)
                if fryear==[]:
                    frauthor = list(db2.execute("select title,author,year,isbn from authtit,book where author ilike :search and authtit.authtit_id=book.authtit_id;",{"search":search+'%'}))
                    results = (frauthor)
                    if frauthor==[]:
                        frisbn = list(db2.execute("select title,author,year,isbn from authtit,book where book.authtit_id in (select authtit_id from book where isbn like :search) and book.authtit_id=authtit.authtit_id;",{"search":search+'%'}))
                        #print(f"\nvalue of search is {search+'%'}\n")
                        results = frisbn

            if results != []:
                res1=[]
                for i in range(len(results)):
                    #print(f"title : {results[i][0]} author : {results[i][1]} year : {results[i][2]} isbn : {results[i][3] }")
                    for j in range(4):
                        res1.append(results[i][j])
                #print(f"\n\nresutls are : {res1} \n\n")
                #return "Your search is now complete check your flask console."
                try:
                    return render_template("result.html",results=res1,usrnm=usrnm,reslen=int(len(res1)/4),llen=int(len(res1)))
                except NameError:
                        return render_template("result.html",results=res1,usrnm='',reslen=int(len(res1)/4),llen=int(len(res1)))
            else:
                # return "sorry there are no results for your search ! "
                try:
                    return render_template("result.html",results="No results found , sorry !",check="true",usrnm=usrnm,reslen=0)
                except NameError:
                    return render_template("result.html", results="No results found , sorry !",check="true",usrnm='',reslen=0)
        except TypeError:
            return render_template("emptyresult.html",usrnm=usrnm)
    except sqlalchemy.exc.OperationalError:
        return render_template("relogin.html", cerror=True)
        #return "Sorry but our site is currently not available. try again later."


@app.route("/book",methods=["POST","GET"])
def book():
    KEY='UF7lsnFgBIuNs7FzIfDBRw'
    try:
        try :
            try:
                try:
                    check1=[]
                    bname=request.args.get("bname")
                    revcnt = request.form.get("rating")
                    rev = request.form.get("review")
                    check = list(db.execute("select bname from reviews where email = :email ;", {"email": email}))
                    for i in range(len(check)):
                        check1.append(check[i][0])
                    if bname in check1:
                        revi = 1
                    else:
                        revi=0
                    if (revcnt != None or rev != None) and revi != 1:
                        bname = request.args.get("bname")
                        check=list(db.execute("select bname from reviews where email = :email ;",{"email":email}))
                        for i in range(len(check)):
                            check1.append(check[i][0])
                        #print(f"\n\nrevcnt:{revcnt}\t rev={rev}\tcheck1={check1}\tbname={bname}")
                        if bname not in check1:
                            db.execute("insert into reviews values(default,:email,:revcnt,:rev,:bname);",{"email":email,"revcnt":revcnt,"rev":rev,"bname":bname})
                            db.commit()
                            revi=1
                    byear = request.args.get("byear")
                    #print("byear=",byear)
                    isbn = list(db2.execute("select isbn from book where authtit_id = (select authtit_id from authtit where title=:title and year=:year);",{"title": bname,"year":byear}))
                    #print("\n0", ''.join(isbn))
                    #print("\n0",isbn)
                    #print("\n1",isbn[0][0])
                    trevs1=list(db.execute("select email,revcnt,rev from reviews where bname=:bname;",{"bname":bname}))
                    trevs=[]
                    for j in range(len(trevs1)):
                        trevs.append(trevs1[j][0])
                        trevs.append(trevs1[j][1])
                        trevs.append(trevs1[j][2])
                    print("\n1",trevs,"\n")
                    usrcnt=0
                    for k in range(len(trevs)):
                        if k%3 == 0 :
                            usernames1=list(db.execute("select fname,lname from persona where email=:email",{"email":email}))
                            usernames=[]
                            for cnt in range(len(usernames1)):
                                name=(f"{usernames1[cnt][0]} {usernames1[cnt][1]}")
                                usernames.append(name)
                            trevs[k]=usernames[usrcnt]
                            usrcnt+=1
                    print("\n2", trevs, "\n")
                    if trevs==[]:
                        trstatus=0
                    else :
                        trstatus=1
                    res = str(requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbn[0][0]}))
                    if res == '<Response [404]>':
                        isbn = ('0' + isbn[0][0])
                        #print('1', isbn)
                    res = str(requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbn}))
                    if res == '<Response [404]>':
                        isbn = isbn + ('X')
                        #print('\n2', isbn)
                    res = str(requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbn}))
                    if res == '<Response [404]>':
                        isbn = (list(db2.execute("select isbn from book where authtit_id = (select authtit_id from authtit where title=:title);",{"title": bname})))
                        isbn1 = []
                        for j in range(len(isbn[0][0])-1):
                            isbn1.append(isbn[0][0][j])
                        isbn1.append('X')
                        isbn = (''.join(isbn1))
                        #print('\n3', isbn)
                    res = str(requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbn}))
                    if res== '<Response [404]>':
                        isbn=('0'+isbn)
                    res = str(requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbn}))
                    if res== '<Response [404]>':
                        isbn=('0'+isbn)
                    res = str(requests.get("https://www.goodreads.com/book/review_counts.json",params={"key": KEY, "isbns": isbn}))
                    if res == '<Response [404]>':
                        return render_template("book.html", bdstatus=0,bname=bname,usrnm=usrnm,revi=revi,trevs=trevs,trstatus=trstatus)
                    res = (requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbn}))
                    print("\nres is ",res,"\n")
                    data = res.json()
                    #print(data)
                    battributes=['id','isbn','isbn13','ratings_count','reviews_count','text_reviews_count','work_ratings_count','work_reviews_count','work_text_reviews_count','average_rating']
                    binfo=[]
                    for attr in battributes:
                        binfo.append(data['books'][0][attr])
                    return render_template("book.html",usrnm=usrnm,bname=bname,isbn=isbn,res=binfo,revi=revi,trevs=trevs,trstatus=trstatus)
                except IndexError:
                    return render_template("relogin.html",cerror=True)
            except NameError:
                return render_template("book.html",usrnm='',bname=bname,isbn=isbn,res=binfo,revi=revi,trevs=trevs,trstatus=trstatus)
        except builtins.UnboundLocalError:
            return render_template("relogin.html", cerror=True)
    except sqlalchemy.exc.OperationalError :
        return render_template("relogin.html", cerror=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)