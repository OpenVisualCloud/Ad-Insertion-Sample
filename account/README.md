The Account service implements a REST service that returns the user profile information such as movie subscription and AD preference.

### User:

For simplicity, the implementation hard-coded a few users and their profile information as follows:

| Username | Subscription | AD Preference |
|:--------:|:------------:|:-------------:|
| guest    |    basic     |      any      |
| 20 popular names | universal | sports or family randomly selected at startup |
| others   |  universal   |      any      |

### Subscription:

The following subscription levels are supported:     

| Subscription | Description |
|:------------:|-------------|
| basic | Play three videos out of the video archive. |
| universal | Play all videos in the video archive.  |   

### AD Preference:

The supported AD preferences are as follows:    

| Preference | Description |
|:----------:|-------------|
|     any    | No preference. |
| sports     | Prefer to see sport related AD.  |   
| family     | Prefer to see family product AD. |   

### Interface:

The Account service exposes the following interface on port 8080:    
 
| Path | Description |
|----|------|
|GET /acct?name=\<user\>|The end point returns the user profile information. |
