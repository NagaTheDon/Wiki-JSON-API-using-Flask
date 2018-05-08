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


@app.route("/documents/<num>/latest")
@app.route("/documents/<num>/latest/")

def latest(num):
		revs = update_revisions(num)
		text = pywikibot.Page(pywikibot.Site(), 'User:Nagathedon/sandbox/'+num).getOldVersion(oldid=revs[0]["revid"]) 
		return jsonify(text)


@app.route("/documents/<num>/<time>")
@app.route("/documents/<num>/<time>/")
def revision_at_timestamp(num, time):
	revs = update_revisions(num)
	date = datetime.strptime(time, '%a, %d %b %Y %H:%M:%S GMT')
	received_time = str(date.isoformat())+"Z"

	revision_id = 0
	for i in range(len(revs)):
		if(received_time == str(revs[i]['timestamp'])):
			revision_id = revs[i]["revid"]
			break

	if(revision_id == 0):
		print("ERROR: No revision with that timestamp")
	else:
		text = pywikibot.Page(pywikibot.Site(), 'User:Nagathedon/sandbox/'+num).getOldVersion(oldid=revision_id) 
		return jsonify(text)


	


if __name__ == "__main__":
	app.run(debug=True)