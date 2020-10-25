"""
REST HTTP/1.1 endpoints for:
    * creating a new node for a user.
    * creating a new relationship between two user nodes.
"""

from flask import Flask, request, jsonify

from n4j.create import create_user, create_tweet
from n4j.create import create_user_similarity, create_tweet_impostor_similarity
from n4j.create import create_authentication_failed, create_verified_similarity

from n4j.update import update_tweet

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/add_user/", methods=["POST"])
def add_user():
    """
    api endpoint: /api/add_user/
    request supported methods: POST
    content type: application/json

    request json data model: user_id: string, user_name: string
    example for same: '{"user_id":"123", "user_name":"yaswant"}'

    response json data model: user_id: string, created: boolean
    example for same: '{"user_id":"123", "created":true}'

    Note: user_id is assumed to be unique in nature.
    """

    content = request.get_json()
    created_bool = create_user(user_id=content["user_id"], user_name=content["user_name"])
    resp_dict = {"user_id": content["user_id"], "created": created_bool}
    return jsonify(resp_dict)


@app.route("/api/add_tweet/", methods=["POST"])
def add_tweet():
    """
    api endpoint: /api/add_tweet/
    request supported methods: POST
    content type: application/json

    request json data model:
        - tweet_id: string
        - user_id: string
        - node_number: int
        - flagged: boolean
    
    response json data model:
        - tweet_id: string
        - created: boolean

    Note: tweet_id is assumed to be unique in nature.
    """

    content = request.get_json()
    created_bool = create_tweet(
        tweet_id=content["tweet_id"],
        user_id=content["user_id"],
        node_number=content["node_number"],
        flagged=content["flagged"],
    )
    resp_dict = {"tweet_id": content["tweet_id"], "created": created_bool}
    return jsonify(resp_dict)


@app.route("/api/edit_tweet/", methods=["POST"])
def edit_tweet():
    """
    api endpoint: /api/update_tweet/
    request supported methods: POST
    content type: application/json

    request json data model:
        - tweet_id: string
        - flagged: boolean
    
    response json data model:
        - tweet_id: string
        - updated: boolean

    Note: tweet_id is assumed to be unique in nature.
    """

    content = request.get_json()
    updated_bool = update_tweet(
        tweet_id=content["tweet_id"],
        flagged=content["flagged"],
    )
    resp_dict = {"tweet_id": content["tweet_id"], "updated": updated_bool}
    return jsonify(resp_dict)


@app.route("/api/add_user_match/", methods=["POST"])
def add_user_match():
    """
    api endpoint: /api/add_user_match/
    request supported methods: POST
    content type: application/json

    request json data model:
        - from_user_id: string
        - to_user_id: string
        - tdna_conf: float

    response json data model:
        - from_user_id: string
        - to_user_id: string
        - tdna_conf: float
        - created: boolean

    Note: assumption is from_user_id and to_user_id are different, direction honestly doesn't matter in
    the end for our usecase.
    """

    content = request.get_json()
    created_bool = create_user_similarity(
        from_user_id=content["from_user_id"],
        to_user_id=content["to_user_id"],
        tdna_conf=content["tdna_conf"]
    )
    resp_dict = {
        "from_user_id": content["from_user_id"],
        "to_user_id": content["to_user_id"],
        "tdna_conf": content["tdna_conf"],
        "created": created_bool,
    }
    return jsonify(resp_dict)


@app.route("/api/add_tweet_verification/", methods=["POST"])
def add_verification():
    """
    api endpoint: /api/add_tweet_verification/
    request supported methods: POST
    content type: application/json

    request json data model:
        - user_id: string
        - tweet_id: string
        - tdna_conf: float

    response json data model:
        - user_id: string
        - tweet_id: string
        - tdna_conf: float
        - created: boolean
    """

    content = request.get_json()
    created_bool = create_verified_similarity(
        from_user_id=content["user_id"],
        verified_tweet_id=content["tweet_id"],
        tdna_conf=content["tdna_conf"]
    )
    resp_dict = {
        "user_id": content["user_id"],
        "tweet_id": content["tweet_id"],
        "tdna_conf": content["tdna_conf"],
        "created": created_bool,
    }
    return jsonify(resp_dict)


@app.route("/api/add_tweet_unverification/", methods=["POST"])
def add_unverification():
    """
    api endpoint: /api/add_tweet_unverification/
    request supported methods: POST
    content type: application/json

    request json data model:
        - from_user_id: string
        - to_user_id: string
        - tdna_conf: float

    response json data model:
        - from_user_id: string
        - to_user_id: string
        - tdna_conf: float
        - created: boolean

    Note: assumption is from_user_id and to_user_id are different, direction honestly doesn't matter in
    the end for our usecase.
    """

    content = request.get_json()
    created_bool = create_authentication_failed(
        from_user_id=content["user_id"],
        unverified_tweet_id=content["tweet_id"],
    )
    resp_dict = {
        "user_id": content["user_id"],
        "tweet_id": content["tweet_id"],
        "created": created_bool,
    }
    return jsonify(resp_dict)


@app.route("/api/add_tweet_match/", methods=["POST"])
def add_tweet_match():
    """
    api endpoint: /api/add_tweet_match/
    request supported methods: POST
    content type: application/json

    request json data model:
        - user_id: string
        - tweet_id: string
        - tdna_conf: float

    response json data model:
        - user_id: string
        - tweet_id: string
        - tdna_conf: float
        - created: boolean
    """

    content = request.get_json()
    created_bool = create_tweet_impostor_similarity(
        impostor_user_id=content["user_id"],
        unverified_tweet_id=content["tweet_id"],
        tdna_conf=content["tdna_conf"]
    )
    resp_dict = {
        "user_id": content["user_id"],
        "tweet_id": content["tweet_id"],
        "tdna_conf": content["tdna_conf"],
        "created": created_bool,
    }
    return jsonify(resp_dict)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
