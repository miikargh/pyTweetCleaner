import re
import string
from dataclasses import dataclass


@dataclass
class TweetCleanerArgs:
    remove_retweets: bool = False
    split_compound_words: bool = False
    remove_non_ascii: bool = False
    remove_hyperlinks: bool = True
    normalize_whitespace: bool = True


class TweetCleaner:
    def __init__(self, args: TweetCleanerArgs = TweetCleanerArgs()):
        """
        clean unnecessary twitter data
        remove_retweets = True if retweets are to be removed (default = False)
        """

        self.args = args

        self.punc_table = str.maketrans(
            "", "", string.punctuation
        )  # to remove punctuation from each word in tokenize

    def compound_word_split(self, compound_word):
        """
        Split a given compound word(string) and return list of words in given compound_word
        Ex: compound_word='pyTWEETCleaner' --> ['py', 'TWEET', 'Cleaner']
        """
        matches = re.finditer(
            ".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", compound_word
        )
        return [m.group(0) for m in matches]

    def remove_non_ascii_chars(self, text):
        """
        return text after removing non-ascii characters i.e. characters with ascii value >= 128
        """
        return "".join([w if ord(w) < 128 else " " for w in text])

    def remove_hyperlinks(self, text):
        """
        return text after removing hyperlinks
        """
        return " ".join([w for w in text.split(" ") if not "http" in w])

    def normalize_whitespace(self, text):
        """Replaces all whitespace with spaces."""
        return " ".join(text.split())

    def get_cleaned_text(self, text):
        """
        return cleaned text(string) for provided tweet text(string)
        """

        # cleaned_text = text.replace('"', "").replace("'", "").replace("-", " ")
        cleaned_text = text

        if self.args.normalize_whitespace:
            cleaned_text = self.normalize_whitespace(cleaned_text)

        if self.args.remove_non_ascii:
            cleaned_text = self.remove_non_ascii_chars(cleaned_text)

        # retweet
        if re.match(r"RT @[_A-Za-z0-9]+:", cleaned_text):  # retweet
            if self.args.remove_retweets:
                return ""
            retweet_info = cleaned_text[
                : cleaned_text.index(":") + 2
            ]  # 'RT @name: ' will be again added in the text after cleaning
            cleaned_text = cleaned_text[cleaned_text.index(":") + 2 :]
        else:
            retweet_info = ""

        if self.args.remove_hyperlinks:
            cleaned_text = self.remove_hyperlinks(cleaned_text)

        cleaned_text = cleaned_text.replace("#", "HASHTAGSYMBOL").replace(
            "@", "ATSYMBOL"
        )  # to avoid being removed while removing punctuations

        cleaned_text = cleaned_text.replace("HASHTAGSYMBOL", "#").replace(
            "ATSYMBOL", "@"
        )
        cleaned_text = retweet_info + cleaned_text

        return cleaned_text


if __name__ == "__main__":
    sample_text = """RT @testUser: Cleaning unnecessary data with pyTweetCleaner
                     by @kevalMorabia97. #pyTWEETCleaner, Check it out at
                     https:\/\/github.com\/kevalmorabia97\/pyTweetCleaner and star
                     the repo!"""

    tc = TweetCleaner(remove_retweets=False)
    tc.clean_tweets(
        input_file="data/sample_input.json", output_file="data/sample_output.json"
    )  # clean tweets from entire file
    print("Output with remove_retweets=False:")
    print(tc.get_cleaned_text(sample_text), "\n")

    tc = TweetCleaner(remove_retweets=True)
    print("Output with remove_retweets=True:")
    print(tc.get_cleaned_text(sample_text), "\n")
