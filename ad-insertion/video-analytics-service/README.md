# Video Analytics Service

The Video Analytics Service exposes a set of RESTful interfaces designed to simplify the deployment and use of hardware optimized video analytics pipelines. It offers RESTful interfaces to customize and execute pre-defined pipelines in either [GStreamer](https://github.com/opencv/gst-video-analytics/wiki)
 or [FFmpeg](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/doc/ffmpeg.md). Each pipeline type defines the semantics of its customizable parameters. Pipeline developers define named and versioned pipelines and expose them to users via simple RESTful interfaces. 

## Architecture Overview
<img src="../../volume/html/image/video_analytics_service_architecture.png" width="800">

## Interfaces

| Path | Description |
|----|------|
| [`GET` /models](interfaces.md#get-models) | Return supported models. |
| [`GET` /pipelines](interfaces.md#get-pipelines) | Return supported pipelines |
| [`GET` /pipelines/{name}/{version}](interfaces.md#get-pipelinesnameversion)  | Return pipeline description.|
| [`POST` /pipelines/{name}/{version}](interfaces.md#post-pipelinesnameversion) | Start new pipeline instance. |
| [`DELETE` /pipelines/{name}/{version}/{instance_id}](interfaces.md#delete-pipelinesnameversioninstance_id) | Stop pipeline instance. |
| [`GET` /pipelines/{name}/{version}/{instance_id}](interfaces.md#get-pipelinesnameversioninstance_id) | Return pipeline instance summary. |
| [`GET` /pipelines/{name}/{version}/{instance_id}/status](interfaces.md#get-pipelinesnameversioninstance_idstatus) | Return pipeline instance status. |

## Example Pipelines

The AD-Insertion E2E sample project contains two sample analytics pipelines.

|Pipeline| Description| Example Request| Example Detection|
|--------|------------|----------------|------------------|
|/pipelines/object_detection/1|Object Detection|curl localhost:8080/pipelines/object_detection/1 -X POST -H 'Content-Type: application/json' -d '{ "source": { "uri": "https://github.com/intel-iot-devkit/sample-videos/blob/master/bottle-detection.mp4?raw=true", "type": "uri" }, "destination": { "type": "file", "uri": "file:///tmp/results.txt"}}'|{"objects": [{"detection": {"bounding_box": {"x_max": 0.8820319175720215, "x_min": 0.7787219285964966, "y_max": 0.8876367211341858, "y_min": 0.3044118285179138}, "confidence": 0.6628172397613525, "label": "bottle", "label_id": 5}}], "resolution": {"height": 360, "width": 640}, "source": "https://github.com/intel-iot-devkit/sample-videos/blob/master/bottle-detection.mp4?raw=true", "timestamp": 7407821229}|
|/pipelines/emotion_recognition/1|Emotion Recognition|curl localhost:8080/pipelines/emotion_recognition/1 -X POST -H 'Content-Type: application/json' -d '{ "source": { "uri": "https://github.com/intel-iot-devkit/sample-videos/blob/master/head-pose-face-detection-male.mp4?raw=true", "type": "uri" }, "destination": { "type": "file", "uri": "file:///tmp/results1.txt"}}'|{"objects": [{"detection": {"bounding_box": {"x_max": 0.5859826803207397, "x_min": 0.43868017196655273, "y_max": 0.5278626084327698, "y_min": 0.15201044082641602}, "confidence": 0.9999998807907104, "label": "face", "label_id": 1}, "emotion": {"label": "neutral", "model": {"name": "0003_EmoNet_ResNet10"}}}], "resolution": {"height": 432, "width": 768}, "source": "https://github.com/intel-iot-devkit/sample-videos/blob/master/head-pose-face-detection-male.mp4?raw=true", "timestamp": 133083333333}|

## Building and Running the Video Analytics Service

The Video Analytis Service is built as a component of the AD-Insertion E2E sample project but can also be built and run as a standalone service.

### Building

To build the service as a standalone component execute the following commands from the top level directory.

```bash
(1) cd ad-insertion/video-analytics-service  
(2) ./build.sh     
```

### Running 

After the service is built it can be run using standard docker run commands (volume mounting is required only to see the sample results)

```bash
(1) sudo docker run -p8080:8080 -v/tmp:/tmp -d --rm video_analytics_service_gstreamer
```

### Sample Request

To run a simple pipeline request against a running Video Analytics Service use the following commands.
```bash
(1) curl localhost:8080/pipelines/object_detection/1 -X POST -H 'Content-Type: application/json' -d '{ "source": { "uri": "https://github.com/intel-iot-devkit/sample-videos/blob/master/bottle-detection.mp4?raw=true", "type": "uri" }, "destination": { "type": "file", "uri": "file:///tmp/results.txt"}}'

(2) tail -f /tmp/results.txt
```
### Sample Result
{"objects": [{"detection": {"bounding_box": {"x_max": 0.9027906656265259, "x_min": 0.792841911315918, "y_max": 0.8914870023727417, "y_min": 0.3036404848098755}, "confidence": 0.6788424253463745, "label": "bottle", "label_id": 5}}], "resolution": {"height": 360, "width": 640}, "source": "https://github.com/intel-iot-devkit/sample-videos/blob/master/bottle-detection.mp4?raw=true", "timestamp": 39854748603}



