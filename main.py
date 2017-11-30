import flask, json, codecs, datetime
import tinydb
from datetime import date
import random

class JokeDatabase:
    def __init__(self):
        self.db = tinydb.TinyDB("jokes.json")
        self.last_updated = date.min
        self.today_joke = ""
    
    def add_joke(self, joke):
        self.db.insert({'joke': joke})
    
    def get_daily_joke(self):
        if date.today() > self.last_updated:
            self.today_joke = random.choice(self.db.all())
            self.last_updated = date.today()
        return self.today_joke
    
    def get_all_jokes(self):
        return self.db.all()
        
    def get_specific_joke(self, doc_id):
        return self.db.get(doc_id=doc_id)
    
    def update_joke(self, doc_id, joke):
        self.db.update({'joke': joke}, doc_ids=[doc_id])
    
    def delete_joke(self, doc_id):
        self.db.remove(doc_ids=[doc_id])

# set the project root directory as the static folder, you can set others.
app = flask.Flask(__name__, static_url_path='')
app.secret_key = b'\xa6\x13m\xa6{m\xdc\xe2e\xabb\xdd\xa4+y\xaf[\xc4\xcf\xd1\xc8\x0cs:'

@app.route('/get')
def get_route():
    return flask.jsonify(db.get_daily_joke())

@app.route('/admin')
def get_all_route():
    jokes = db.get_all_jokes()
    return flask.render_template("admin.html", jokes=jokes)

@app.route('/add', methods=['POST'])
def insert_route():
    if flask.request.form["joke"] is not None:
        db.add_joke(flask.request.form["joke"])
        flask.flash("Joke added")
        return flask.redirect(flask.url_for("get_all_route"))
    else:
        return "Invalid joke"

@app.route('/delete/<int:doc_id>')
def delete_route(doc_id):
    db.delete_joke(doc_id)
    flask.flash("Joke deleted")
    return flask.redirect(flask.url_for("get_all_route"))
        
if __name__ == "__main__":
    db = JokeDatabase()
    app.run()