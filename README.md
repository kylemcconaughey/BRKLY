# [BRKLY: Backend API](https://brkly.herokuapp.com/)
![Barkley Logo](https://brkly.s3.amazonaws.com/post_images/barkley_logo.png)
## BRKLY is a REST API built with Django, for use with the Barkley front-end app using React. 

The [BRKLY API](https://brkly.herokuapp.com/) allows users to create dog and owner profiles, connect with other users via direct message and discussion boards, schedule meetups based on location, and share posts to a newsfeed.

---------------------------------------------------------------

### Models that exist
| Model | Notes |
| ----- | ----- |
| User |  |
| Dog | <3 |
| Conversation |  |
| Message |  |
| Meetup |  |
| DiscussionBoard | Posting requires just the title & body |
| Note | Notes go on discussion boards, displayed in order of `total_votes` |
| Post | Foreign key to user and dog |
| Comment | Requires `post` and `body` |
| Reaction | Reaction is a CharField |
| Request | proposing=`self.request.user`, recieving=`/users/<pk>/` |

---------------------------------------------------------------

### Endpoints: 
| HTTP Method | Endpoint | Result | Notes |
| ----------- | -------- | -------| ----- |
| POST | `/<basic model>/` | Creates a new instance |  |
| GET | `/<basic model>/` | Returns a list of all instances of that model |  |
| GET | `/<basic model>/<obj_pk>/` | Returns data about `<obj_pk>` object |  |
| POST | `/auth/token/login/` | Returns Auth Token | Requires `username` and `password` |
| GET | `/admin/` | Not so much for the API |  |
| POST | `/users/<user_pk>/follow/` | Adds self.request.user to `user_pk`'s follower list |  |
| POST | `/users/<user_pk>/unfollow/` | Removes `self.request.user` from `user_pk`'s follower list |  |
| POST | `/users/<user_pk>/request/ | Creates a `Request` object with `self.request.user` as proposing & `<user_pk>` as recieving |  |
| POST | `/users/<user_pk>/unfriend/` | Removes `<user_pk>` from `self.request.user`'s friend's list (it's symmetrical=True), deletes 'Request' object instance |  |
| GET | `/users/search/?q=<search term>` | Returns a list of all users with `search term` in their user/first/last/dog's name |  |
| GET | `/dogs/name_search/?=<search tearm>` | Returns a list of all dogs with names that match `search term` |  |
| GET | `/dogs/tag_search/?=<search tearm>` | Returns a list of all dogs with attributes that match `search term` |  |
| POST | `/requests/<req_pk>/accept/` | Sets `request.accepted = True`, adds `request.proposing` to `self.request.user`'s friends and vice versa |  |
| POST | `/requests/<req_pk>/deny/` | Deletes `Request` object |  |
| POST | `/messages/<msg_pk>/read/` | Adds `self.request.user` to the message's `read` M2M field |  |
| POST | `/comments/<pk>/like/` | Adds `self.request.user` to `Comment` object's `liked_by` list. | Removes `self.request.user` if already in `liked_by` list |
| POST | `/comments/` | Create a new comment | Requires both `post` Foreign Key and `body` text |
| POST | `/posts/<pk>/react/?r=<reaction>` | Creates a `Reaction` object of `<reaction>` for that post |  |
| GET | `/posts/mine/` | Returns a list of all of `self.request.user`'s posts |  |
| GET | `/posts/all/` | Returns a list of all posts from the logged-in user, their friends, and the people they follow |  |
| POST | `/discussionboards/<db_pk>/upvote/` | Adds `self.request.user` to board's upvotes M2M field | Removes `self.request.user` if already upvoted |
| POST | `/discussionboards/<db_pk>/downvote/` | Same as above but with downvotes | Both should be posted with empty bodies/no other data |
| POST | `/notes/<note_db>/upvote/` | Adds `self.request.user` to note's upvotes M2M field | Removes `self.request.user` if already upvoted |  |
| POST | `/notes/<note_db>/downvote/` | Same as above but with downvotes |  |
| TBD | `/user_list/` | Websockets coming soon! | But boy is it hard! |

---------------------------------------------------------------