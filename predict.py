import model as m
import twitter as tw
import numpy as np

c_key = "key"
c_secret ="secret"
at_key = "key"
at_secret = "secret"

def auth_api(c_key, c_secret, at_key, at_secret):
   return tw.Api(consumer_key=c_key, consumer_secret=c_secret, access_token_key=at_key, access_token_secret=at_secret)


def get_user(bnb, username, api, CVec, anly_CV, n):
   user_timeline = api.GetUserTimeline(screen_name=username, count=n)
   tweet_txt = [i.text for i in user_timeline]
   tweets = [CVec.transform(anly_CV(y)) for y in tweet_txt]
   tweets_process = []
   for i in tweets:
       x = i.toarray().sum(axis=0)
       tweets_process.append(x)
   proba =  bnb.predict_proba(tweets_process)
   max = np.argmax(proba[:,1])
   min = np.argmin(proba[:,1])
   tw_max = {"text":tweet_txt[max], "p":proba[max,1]}
   tw_min = {"text":tweet_txt[min], "p":proba[min,1]}
   return tw_max, tw_min, proba


def get_tweet(bnb, tweet_id, api, CVec, anly_CV):
   tweet = api.GetStatus(tweet_id)
   analy_tweet = CVec.transform(anly_CV(tweet.text))
   x = analy_tweet.toarray().sum(axis=0)
   return bnb.predict_proba([x])


def search_term(bnb, term, api, CVec, anly_CV):
   term_tweet = api.GetSearch(term, count=50)
   tweets = [CVec.transform(anly_CV(i.text)) for i in term_tweet]
   tweets_process = []
   for i in tweets:
       x = i.toarray().sum(axis=0)
       tweets_process.append(x)
   return bnb.predict_proba(tweets_process)


def show_term(bnb, term, api, CVec, anly_CV):
   term_tweet = api.GetSearch(term, count=10)
   term_user = [i.user for i in term_tweet]
   term_texts = [i.text for i in term_tweet]
   tweets = [CVec.transform(anly_CV(i.text)) for i in term_tweet]
   tweets_process = []
   for i in tweets:
       x = i.toarray().sum(axis=0)
       tweets_process.append(x)
   proba = bnb.predict_proba(tweets_process)

   term_dict = []
   screen_name = [u.screen_name for u in term_user]
   real_name = [u.name for u in term_user]
   for i in range(len(term_texts)):
       term_dict.append({"screen_name": screen_name[i], "name":real_name[i], "text":term_texts[i], "p":round(proba[i][1]*100, 0)})
   return (term_dict)

def calc_sentiment(arr):
   positive = sum([x[1] for x in arr])
   negative = sum([x[0] for x in arr])
   pos_rat = positive/arr.shape[0]
   neg_rat = negative/arr.shape[0]
   return [pos_rat, neg_rat]

api = auth_api(c_key, c_secret, at_key, at_secret)

