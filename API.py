from flask import Flask, jsonify, request,json
import pywikibot
from datetime import datetime

page_names  = ["Ironman", "Thor", "Captain_America", "Black_Widow", "Hulk"]

site = pywikibot.Site("en", "wikipedia")

def update_revisions(name_of_article):
    page = pywikibot.Page(site, "User:Nagathedon/sandbox/"+name_of_article)
    revs = page.revisions(content=False)
    revs = list(revs)

    return revs


app = Flask(__name__)

@app.route("/documents", methods = ["GET"])
@app.route("/documents/", methods = ["GET"])

def index():
    return jsonify(page_names)


@app.route("/documents/<name>", methods = ["GET", "POST"])
@app.route("/documents/<name>/", methods = ["GET"])

def revisions(name):
    try:
        revs = update_revisions(name)
        timestamps = []
        if (request.method == 'POST'):
            some_json = request.get_json()
            content_str = some_json.get("content")
            text = pywikibot.Page(pywikibot.Site(), 'User:Nagathedon/sandbox/'+name).getOldVersion(oldid=revs[0]["revid"])
            page = pywikibot.Page(site, 'User:Nagathedon/sandbox/'+name)
            page.text = page.text.replace(text, content_str)
            page.save('Replaced '+name+" Page") 
            return jsonify(some_json.get("content"))

        else:
            for i in range(len(revs)):
                timestamps.append(revs[i]['timestamp'])
            return jsonify(timestamps)

    except pywikibot.exceptions.NoPage:
        print("This page does not EXIST!")
        return jsonify("This PAGE does not exist! Select one of the given pages!")


@app.route("/documents/<num>/latest")
@app.route("/documents/<num>/latest/")

def latest(num):
    try:
        revs = update_revisions(num)
        text = pywikibot.Page(pywikibot.Site(), 'User:Nagathedon/sandbox/'+num).getOldVersion(oldid=revs[0]["revid"]) 
        return jsonify(text)

    except pywikibot.exceptions.NoPage:
        print("This page does not EXIST!")
        return jsonify("This PAGE does not exist! Select one of the given pages!")


@app.route("/documents/<num>/<time>",methods = ["GET"])
@app.route("/documents/<num>/<time>/",methods = ["GET"]    )
def revision_at_timestamp(num, time):
    try:
        revs = update_revisions(num)

        date = datetime.strptime(time, '%a, %d %b %Y %H:%M:%S GMT')
        received_time = str(date.isoformat())+"Z"

        revision_id = 0
        for i in range(len(revs)):
            if(received_time == str(revs[i]['timestamp'])):
                revision_id = revs[i]["revid"]
                break

        try:
            text = pywikibot.Page(pywikibot.Site(), 'User:Nagathedon/sandbox/'+num).getOldVersion(oldid=revision_id) 
            return jsonify(text)

        except KeyError:
            print("This revision does not exist!")
            return jsonify("This revision does not exist! Make a revision using the POST function described in README.txt")


    except (pywikibot.exceptions.NoPage,ValueError) as e :
        print("This page does not EXIST!")
        return jsonify("This PAGE does not exist! Select one of the given pages! Check the format for Dates")

    


if __name__ == "__main__":
    app.run(debug=True)