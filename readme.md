
To build the Docker container:
```
docker build -t vid_sync`
```

To run the Docker container:
```
docker run -it -v ${PWD}:/vid_sync vid_sync
<maybe some docker exec command like: flask --app ...?>
```
