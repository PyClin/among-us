"""
has functions which can be used for:
    * creating new nodes.
    * creating relationships between two existing nodes.
"""


import os
import uuid

import dotenv
import py2neo

# constants for user node label and relationship property value
USER_NODE_LABEL = "User"
TWEET_NODE_LABEL = "Tweet"

USER_SIMILAR_RELATIONSHIP = "USER-SIMILAR"
VERIFIED_RELATIONSHIP = "VERIFIED"
UNVERIFIED_RELATIONSHIP = "UNVERIFIED"
TWEET_SIMILAR_RELATIONSHIP = "TWEET-SIMILAR"

dotenv.load_dotenv(verbose=True)

NEO4J_ADDRESS = os.getenv("NEO4J_ADDRESS")
NEO4J_AUTH_USERNAME=os.getenv("NEO4J_AUTH_USERNAME")
NEO4J_AUTH_PASSWORD=os.getenv("NEO4J_AUTH_PASSWORD")

AUTH = (NEO4J_AUTH_USERNAME, NEO4J_AUTH_PASSWORD)

graph = py2neo.Graph(address=NEO4J_ADDRESS, auth=AUTH)


def create_user(user_id: str, user_name: str) -> bool:
    """
    takes user's unique id and name as inputs
    to insert as a node in the neo4j db

    note: it will create a new node, even if
    the user_id and name combo already exists.

    Args:
     user_id (string), user's id for reference
     user_name (string), user's name for reference

    Returns:
     boolean, confirming whether newly onboarded User got created or not.
    """

    user = py2neo.Node(USER_NODE_LABEL, user_id=user_id, name=user_name)
    graph.create(user)

    return graph.exists(user)


def create_tweet(
    tweet_id: str, user_id: str,
    node_number: int, flagged: bool,
    ) -> bool:
    """
    takes relevant tweet details and inserts it

    Args:
     tweet_id (string), tweet's id for reference
     user_id (string), user's id for reference
     node_number (int), number indicating chronlogical order of user's tweets
     flagged (boolean), indicating whether the tweet got flagged or not.

    Returns:
     boolean, confirming whether Tweet got created or not.
    """

    tweet = py2neo.Node(
        TWEET_NODE_LABEL,
        tweet_id=tweet_id, user_id=user_id,
        node_number=node_number, flagged=flagged
        )
    graph.create(tweet)

    return graph.exists(tweet)


def create_user_similarity(
    from_user_id: str, to_user_id: str,
    tdna_conf: float) -> bool:
    """
    to create a relationship called "USER-SIMILAR" between two User nodes with
    confidence score as a property for that relationship.

    Args:
     from_user_id (string), from-node's user id
     to_user_id   (string), to-node's user id
     tdna_conf     (float), confidence score of similarity between users

    Returns:
     boolean, representing whether the relationship got inserted or not.
    """

    matcher = py2neo.NodeMatcher(graph)
    from_node = matcher.match(USER_NODE_LABEL, user_id=from_user_id).first()
    to_node = matcher.match(USER_NODE_LABEL, user_id=to_user_id).first()

    user_similar = py2neo.Relationship(
        from_node,
        USER_SIMILAR_RELATIONSHIP,
        to_node,
        tdna_conf=tdna_conf
        )
    graph.create(user_similar)

    return graph.exists(user_similar)


def create_verified_similarity(
    from_user_id: str, verified_tweet_id: str,
    tdna_conf: float) -> bool:
    """
    to create a relationship called "VERIFIED" between a legit User 
    to his typing DNA verified tweet & confidence score as a 
    property for that relationship.

    Args:
     from_user_id (string), person who tweeted, their user id
     verified_tweet_id   (string), the authenticated tweet id, from that user id
     tdna_conf     (float), confidence score of similarity between onboard & tweet pattern

    Returns:
     boolean, representing whether the relationship got inserted or not.
    """

    matcher = py2neo.NodeMatcher(graph)
    from_node = matcher.match(USER_NODE_LABEL, user_id=from_user_id).first()
    to_node = matcher.match(TWEET_NODE_LABEL, tweet_id=verified_tweet_id).first()

    verified_similar = py2neo.Relationship(
        from_node,
        VERIFIED_RELATIONSHIP,
        to_node,
        tdna_conf=tdna_conf
        )
    graph.create(verified_similar)

    return graph.exists(verified_similar)


