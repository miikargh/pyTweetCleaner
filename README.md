# tweet_cleaner
Python module to clean twitter json data and remove unnecessary tweet data

## Installation
```python
$ git clone git@github.com:miikargh/tweet_cleaner.git
$ cd tweet_cleaner
$ pip install -e .
```

## Usage 1
```python
>>> from tweet_cleaner import TweetCleaner
>>> tc = TweetCleaner(remove_retweets=False)
>>> tc.clean_tweets(input_file='data/sample_input.json', output_file='data/sample_output.json')
```

## Usage 2
```python
>>> from tweet_cleaner import TweetCleaner
>>> sample_text = 'RT @testUser: Cleaning unnecessary data with pyTweetCleaner by @kevalMorabia97. #pyTWEETCleaner, Check it out at https:\/\/github.com\/kevalmorabia97\/pyTweetCleaner and star the repo! '
>>>
>>> tc = TweetCleaner(remove_retweets=False)
>>> print(tc.get_cleaned_text(sample_text))
RT @testUser: Cleaning unnecessary data with pyTweetCleaner by @kevalMorabia97 #pyTWEETCleaner Check it out at and star the repo
>>>
>>> tc = TweetCleaner(remove_retweets=True)
>>> print(tc.get_cleaned_text(sample_text))
```


## Data Removed and Kept
```
REMOVE:        TWEETS THAT HAVE in_reply_to_status_id != null i.e. COMMENTS ON SOMEONE ELSE'S TWEETS
               TWEETS THAT HAVE lang != en i.e. NOT IN ENGLISH LANGUAGE
               DATA ABOUT DELETED TWEETS
               NON-ASCII CHARACTERS FROM text
               HYPERLINKS FROM text

KEEP:          created_at
               id
               text
               user_id
               user_name
               user_screen_name
               user_followers_count
               coordinates
               place
               retweet_count
               entities
               retweeted_status
```
