The CDN service is a caching proxy of any content from the [AD Insertion](../ad-insertion/README.md) service or the [Content Provider](../content-provider/README.md) service.    

In addition, the CDN service implements a debug hook to show server activities and statistics.   

### Interface:

The CDN service exposes the following interface(s) on port 8443:    
 
| Path | Description |
|----|------|
|GET /|Proxy to the [AD Insertion](../ad-insertion/README.md) service. |
|GET /api/debug/analytics | Debug only: query the database for any analytics data to show on the UI analytics panel. |
|GET /api/debug | Debug only: listen on the Kafka topics and open a websocket connection to UI for showing messages in the debug console and charts. |
