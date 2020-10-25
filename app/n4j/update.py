import os
import uuid

import dotenv
import py2neo

# constants for user node label and relationship property value
TWEET_NODE_LABEL = "Tweet"


dotenv.load_dotenv(verbose=True)

NEO4J_ADDRESS = os.getenv("NEO4J_ADDRESS")
NEO4J_AUTH_USERNAME=os.getenv("NEO4J_AUTH_USERNAME")
NEO4J_AUTH_PASSWORD=os.getenv("NEO4J_AUTH_PASSWORD")

AUTH = (NEO4J_AUTH_USERNAME, NEO4J_AUTH_PASSWORD)

graph = py2neo.Graph(address=NEO4J_ADDRESS, auth=AUTH)


def update_tweet(
    tweet_id: str, flagged: bool,
    ) -> bool:
    """
    takes relevant tweet details and updates it

    Args:
     tweet_id (string), tweet's id for reference
     flagged (boolean), indicating whether the tweet got flagged or not.

    Returns:
     boolean, confirming whether Tweet got updated or not.
    """

    matcher = py2neo.NodeMatcher(graph)
    tweet = matcher.match(TWEET_NODE_LABEL, tweet_id=tweet_id).first()

    tweet["flagged"] = flagged
    graph.push(tweet)

    return graph.exists(tweet)

if __name__ == "__main__":

    print(update_tweet(tweet_id="890", flagged=True))