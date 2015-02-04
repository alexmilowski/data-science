import tweepy

# Note: You must fill in your four values below from your registered application.

consumer_key = "twI3B0GuFxkAY5Y8EggYuH1MW"
consumer_secret = "MRnoOyoGOgoXAyd26Rwm2cZloVBT63MhZr5ZyvT06koxPDlIhV"

access_token = "720169710-4hstZM04S6DMKm1rr1y4Cy9TWvgTvu29LUKzbUT6"
access_token_secret = "v23joaXipB0ORm5JCEEpR8xSOEwJWkNAXidpHRlElm3hY"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

for tweet in api.search(q="minecraft"):
   print tweet.text
