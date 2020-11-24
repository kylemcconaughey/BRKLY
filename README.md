# [BRKLY: Backend API](https://brkly.herokuapp.com/)
![Barkley Logo](https://brkly.s3.amazonaws.com/post_images/barkley_logo.png "Barkley Logo")
## BRKLY is a REST API built with Django, for use with the [Barkley](http://barkley.netlify.app/) front-end app using React. 

The [BRKLY API](https://brkly.herokuapp.com/) provides the backend & API of our Barkley app. Barkley allows users to create dog and owner profiles, connect with other users via direct message and discussion boards, schedule meetups based on location, and share posts to a newsfeed.

This was the final project for [Momentum Learning](https://www.momentumlearn.com/), created by [Clint Jordan](https://github.com/clintjordan5) and [Kyle McConaughey](https://github.com/kylemcconaughey).

---------------------------------------------------------------

### Models that exist
| Model | Notes |
| ----- | ----- |
| [User](https://brkly.herokuapp.com/users/) |  |
| [Dog](https://brkly.herokuapp.com/dogs/) | <3 |
| [Conversation](https://brkly.herokuapp.com/conversations/) |  |
| [Message](https://brkly.herokuapp.com/messages/) |  |
| [Meetup](https://brkly.herokuapp.com/meetups/) |  |
| [DiscussionBoard](https://brkly.herokuapp.com/discussionboards/) | Posting requires just the title & body |
| [Note](https://brkly.herokuapp.com/notes/) | Notes go on discussion boards, displayed in order of `total_votes` |
| [Post](https://brkly.herokuapp.com/posts/) | Foreign key to user and dog |
| [Comment](https://brkly.herokuapp.com/comments/) | Requires `post` and `body` |
| [Reaction](https://brkly.herokuapp.com/reactions/) | Reaction is a CharField |
| [Request](https://brkly.herokuapp.com/requests/) | proposing=`self.request.user`, recieving=`/users/<pk>/` |

---------------------------------------------------------------

### Endpoints: 
| HTTP Method | Endpoint | Result | Notes |
| ----------- | -------- | -------| ----- |
| POST | `/<basic model>/` | Creates a new instance |  |
| GET | `/<basic model>/` | Returns a list of all instances of that model |  |
| GET | `/<basic model>/<obj_pk>/` | Returns data about `<obj_pk>` object |  |
| POST | `/auth/token/login/` | Returns Auth Token | Requires `username` and `password` |
| GET | `/admin/` | Not so much for the API |  |
|     | User Friending/Following & Dog Endpoints, & Search |  |  |
| -------- | -------- | -------- | -------- |
| POST | `/users/<user_pk>/follow/` | Adds self.request.user to `user_pk`'s follower list |  |
| POST | `/users/<user_pk>/unfollow/` | Removes `self.request.user` from `user_pk`'s follower list |  |
| POST | `/users/<user_pk>/request/` | Creates a `Request` object with `self.request.user` as proposing & `<user_pk>` as recieving |  |
| POST | `/users/<user_pk>/unfriend/` | Removes `<user_pk>` from `self.request.user`'s friend's list (it's symmetrical=True), deletes 'Request' object instance |  |
| GET | `/users/search/?q=<search term>` | Returns a list of all users with `search term` in their user/first/last/dog's name |  |
| GET | `/dogs/name_search/?=<search tearm>` | Returns a list of all dogs with names that match `search term` |  |
| GET | `/dogs/tag_search/?=<search tearm>` | Returns a list of all dogs with attributes that match `search term` |  |

|  | Requests, Convos, Messaging |  |  |
| -------- | -------- | -------- | -------- |
| POST | `/requests/<req_pk>/accept/` | Sets `request.accepted = True`, adds `request.proposing` to `self.request.user`'s friends and vice versa |  |
| POST | `/requests/<req_pk>/deny/` | Deletes `Request` object |  |
| POST |   `/conversations/<convo_pk>/message/` | Creates a `Message` object - sender=`self`, convo=`<convo_pk>`, `read_by.add(self)` | Requires `body`, can include `image`, will not accept anything else |
| POST | `/messages/<msg_pk>/read/` | Adds `self.request.user` to the message's `read` M2M field |  |
| POST | `/comments/<pk>/like/` | Adds `self.request.user` to `Comment` object's `liked_by` list. | Removes `self.request.user` if already in `liked_by` list |
| POST | `/comments/` | Create a new comment | Requires both `post` Foreign Key and `body` text |

|      | Social Media |          |          |
| -------- | -------- | -------- | -------- |
| POST | `/posts/<pk>/react/?r=<reaction>` | Creates a `Reaction` object of `<reaction>` for that post |  |
| GET | `/posts/mine/` | Returns a list of all of `self.request.user`'s posts |  |
| GET | `/posts/all/` | Returns a list of all posts from the logged-in user, their friends, and the people they follow |  |
| GET | `/posts/theirs/?p=<user_pk>` | Returns a list of all of `user_pk`'s posts |  |

|     | Discussion Forum |      |       |
| -------- | -------- | -------- | -------- |
| POST | `/discussionboards/<db_pk>/upvote/` | Adds `self.request.user` to board's upvotes M2M field | Removes `self.request.user` if already upvoted |
| POST | `/discussionboards/<db_pk>/downvote/` | Same as above but with downvotes | Both should be posted with empty bodies/no other data |
| POST | `/notes/<note_db>/upvote/` | Adds `self.request.user` to note's upvotes M2M field | Removes `self.request.user` if already upvoted |  |
| POST | `/notes/<note_db>/downvote/` | Same as above but with downvotes |  |

|       | Notifications/Websockets |        |       |
| -------- | -------- | -------- | -------- |
| GET | `/notifications/mine/` | Returns a list of all of `self.request.user`'s notifications | Does not involve websockets at all, this is currently a semi-static list, in that it will update if the page is refreshed but not otherwise |
| POST | `/notifications/ping/?p=<username>` | Creates a `Notification` object where `sender` = `self.request.user`, `recipient` = `<username>`, and `trigger` = `"mention"` | Do not put quotes or anything around `<username>` in the url, do not send anything in the body of the POSTing, the API will auto-fill everything |
| GET | `/websockets/` | HTML page with unordered list of notifications | Currently points to an HTML template, needs to change but I'm not sure how - probably involves front-end setting up some websocket stuff to receive notifications? |

---------------------------------------------------------------

## Model Construction

### Notification
```
{
    "sender": ForeignKey(to=User)
    "recipient": ForeignKey(to=User)
    "created_at": DateTimeField
    "opned": BooleanField
    "trigger": CharField [Current options: "Message", "Mention", "Request"]
}
```

### User
```
{
    "first_name": CharField
    "last_name": CharField
    "last_name_is_public": BooleanField
    "num_pets": IntegerField
    "street_address": CharField
    "address_is_public": BooleanField
    "city": CharField
    "state": CharField
    "created_at": DateTimeField
    "phone_num": CharField
    "phone_is_public": BooleanField
    "birthdate": DateField
    "picture": ImageField
    "followers": ManyToManyField
    "friends": ManyToManyField
}
```

### Dog
```
{
    "owner": ForeignKey(to=User)
    "name": CharField
    "breed": CharField
    "picture": ImageField
    "age": IntegerField
    "created_at": DateTimeField
    "size": CharField/TextChoices
    "energy": CharField/TextChoices
    "temper": CharField/TextChoices
    "group_size": CharField/TextChoices
    "vaccinated": CharField/TextChoices
    "kid_friendly": CharField/TextChoices
}
```

### Conversation
```
{
    "members": ManyToManyField(to=User)
    "created_at": DateTimeField
    "convo_name": CharField
    "admin": ForeignKey(to=User)  - auto adds `self.request.user` upon creation
}
```

### Message
```
{
    "sender": ForeignKey(to=User)
    "conversation": ForeignKey(to=Conversation)
    "time_sent": DateTimeField
    "body": TextField
    "reactions": ManyToManyField(to=Reaction)
    "image": ImageField
    "read_by": ManyToManyField(to=User)
}
```

### Meetup
```
{
    "admin": ForeignKey(to=User)
    "attending": ManyToManyField(to=User)
    "start_time": DateTimeField
    "end_time": DateTimeField
    "location": ForeignKey(to=Location)
}
```

### DiscussionBoard
```
{
    "title": CharField
    "body": TextField
    "user": ForeignKey(to=User)
    "posted_at": DateTimeField
    "upvotes": ManyToManyField(to=User)
    "downvotes": ManyToManyField(to=User)
}
```

### Note
```
{
    "body": TextField
    "board": ForeignKey(to=DiscussionBoard)
    "user": ForeignKey(to=User)
    "posted_at": DateTimeField
    "upvotes": ManyToManyField(to=User)
    "downvotes": ManyToManyField(to=User)
    "num_upvotes": IntegerField
    "num_downvotes": IntegerField
    "def total_votes": returns self.num_upvotes - self.num_downvotes
}
```

### Post
```
{
    "body": CharField
    "dog": ForeignKey(to=Dog)
    "posted_at": DateTimeField
    "user": ForeignKey(to=User)
    "font_style": CharField/TextChoices
    "text_align": CharField/TextChoices
    "font_size": CharField/TextChoices
    "image": ImageField
    "liked_by": ManyToManyField(to=User)
    "reactions": ManyToManyField(to=Reaction)
}
```

### Comment
```
{
    "body": CharField
    "post": ForeignKey(to=Post)
    "user": ForeignKey(to=User)
    "posted_at": DateTimeField
    "liked_by": ManyToManyField(to=User)
}
```

### Reaction
```
{
    "reaction": CharField
    "user": ForeignKey(to=User)
}
```

### Request
```
{
    "proposing": ForeignKey(to=User)
    "receiving": ForeignKey(to=User)
    "accepted": BooleanField
}
```
