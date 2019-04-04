The AD Content service archives the AD videos and serves them upon request.  

### Interface:

The AD Content service exposes the following interface(s) on 8080:      
 
| Path | Description |
|----|------|
|GET/| Return the AD video content. |
|GET/inventory| Returns the inventory. |
|GET/adstats | Return a stat page that shows the statistics of AD clips played. |
|POST/adstats | Submit an AD viewing report, in the request body. |

e.g. report to post 
{"uri":"cat.mp4", "clicked":1, "watched":1}

