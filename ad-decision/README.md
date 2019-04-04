
The AD Decision Service 

The service makes decision on what AD to show in the next AD break, and returns the AD URL. The decision is based on combination of user AD preference and available cues, results from analyzing the video content.       

### Interface:

The AD Decision service exposes the following interface(s) on port 8080:      
 
| Path | Description |
|----|------|
|Get /metadata | return the reponse template. |
|POST /metadata | Submit the list of meta data (in the request body): {"metadata":[],"user":{"name":"","keywords":[]}}. Return the AD URL. |

