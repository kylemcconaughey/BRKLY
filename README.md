# BRKLY: Backend API

## BRKLY is a REST API built with Django, for use with the Barkley front-end app using React. 

The API allows users to create dog and owner profiles, connect with other users via direct message and discussion boards, schedule meetups based on location, and share posts to a newsfeed. 

### Endpoints: 
| HTTP Method | Endpoint | Result | Notes |
| ----------- | -------- | -------| ----- |
| POST | `<basic model>` | Creates a new instance |  |
| GET | `<basic model>` | Returns a list of all instances of that model |  |
| GET | `<basic model>/<obj_pk>/` | Returns data about `<obj_pk>` object |  |
| GET | `/dogs/tag_search/?=<search tearm>` | Returns a list of all dogs that match `search term` |  |
| GET | `/dogs/name_search/?=<search tearm>` | Returns a list of all dogs that match `search term` |  |
| GET | `/users/search/?q=<search term>` | Returns a list of all users with `search term` in their user/first/last/dog's name |  |
| POST | `/users/<user_pk>/follow/` | Adds self.request.user to `user_pk`'s follower list |  |
| POST | `users/<user_pk>/unfollow/` | Removes `self.request.user` from `user_pk`'s follower list |  |
| POST | `users/<user_pk>/request/ | Creates a `Request` object with `self.request.user` as proposing & `<user_pk>` as recieving |  |
| POST | `users/<user_pk>/unfriend/` | Removes `<user_pk>` from `self.request.user`'s friend's list (it's symmetrical=True), deletes 'Request' object instance |  |
| POST | `requests/<req_pk>/accept/` | Sets `request.accepted = True`, adds `request.proposing` to `self.request.user`'s friends and vice versa |  |
| POST | `requests/<req_pk>/deny/` | Deletes `Request` object |  |
| POST | `messages/<msg_pk>/read/` | Adds `self.request.user` to the message's `read` M2M field |  |
| POST | `/comments/<pk>/like/` | Adds `self.request.user` to `Comment` object's `liked_by` list. | Removes `self.request.user` if already in `liked_by` list |
| POST | `/posts/<pk>/react/?r=<reaction>` | Creates a `Reaction` object of `<reaction>` for that post |  |
| GET | `/posts/mine/` | Returns a list of all of `self.request.user`'s posts |  |
| GET | `/posts/all/` | Returns a list of all posts from the logged-in user, their friends, and the people they follow |  |
| POST | `/discussionboards/<db_pk>/upvote/` | Adds `self.request.user` to board's upvotes M2M field | Removes `self.request.user` if already upvoted |
| POST | `/discussionboards/<db_pk>/downvote/` | Same as above but with downvotes | Both should be posted with empty bodies/no other data |
| POST | `/notes/<note_db>/upvote/` | Adds `self.request.user` to note's upvotes M2M field | Removes `self.request.user` if already upvoted |  |
| POST | `/notes/<note_db>/downvote/` | Same as above but with downvotes |  |
| POST |  |  |  |
| POST |  |  |  |
| POST |  |  |  |
| POST |  |  |  |
| POST |  |  |  |
| POST |  |  |  |
| POST |  |  |  |



'/admin'
'/auth'
'/comments'
'/conversations'
'/discussionboards'
'/dogs'
'/locations'
'/maps'
'/media'
'/meetups'
'/messages'
'/notes'
'/posts'
'/reactions'
'/requests'
'/user_list'
'/users'

