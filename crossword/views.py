from flask import render_template
from itertools import groupby
from . import app
from .database import session, Entry
from flask import flash
from flask.ext.login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from .database import User
from flask import request, redirect, url_for
from flask.ext.login import login_required, current_user
import datetime
from datetime import date, timedelta, tzinfo
from pytz import timezone
import pytz
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


@app.route("/")
@app.route("/date/<selected_date>")
def entries(selected_date = str(datetime.datetime.now(pytz.timezone('US/Eastern')))):
    print(selected_date)
    try:
        selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
    except ValueError:
        selected_date = selected_date[:selected_date.rindex(" ")]
        selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
    
    now_utc = datetime.datetime.now(timezone('UTC'))
    print(now_utc)
    now_eastern = now_utc.astimezone(timezone('US/Eastern'))
    print(now_eastern, "should be 16")
    #selected_date = (now_utc.astimezone(local_tz).date())
    

    print(selected_date)
    #selected_date = (now_utc.astimezone(local_tz).date())
    #local_time = datetime.datetime.strptime(local_time, "%Y-%m-%d").date()
    #selected_date = str(datetime.date.today())
    #selected_date = datetime.datetime.strptime(str(selected_date), "%Y-%m-%d").date()
    # Zero-indexed page
    #page_index = page - 1
    i = 0
    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    oldestentry = entries[-1]
    newestentry = entries[0]
    entrylist = []
    count = session.query(Entry).count()
    while entrylist == []:
        older = selected_date - timedelta(1)
        newer = selected_date + timedelta(1)
        print(newer)
        #create a list (entrylist) that has just the entries from a certain day.
        for entry in entries:
            #print(entry.datetime)
            #entry.datetime = datetime(timezone('UTC'))
            #entry.datetime.astimezone(timezone('US/Eastern'))
            #print(entry.datetime, "want this to be 15:43:21.262308")
            daybefore = selected_date - timedelta(i)
            if entry.datetime.strftime("%Y-%m-%d") == daybefore.strftime("%Y-%m-%d"):
                entrylist.append(entry)
                print(entrylist)
        if entrylist == []:
            selected_date = selected_date - timedelta(1)
            return redirect(url_for("entries", selected_date = selected_date))
            
            
    #NEED A NEW/SEPERATE METHOD FOR NEWER.**************
    
    #Trying to classify a winner here
    
        
    limit= len(entrylist)
    total_pages = (count - 1) / limit + 1
    
    #determine "newer" and/or "older" links should be shown
    if newestentry in entrylist:
        has_next = True
        has_prev = False
    elif oldestentry not in entrylist:    
        has_next = True
        has_prev = True
    else:
        has_prev = True
        has_next = False
        
    '''quickest = min(int(entry.title) for entry in entrylist)
    print(quickest)'''
    #test = entrylist[0]
    #formatted = datetime.timedelta(seconds=int(test.title))
    #print(formatted)
    #formatted.datetime.strftime("%m-%s")
    '''s = int(test.title)
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    print('%s:%s' % (minutes, seconds))'''
    #try this when only one entry for the day :)
    #print(test.title, "test")
    
    '''for entry.title in entrylist:
        entry.title = int(entry.title)
        hours, remainder = divmod(entry.title, 3600)
        minutes, seconds = divmod(remainder, 60)'''
    
    
        
    return render_template("entries.html",
        entries=entrylist,
        has_next=has_next,
        has_prev=has_prev,
        selected_date=selected_date,
        older = older,
        newer = newer,
        total_pages=total_pages
    )
        
@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))
    login_user(user, remember=True, force=True)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for("add_entry_get"))
    

@app.route("/register", methods=["GET"])
def register_get():
    return render_template('register.html')

@app.route("/register", methods=["POST"])
def register_post():
    try: 
        name = User(name=request.form["username"], password=generate_password_hash(request.form["password"]), email=request.form["email"])
        session.add(name)
        session.commit()
        flash("User successfully registered")
        login_user(name)
        return redirect(request.args.get("next") or url_for("entries"))
    except IntegrityError:
        flash("The username or email was already taken.  This app isn't sophisticated enough to let you reset a password, so just register a new user", "danger")
        return redirect(url_for("register_get"))
    
    
@app.route("/entry/<id>", methods=["GET"])
def get_entry(id):
    entry = session.query(Entry)
    return render_template("render_entry.html", entry = entry.get(id))
    
    
@app.route("/entry/add", methods=["GET"])
@login_required
def add_entry_get():
    return render_template("add_entry.html")

    
@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    time = request.form["title"]
    if time[0] == ":":
        title = time
    elif ":" not in time:
        title = time
    else:
        title=sum(int(x) * 60 ** i for i,x in enumerate(reversed(time.split(":"))))
    #print(sum(int(x) * 60 ** i for i,x in enumerate(reversed(time.split(":")))))
    entry = Entry(
        title = title,
        content=request.form["content"],
        author=current_user
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))
    
    
@app.route("/entry/<id>/edit", methods=["GET"])
@login_required
def edit_entry_get(id):
    entry = session.query(Entry)
    return render_template("edit_entry.html", entry = entry.get(id))
    
@app.route("/entry/<id>/edit", methods=["POST"])
def edit_entry_post(id):
    if "cancel" in request.form:
        return redirect(url_for("entries"))
    else:
        entry = session.query(Entry).get(id)
        entry.title = request.form["title"]
        entry.content = request.form["content"]
        entry.datetime = request.form
        session.commit()
        return redirect(url_for("entries"))
        
    
@app.route("/entry/<id>/delete", methods=["GET"])
def delete_entry_get(id):
    entry = session.query(Entry)
    return render_template("delete_entry.html", entry = entry.get(id))
        
@app.route("/entry/<id>/delete", methods=["POST"])
def delete_entry_post(id):
    entry = session.query(Entry).get(id)
    session.delete(entry)
    session.commit()
    return redirect(url_for("entries"))
    
    
