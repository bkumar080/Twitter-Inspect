from flask import Flask
from flask import request
from flask import render_template
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re
from re import sub
import webbrowser

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("cs.html")

# -----------------------------------------------------------------------------

def HTML(myURL):
	uClient = uReq(myURL)
	pageHTML = uClient.read()
	uClient.close()

	pageSoup = soup(pageHTML, "html.parser")
	return pageSoup

def fakecheck(usr):
	global count
	myURLfc = "https://www.twitteraudit.com/" + usr
	
	try:
		pgSoup = HTML(myURLfc)
		foll = pgSoup.findAll("div",{"class":"audit"})

		link = foll[0].div.a["href"]
		real = foll[0].findAll("span",{"class":"real number"})[0]["data-value"]
		fake = foll[0].findAll("span",{"class":"fake number"})[0]["data-value"]
		scr = foll[0].findAll("div",{"class":"score"})[0].div
		scoresent = scr["class"][1]
		score = re.findall(r'\d{1,3}',str(scr))[0]
		print (count)
	
	except Exception as e:
		pass

	return [link, real, fake, scoresent, score]

def tweety(box):
	inp = box
	myURL = 'https://twitter.com/search?f=users&q='+inp.replace(" ", "%20")+'&src=typd&lang=en'

	inpy = inp.split(" ")

	pageSoup = HTML(myURL)

	card = pageSoup.findAll("div",{"class":"ProfileCard-content"})

	det = []

	count = 0
	para = ""
	for cardy in card:
		dum = cardy.findAll("p",{"class":"ProfileCard-bio u-dir js-ellipsis"})
		dis = re.sub(r'<.*?>','',str(dum[0]))

		name = cardy.div.div.div.div["data-name"]
		tname = cardy.div.div.div.div["data-screen-name"]
		tid	= cardy.div.div.div.div["data-user-id"]
		img	= cardy.a.img["src"] 
		desc = dis.replace("\n", "  ")
		
		link, real, fake, scoresent, score = fakecheck(tname)
		#print ("Link: "+link)
		#dumz = "<br />" +"Name : " + name + "<br />"+"User Name : " + tname + "<br />" + "score : " + score + "%" + "<br/>"
		

		#dumz ="<tr><td class=\"tg-yw4l\"><img src="+img+"></td><td class=\"tg-yw4l\"><b>"+name+"</b><br /><i>"+tname+"</i></td><td class=\"tg-yw4l\">Real : "+real+" Followers<br />Fake : "+fake+" Followers</td><td class=\"tg-yw4l\">Score : "+score+"<br />Result : "+scoresent+"</td><td class=\"tg-yw4l\"><a href=\"https://twitter.com/"+link+"\"><button style=\"height: 35px;width: 80px\">Profile Link</button></a></td></tr>"
		dumz ="<tr><td><img src="+img+"></td><td><b>"+name+"</b><br /><i>@"+tname+"</i></td><td><b>Real :</b> "+real+" <br /><b>Fake :</b> "+fake+" </td><td><b>Score :</b> "+score+" %<br /><b>Result :</b> "+scoresent+"</td><td><a href=\"https://twitter.com/"+link+"\"><button class=\"button\" style=\"height: 35px;width: 80px\">Profile Link</button></a></td></tr>"

		#"<p><b>"+name+"</b><br /><i>"+tname+"</i><br />Score : "+score+"<br />Result : "+scoresent+"<br /> Real : "+real+" Followers<br />Fake : "+fake+" Followers<br />Link : "+link+" </p> \n"                                                     <button class="button" style="vertical-align:middle"><span>Hover </span></button>
		para = para + dumz
		count += 1
	front = """<head>
    <title>Twitter Inspect</title>
    <link rel="icon" href="/static/cropfingerprint_transparent.png" type="image/gif" sizes="16x16">
    </head>
	<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
.tg .tg-yw4l{vertical-align:top}

h1{
  font-size: 35px;
  color: #fff;
  text-transform: uppercase;
  font-weight: 300;
  text-align: center;
  margin-bottom: 15px;
}
table{
  width:100%;
  table-layout: fixed;
}
.tbl-header{
  background-color: rgba(255,255,255,0.3);
 }
.tbl-content{
  height:590px;
  overflow-x:auto;
  margin-top: 0px;
  border: 1px solid rgba(255,255,255,0.3);
}
th{
  padding: 20px 15px;
  text-align: left;
  font-weight: 500;
  font-size: 16px;
  text-align: center;
  color: #fff;
  text-transform: uppercase;
}
td{
  padding: 15px;
  text-align: left;
  vertical-align:middle;
  font-weight: 300;
  font-size: 12px;
  color: #fff;
  text-align: center;
  border-bottom: solid 1px rgba(255,255,255,0.1);
}


/* demo styles */

@import url(http://fonts.googleapis.com/css?family=Roboto:400,500,300,700);
body{
  background: -webkit-linear-gradient(left, #25c481, #25b7c4);
  background: linear-gradient(to right, #25c481, #25b7c4);
  font-family: 'Roboto', sans-serif;
}
section{
  margin: 50px;
}


/* follow me template */
.made-with-love {
  margin-top: 40px;
  padding: 10px;
  clear: left;
  text-align: center;
  font-size: 10px;
  font-family: arial;
  color: #fff;
}
.made-with-love i {
  font-style: normal;
  color: #F50057;
  font-size: 14px;
  position: relative;
  top: 2px;
}
.made-with-love a {
  color: #fff;
  text-decoration: none;
}
.made-with-love a:hover {
  text-decoration: underline;
}


/* for custom scrollbar for webkit browser*/

::-webkit-scrollbar {
    width: 6px;
} 
::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3); 
} 
::-webkit-scrollbar-thumb {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3); 
}

.button {
  display: inline-block;
  border-radius: 4px;
  background-color: #536DFE;
  border: none;
  color: #FFFFFF;
  text-align: center;
  font-size: 10px;

  width: 200px;
  transition: all 0.5s;
  cursor: pointer;
  margin: 5px;
}

.button span {
  cursor: pointer;
  display: inline-block;
  position: relative;
  transition: 0.5s;
}

.button span:after {
  content: '\00bb';
  position: absolute;
  opacity: 0;
  top: 0;
  right: -20px;
  transition: 0.5s;
}

.button:hover span {
  padding-right: 25px;
}

.button:hover span:after {
  opacity: 1;
  right: 0;
}

</style>
<h1><b>Twitter Inspect</b></h1>
<div class="tbl-header">
    <center><table cellpadding="0" cellspacing="0"   margin-left:100px  margin-right: 100px>
      <thead>
  <tr>
    <th><b>Profile Picture</b></th>
    <th><b>Name &amp; ID</b></th>
    <th><b>Followers</b></th>
    <th><b>Score</b></th>
    <th><b>Twitter Link</b></th>
  </tr>
  </thead>
    </table>
  </div>
  <div class="tbl-content">
    <table cellpadding="0" cellspacing="0" border="0">
      <tbody>\n"""
	back = """\n</tbody>\n</div>\n</table></center>\n</div>

</div>
"""
	table = front + para + back
	return (table)

# --------------------------------------------------------------

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    processed_text = tweety(text)

    return processed_text

	
    

if __name__ == '__main__':
    app.run()