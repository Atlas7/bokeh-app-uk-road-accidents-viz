
```
docker build -t pyviz:v1 .
docker run -it --rm pyviz:1
docker run -it --rm -p 5006:5006 pyviz:1 bash
docker run -p 5006:5006 pyviz
docker exec -it <name of container you want to connect to> bash
```

```
List all containers (only IDs)
docker ps -aq
Stop all running containers
docker stop $(docker ps -aq)
Remove all containers
docker rm $(docker ps -aq)
Remove all images
docker rmi $(docker images -q)
```


Enter the new value, or press ENTER for the default
  Full Name []:   Room Number []:   Work Phone []:  Home Phone []:  Other []: Use of uninitialized value $answer in chop at /usr/sbin/adduser line 582.
Use of uninitialized value $answer in pattern match (m//) at /usr/sbin/adduser line 583.



docker run -it --rm -p 5006:5006 pyviz:2 bash



Problem:
ImportError: libGL.so.1: cannot open shared object file: No such file or directory

solution 1 (failed):
https://groups.google.com/forum/#!topic/py6s/yT37xNmJDVQ

apt-get install libgl1-mesa-glx

solution 2:
https://github.com/ContinuumIO/docker-images/issues/49
WARNING: apt does not have a stable CLI interface yet. Use with caution in scripts.

apt update
apt install libgl1-mesa-swx11




### Before going to bed...

to test locally (http://localhost/webapp)

```
docker run -i -t -p 80:5006 pyviz:4 /bin/bash -c "source activate pyviz && bokeh serve webapp --host=* --port=5006 --address=0.0.0.0 --use-xheaders"
```

Dockerfile:
CMD [ "source activate pyviz && bokeh serve webapp --host=* --port=$PORT --address=0.0.0.0 --use-xheaders" ]

docker run -i -t -p 5006:5006 pyviz:4 /bin/bash -c "source activate pyviz && bokeh serve webapp"

