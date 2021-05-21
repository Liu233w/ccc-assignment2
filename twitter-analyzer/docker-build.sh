#!/bin/bash

docker build -t liu233w/ccc-assignment2-analyser-uploader \
  --build-arg http_proxy=http://wwwproxy.unimelb.edu.au:8000/ \
  --build-arg https_proxy=http://wwwproxy.unimelb.edu.au:8000/ \
  . \
&& docker push liu233w/ccc-assignment2-analyser-uploader