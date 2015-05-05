#!/bin/bash
project_base=/Users/Harsh/Documents/Eclipse/poke-netty
protoc_home=/usr/local/bin

rm ${project_base}/python/comm_pb2.py 

${protoc_home}/protoc -I=${project_base}/resources --python_out=. ${project_base}/resources/comm.proto
