# Baltimore is at 39.2833 N, 76.6167 W
# Random point I selected from the city center: 39.355411, -76.501172
import twitter
import json
import sys
import time

BALTIMORE = (39.2833, -76.6167, '30km')

# You need to create a creds.txt file with each of these
#  that you got from twitter.
creds = open('creds.txt').read().split('\n')

api = twitter.Api(consumer_key=creds[0], \
          consumer_secret=creds[1], \
          access_token_key=creds[2], \
          access_token_secret=creds[3])

tweets = []

# Start from the most recent if nothing is passed.
# You can pass in a id to start the search from where you left off earlier
last_id = sys.argv[1] if len(sys.argv) == 2 else None

seen_ids = set()

while True:

    try:
        # get some tweets. Twitter only likes to return ~100 at a time
        for tweet in api.GetSearch(geocode=(BALTIMORE), count=500, max_id=last_id):

            # tweets have an ascending ID #
            last_id = tweet.GetId()

            # sometimes the API starts to return duplicates, so if it does just give up
            #   and try again soon.
            if tweet.GetId() in seen_ids:
                print >> sys.stderr, "I just saw a duplicate tweet... I'm going to take a break"
                time.sleep(30)
                break

            print tweet # outputs the tweet, probably will get redirected to a file

            seen_ids.add(tweet.GetId())
            last_id = tweet.GetId()
        else:
            print >> sys.stderr, "Last id:", last_id
            continue

        break

    # Twitter will rate limit us, so we'll just take a break when they get mad at us
    except twitter.error.TwitterError:
        print >> sys.stderr, "I think I got rate limited, sleeping for a bit"
        time.sleep(60 * 15)



