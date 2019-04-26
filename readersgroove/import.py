import os
import csv
import sys

from flask import Flask
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

with open("c://users//abhishek//desktop//project1//books.csv") as books:
    read=csv.reader(books)
    blist=list(read)

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["DEBUG"] = True
Session(app)


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/",methods=["POST","GET"])
def default():
    return "This is the homepage which does not do anything !\n" \
           "1.use route /insertauthor for inserting data into table author.\n"\
           "2.use route /insertauthtit for inserting data into table authtit.\n"\
           "3.use route /insertbook for inserting data into table book."


@app.route("/insertauthor",methods=["POST","GET"])
def authorinsert():
    for i in range(len(blist)):
        #db.execute("insert into authtit(author) values(:aname)",{"aname":(blist[i + 1][2])})
        db.execute("update authtit set author=:author where authtit_id=:authtit_id",{"author":(blist[i + 1][2]),"authtit_id":(i+1)})
        progress = ("{0:.2f}".format(((i + 1) / 5000) * 100))
        sys.stdout.write(f"\n[Progress = {progress} % ]\t\t{i+1} // Inserted record with author = {(blist[i + 1][2])} authtit_id = {i+1} ")
        try:
            if (i+1)%200==0:
                db.commit()
        except IndexError:
            db.commit()
            pass
    return " \n\nAll the records were inserted Successfully ! "

@app.route("/insertauthtitid",methods=["POST","GET"])
def authtitid():
    for i in range(len(blist)):
        try:
            aidls = list(db.execute("select aid from author where aname=:aname", {"aname": blist[i + 1][2]}))
            aid=(aidls[0][0])
            db.execute("insert into authtit values(:authtitid,:title,:year,:aid)",{"authtitid":i+1,"title":(blist[i+1][1]),"year":(blist[i+1][3]),"aid":aid})
            progress = ("{0:.2f}".format(((i + 1) / 5000) * 100))
            sys.stdout.write(f"\n[Progress = {progress} % ]\t\t{i + 1} || Inserted authtitid={i+1} title={(blist[i+1][1])} year={(blist[i+1][3])} aid={aid}")
            sys.stdout.flush()
        except IndexError:
            pass
        try:
            if (i + 1) % 200 == 0:
                db.commit()
        except IndexError:
            db.commit()
            pass

    return "\n\nAll the 5000 records were inserted successfully !\n\n"


@app.route("/insertbook",methods=["POST","GET"])
def book():
    for i in range(len(blist)):
        try:
            authtitls=list(db.execute("select authtit_id from authtit where title=:title", {"title": blist[i + 1][1]}))
            authtit=authtitls[0][0]
            progress = ("{0:.2f}".format(((i + 1) / 5000) * 100))
            tmpls = []
            if (blist[i + 1][0][9]) == 'x' or (blist[i + 1][0][9]) == 'X':
                for j in range(10):
                    tmpls.append(blist[i + 1][0][j])
                tmpls[9] = '0'
                isbn = (''.join(tmpls))
                db.execute("insert into book values(:isbn,:authtitid)",{"isbn": isbn, "authtitid": authtit})
                sys.stdout.write(f"\n[Progress = {progress} % ]\t{i + 1} ||\tauthtit_id = {authtit} and C.isbn={isbn} instead O.isbn = {blist[i + 1][0]} **")
            else:
                db.execute("insert into book values(:isbn,:authtitid)",{"isbn":(blist[i+1][0]),"authtitid":authtit})
                sys.stdout.write(f"\n[Progress = {progress} % ]\t{i + 1} ||\tauthtit_id = {authtit} and C.isbn= NULL instead O.isbn = {blist[i + 1][0]}")
            sys.stdout.flush()
        except IndexError:
            pass
        try:
            if (i + 1) % 200 == 0:
                db.commit()
        except IndexError:
            db.commit()
            pass

    return "\n\nAll the 5000 records were inserted successfully !\n\n"


if __name__=="__main__":
    default()