# aldini-graph


## Instructions on getting up and running

``` sh
→ docker build --rm . -t among-us-neo4j

→ docker-compose --env-file app/.env up 
```

## Instructions on how to use the endpoints

Note: replace the IP with your DOCKER IP though. You can find it as `inet addr` under `docker0` in ifconfig. Also the NGINX_PORT has been purposefully set as 8080 (in the .env) so that aldini-backend can run on default port 80.

DOCKER_IP: 172.17.0.1

1. `/api/add_user/` which is used to create a new User node.

```
    api endpoint: /api/add_user/
    request supported methods: POST
    content type: application/json

    request json data model: user_id: string, user_name: string
```


```sh
→ curl -d '{"user_id":"j3", "user_name":"jaivarsan"}' -H "Content-Type: application/json" -X POST http://172.17.0.1:8080/api/add_user/
{"created":true,"user_id":"j3"}
```

2. `/api/add_tweet/` used for creating new Tweet.

```
    api endpoint: /api/add_tweet/
    request supported methods: POST
    content type: application/json

    request json data model:
        - tweet_id: string
        - user_id: string
        - node_number: int
        - flagged: boolean
```

```sh
→ curl -d '{"tweet_id": "12345", "user_id":"yas1", "node_number": 6, "flagged": false}' -H "Content-Type: application/json" -X POST http://172.17.0.1:8080/api/add_tweet/
{"created":true,"tweet_id":"12345"}
```


3. `/api/edit_tweet/` which is used to update the `flagged` property of the Tweet Node.

```
    api endpoint: /api/update_tweet/
    request supported methods: POST
    content type: application/json

    request json data model:
        - tweet_id: string
        - flagged: boolean
```

```sh
→ curl -d '{"tweet_id": "12345", "flagged": true}' -H "Content-Type: application/json" -X POST http://172.17.0.1:8080/api/edit_tweet/
{"tweet_id":"12345","updated":true}
```

4. `/api/add_user_match/` which is used to create similarity relationship between two existing User nodes.

```
    api endpoint: /api/add_user_match/
    request supported methods: POST
    content type: application/json

    request json data model:
        - from_user_id: string
        - to_user_id: string
        - tdna_conf: float
```

```sh
→ curl -d '{"from_user_id":"yas1", "to_user_id":"b2", "tdna_conf":0.8}' -H "Content-Type: application/json" -X POST http://172.17.0.1:8080/api/add_user_match/
{"created":true,"from_user_id":"yas1","tdna_conf":0.8,"to_user_id":"b2"}
```

5. `/api/add_tweet_verification/` which is used to send updates when tweet posted is legitimate and came from that actual user only.

```
    api endpoint: /api/add_tweet_verification/
    request supported methods: POST
    content type: application/json

    request json data model:
        - user_id: string
        - tweet_id: string
        - tdna_conf: float
```

```sh
→ curl -d '{"user_id": "yas1", "tweet_id": "12345", "tdna_conf": 0.9}' -H "Content-Type: application/json" -X POST http://172.17.0.1:8080/api/add_tweet_verification/
{"created":true,"tdna_conf":0.9,"tweet_id":"12345","user_id":"yas1"}
```

6. `/api/add_tweet_unverification/` which is where when the tweet hasn't been verified / authentication failed with typingDNA with the User's onboarding pattern.

```
    api endpoint: /api/add_tweet_unverification/
    request supported methods: POST
    content type: application/json

    request json data model:
        - from_user_id: string
        - to_user_id: string
        - tdna_conf: float
```

```sh
→ curl -d '{"user_id": "b2", "tweet_id": "12345"}' -H "Content-Type: application/json" -X POST http://172.17.0.1:8080/api/add_tweet_unverification/
{"created":true,"tweet_id":"12345","user_id":"b2"}
```

7. `/api/add_tweet_match/` when we found the impostor/similarity using the tweet pattern with the impostor's onboarding pattern.

```
    api endpoint: /api/add_tweet_match/
    request supported methods: POST
    content type: application/json

    request json data model:
        - user_id: string
        - tweet_id: string
        - tdna_conf: float
```

```sh
→ curl -d '{"user_id":"j3", "tweet_id":"12345", "tdna_conf":0.8}' -H "Content-Type: application/json" -X POST http://172.17.0.1:8080/api/add_tweet_match/
{"created":true,"tdna_conf":0.8,"tweet_id":"12345","user_id":"j3"}
```

now run to your browser & open [http://localhost:7474](http://localhost:7474) to see visualzations using [Neo4j Browser User Interface](https://neo4j.com/developer/neo4j-browser/)


## Visualization Usage

For demo purposes these commands might be useful:

* show all User nodes, Tweet nodes and relationships

``` 
MATCH (n) RETURN n
```

* delete all nodes and relationships

``` 
MATCH (n) DETACH DELETE n
```

* show all Users relationships

```
MATCH (n:User)-[r:SIMILAR]-(:User) RETURN n
```


* show all relationships based on property's value

```
MATCH (n:User)-[r:SIMILAR]-(:User) WHERE r.conf > 0.8 RETURN n
```

* show all verified tweets from every user account

```
MATCH (n:User)-[r:VERIFIED]-(t:Tweet) RETURN n, r, t
```

* show all verified tweets from one user account (usecase 1)

```
MATCH (n:User {name: "yaswant"})-[r:VERIFIED]-(t:Tweet) RETURN n, r, t
```

* show all verified+unverfied tweets from that one particular user account

```
MATCH (n:User {name: "yaswant"})-[:VERIFIED|:UNVERIFIED]-(t:Tweet) RETURN n, t
```

* show all verfied-flagged tweets from partciular User

```
MATCH (n:User {name:"shaaran"})-[:VERIFIED]-(t:Tweet {flagged:true}) RETURN n, t
```

* for a user, find all his flagged tweets and similar users to that user

```
MATCH (n:User {name:"shaaran"})-[:VERIFIED]-(t:Tweet {flagged:true}) 
MATCH (u:User)-[:USER_SIMILAR]-(n)
RETURN n, t, u
```

* for a particular verfied-tweet from the legit User, find other simlar users. (usecase 2)

```
MATCH (t:Tweet {tweet_id:"890"})-[:VERIFIED]-(u:User) 
MATCH (n:User)-[:USER_SIMILAR]-(u)
RETURN n, t, u
```

* for a particular unverfied-tweet, show the hacked user account and who is the impostor responsible
for that particular unverified-tweet. (usecase 3)

```
MATCH (t:Tweet {tweet_id:"456"})-[r1:UNVERIFIED]-(u1:User)
MATCH (t)-[r2:TWEET_SIMILAR]-(u2:User)
RETURN t, r1, u1, r2, u2
```