def create_authentication_failed(
    from_user_id: str, unverified_tweet_id: str) -> bool:
    """
    to create a relationship called "UNVERIFIED" between a legit User 
    to an impostor tweet from their account.

    Args:
     from_user_id (string), person who tweeted, their user id
     unverified_tweet_id  (string), the unauthenticated tweet id, from that user id

    Returns:
     boolean, representing whether the relationship got inserted or not.
    """

    matcher = py2neo.NodeMatcher(graph)
    from_node = matcher.match(USER_NODE_LABEL, user_id=from_user_id).first()
    to_node = matcher.match(TWEET_NODE_LABEL, tweet_id=unverified_tweet_id).first()

    failed_auth = py2neo.Relationship(
        from_node,
        UNVERIFIED_RELATIONSHIP,
        to_node,
        )
    graph.create(failed_auth)

    return graph.exists(failed_auth)


def create_tweet_impostor_similarity(
    impostor_user_id: str, unverified_tweet_id: str,
    tdna_conf: float) -> bool:
    """
    to create a relationship called "TWEET-SIMILAR" between a fraudulent
    not-verified Tweet with the impostor User among the network (thus Among Us) &
    confidence score as a property for that relationship.

    Args:
     impostor_user_id (string), impostor user id whose onboard pattern matched the tweet.
     unverified_tweet_id  (string), the unverified tweet, which was posted to dupe or fake.
     tdna_conf  (float), confidence score of similarity between impostor onboard & tweet patterns

    Returns:
     boolean, representing whether the relationship got inserted or not.
    """

    matcher = py2neo.NodeMatcher(graph)
    from_node = matcher.match(USER_NODE_LABEL, user_id=impostor_user_id).first()
    to_node = matcher.match(TWEET_NODE_LABEL, tweet_id=unverified_tweet_id).first()

    tweet_similar = py2neo.Relationship(
        from_node,
        TWEET_SIMILAR_RELATIONSHIP,
        to_node,
        tdna_conf=tdna_conf
        )
    graph.create(tweet_similar)

    return graph.exists(tweet_similar)


if __name__ == "__main__":

    # only for raw sample examples

    gen_id = lambda : str(uuid.uuid4())

    yaswant_user_id = gen_id()
    bhavesh_user_id = gen_id()
    rithumbhara_user_id = gen_id()
    shaaran_user_id = gen_id()
    jaivarsan_user_id = gen_id()

    # creating 5 new twitter signups
    print(create_user(user_id=yaswant_user_id, user_name="yaswant"))
    print(create_user(user_id=bhavesh_user_id, user_name="bhavesh"))
    print(create_user(user_id=rithumbhara_user_id, user_name="rithumbhara"))
    print(create_user(user_id=shaaran_user_id, user_name="shaaran"))
    print(create_user(user_id=jaivarsan_user_id, user_name="jaivarsan"))

    print(create_user_similarity(rithumbhara_user_id, shaaran_user_id, 0.999))

    # 3 legit tweets from yaswant
    print(create_tweet(tweet_id="123", user_id=yaswant_user_id, node_number=1, flagged=False))
    print(create_verified_similarity(yaswant_user_id, "123", 0.9))
    print(create_tweet(tweet_id="234", user_id=yaswant_user_id, node_number=2, flagged=False))
    print(create_verified_similarity(yaswant_user_id, "234", 0.92))
    print(create_tweet(tweet_id="345", user_id=yaswant_user_id, node_number=3, flagged=False))
    print(create_verified_similarity(yaswant_user_id, "345", 0.93))
    
    # 1 legit tweet from bhavesh
    print(create_tweet(tweet_id="567", user_id=bhavesh_user_id, node_number=1, flagged=False))
    print(create_verified_similarity(bhavesh_user_id, "567", 0.89))

    # 1 impostor tweet from yaswant's twitter + 1 impostor tweet from bhavesh's twitter
    # impostor because no-verification/authentication-failed is being called,
    # thus someone else did it.
    print(create_tweet(tweet_id="456", user_id=yaswant_user_id, node_number=4, flagged=False))
    print(create_authentication_failed(yaswant_user_id, "456"))
    print(create_tweet(tweet_id="678", user_id=bhavesh_user_id, node_number=2, flagged=False))
    print(create_authentication_failed(bhavesh_user_id, "678"))

    # unverified tweet patterns from yaswant and bhavesh 
    # should match jaivarsan's onboard pattern, since he's the impostor
    print(create_tweet_impostor_similarity(jaivarsan_user_id, "456", tdna_conf=0.801))
    print(create_tweet_impostor_similarity(jaivarsan_user_id, "678", tdna_conf=0.813))

    # using 890 tweet id to test user-user similarity based on flagged tweet
    print(create_tweet(tweet_id="789", user_id=shaaran_user_id, node_number=1, flagged=False))
    print(create_verified_similarity(shaaran_user_id, "789", 0.89))
    print(create_tweet(tweet_id="890", user_id=shaaran_user_id, node_number=2, flagged=False))
    print(create_verified_similarity(shaaran_user_id, "890", 0.89))
