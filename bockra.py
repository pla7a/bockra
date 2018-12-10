
from flask import Flask, request, redirect, render_template
import spotipy
from spotipy import util
import string
import random
from spotipy import oauth2
import json 
import model as m
import predict as p

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')

@app.route('/u')
def user_page():
    return render_template('user_form.html')

@app.route('/u', methods=['POST'])
def user_form():
    text = request.form['text']
    return redirect("/u/%s" %text)

@app.route('/u/<user>')
def user_tweets(user):
    max, min, proba = p.get_user(m.bnb, user, p.api, m.CVec, m.anly_CV, 10)
    pos, neg = p.calc_sentiment(proba)
    pos = round(pos*100, 0)
    neg = round(neg*100, 0)
    max_p = round(max["p"]*100,0)
    min_p = round(100-(min["p"]*100),0)
    return render_template("user_page.html", user=user, pos=pos, neg=neg, max_tweet=max["text"], max_p=max_p, min_tweet=min["text"], min_p=min_p)

@app.route('/t')
def term_page():
    return render_template("term_form.html")

@app.route('/t',methods=["POST"])
def term_form():
    text = request.form['text']
    return redirect("/t/%s" %text)


@app.route('/t/<term>')
def term_tweets(term):
    proba = p.search_term(m.bnb, term, p.api, m.CVec, m.anly_CV)
    pos, neg = p.calc_sentiment(proba)
    pos = round(pos*100, 0)
    neg = round(neg*100, 0)
    term_dict = p.show_term(m.bnb, term, p.api, m.CVec, m.anly_CV)
    return render_template("term_page.html", term=term, pos=pos, neg=neg, term_dict=term_dict)

@app.route('/tw')
def tweet_page():
    return render_template("tweet_form.html")

@app.route('/tw',methods=["POST"])
def tweet_form():
    text = request.form['text']
    return redirect("/tw/%s" %text)

@app.route('/tw/<id>')
def tweet_tweets(id):
    tweet = p.api.GetStatus(id)
    screen_name = tweet.user.screen_name
    real_name = tweet.user.name
    tweet_text = tweet.text
    proba = p.get_tweet(m.bnb, id, p.api, m.CVec, m.anly_CV)
    pos, neg = p.calc_sentiment(proba)
    pos = round(pos*100,0)
    neg = round(neg*100,0)
    return render_template("tweet_page.html", name=real_name, screen_name=screen_name, tweet_text=tweet_text, pos=pos, neg=neg)

@app.route('/s/')
def spotify_code():
    scope = "user-top-read"
    client_id = "id"
    client_secret = "secret"
    redirect_uri = "uri"

    code = request.args.get('code')
    code = str(code)
    try:
        sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope, cache_path="")
        auth_token = sp_oauth.get_access_token(code)
        token = auth_token["access_token"]
        sp = spotipy.Spotify(auth=token)
        
    # Get information about current user
        me = sp.current_user()
        me_ds = json.dumps(me)

        # Get top artists
        cuta = sp.current_user_top_artists(limit=10, offset=0, time_range='long_term')
        a = {}
        for i in cuta['items']:
            a[i["name"]]= i["popularity"]
        cuta_ds = json.dumps(a)

	# Get top songs
        cutt = sp.current_user_top_tracks(limit=10, offset=0, time_range="long_term")
        cutt_ds = json.dumps(cutt)
        return render_template("submit.html", cuta_ds=cuta_ds, cutt_ds=cutt_ds, me_ds=me_ds)

    except:
        return render_template("accessError.html")

#@app.route('/user')
#def user_verify():
#    return redirect('top-read-url')
