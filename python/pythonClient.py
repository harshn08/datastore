import comm_pb2

import socket               

import time

import struct

import base64

import io

from PIL import Image

from PIL import ImageDraw

from PIL import ImageFont

import binascii

from base64 import decodestring

import cStringIO

import pdb 

#from protobuf_to_dict import protobuf_to_dict 

from io import BytesIO 

from StringIO import *   

def writeImage(image_path, ownerId):

    with open(image_path,"rb") as file_handle:
   
        #image=str(base64.b64encode(file_handle.read()))
	
	#image=file(file_handle.read())
    	image=str(file_handle.read())
	#image=file("/home/gaurav/Pictures/1.png","rb").read()
	#imge=open("/home/gaurav/Pictures/testwrite.png","wb")
	#imge.write(image)
	#imge.close
	 
    	
    jobId = str(int(round(time.time() * 1000)))



    r = comm_pb2.Request()  

    

    r.body.job_op.job_id = jobId


    r.body.job_op.action = comm_pb2.JobOperation.ADDJOB


    r.body.job_op.data.name_space = "image"

    r.body.job_op.data.owner_id = ownerId

    r.body.job_op.data.job_id = jobId

    r.body.job_op.data.status = comm_pb2.JobDesc.JOBQUEUED

    r.body.job_op.data.options.node_type = comm_pb2.NameValueSet.NODE

    r.body.job_op.data.options.name = "operation"

    r.body.job_op.data.options.value = "image"

   # r.body.photoPayload.name="Write_Image"

    r.body.photoPayload.data=image
    print type(r.body.photoPayload.data)
 
  #  path = comm_pb2.NameValueSet()

  #  path.node_type = comm_pb2.NameValueSet.NODE

  #  path.name = "path"

  #  path.value = image
 
   # r.body.job_op.data.options.node.extend([path])

    r.header.originator = 1

    r.header.photoHeader.requestType=1
    
    #r.header.photoHeader.contentLength=image.size()

    r.header.routing_id = comm_pb2.Header.JOBS

    r.header.toNode = 1

    #r.header.
  
    msg = r.SerializeToString()

    return msg
    
def readImage(uuid,ownerId):

    print "in readImage uuid",uuid

    jobId1 = str(int(round(time.time() * 1000)))
    
    r = comm_pb2.Request()  

    r.body.job_op.job_id = jobId1

    r.body.job_op.action = comm_pb2.JobOperation.ADDJOB

    r.body.job_op.data.name_space = "image_read"

    r.body.job_op.data.owner_id = ownerId

    r.body.job_op.data.job_id = jobId1

    r.body.job_op.data.status = comm_pb2.JobDesc.JOBQUEUED

    r.body.job_op.data.options.node_type = comm_pb2.NameValueSet.NODE

    r.body.job_op.data.options.name = "operation"

    r.body.job_op.data.options.value = "image"

    r.body.photoPayload.name="Read_Image"

    #r.body.photoPayload.data=image
    
    r.body.photoPayload.uuid=uuid
    print "in body uuid is ",r.body.photoPayload.uuid
 
  #  path = comm_pb2.NameValueSet()

  #  path.node_type = comm_pb2.NameValueSet.NODE

  #  path.name = "path"

  #  path.value = image
 
   # r.body.job_op.data.options.node.extend([path])

    r.header.originator = 1

    r.header.photoHeader.requestType=0
    
   # r.header.photoHeader.contentLength=image.size()

    r.header.routing_id = comm_pb2.Header.JOBS

    r.header.toNode = 1

    #r.header.
    
    #print "request builder",r
   # print "request\n",r
  
    msg = r.SerializeToString()
    
  #  print "Message::",msg

    return msg

#delete


def deleteImage(uuid, ownerId):

    jobId = str(int(round(time.time() * 1000)))
    
    r = comm_pb2.Request()  

    r.body.job_op.job_id = jobId

    r.body.job_op.action = comm_pb2.JobOperation.ADDJOB

    r.body.job_op.data.name_space = "delete image"

    r.body.job_op.data.owner_id = ownerId

    r.body.job_op.data.job_id = jobId

    r.body.job_op.data.status = comm_pb2.JobDesc.JOBQUEUED

    r.body.job_op.data.options.node_type = comm_pb2.NameValueSet.NODE

    r.body.job_op.data.options.name = "operation"

    r.body.job_op.data.options.value = "image"

    r.header.originator = 1

    r.header.photoHeader.requestType=2
    
    r.header.routing_id = comm_pb2.Header.JOBS

    r.header.toNode = 1
    
    r.body.photoPayload.uuid=uuid
    

    msg = r.SerializeToString()

    return msg
  
def writeImage(image_path, ownerId):

    with open(image_path,"rb") as file_handle:
   
        #image=str(base64.b64encode(file_handle.read()))
	
	#image=file(file_handle.read())
    	image=str(file_handle.read())
	#image=file("/home/gaurav/Pictures/1.png","rb").read()
	#imge=open("/home/gaurav/Pictures/testwrite.png","wb")
	#imge.write(image)
	#imge.close
	 
    	
    jobId = str(int(round(time.time() * 1000)))



    r = comm_pb2.Request()  

    

    r.body.job_op.job_id = jobId


    r.body.job_op.action = comm_pb2.JobOperation.ADDJOB


    r.body.job_op.data.name_space = "image"

    r.body.job_op.data.owner_id = ownerId

    r.body.job_op.data.job_id = jobId

    r.body.job_op.data.status = comm_pb2.JobDesc.JOBQUEUED

    r.body.job_op.data.options.node_type = comm_pb2.NameValueSet.NODE

    r.body.job_op.data.options.name = "operation"

    r.body.job_op.data.options.value = "image"

   # r.body.photoPayload.name="Write_Image"

    r.body.photoPayload.data=image
    print type(r.body.photoPayload.data)
 
  #  path = comm_pb2.NameValueSet()

  #  path.node_type = comm_pb2.NameValueSet.NODE

  #  path.name = "path"

  #  path.value = image
 
   # r.body.job_op.data.options.node.extend([path])

    r.header.originator = 1

    r.header.photoHeader.requestType=1
    
    #r.header.photoHeader.contentLength=image.size()

    r.header.routing_id = comm_pb2.Header.JOBS

    r.header.toNode = 1

    #r.header.
  
    msg = r.SerializeToString()

    return msg
    

def buildNS():

    r = comm_pb2.Request()

    r.body.space_op.action = comm_pb2.NameSpaceOperation.ADDSPACE

    r.header.originator = "python client"

    r.header.tag = str(int(round(time.time() * 1000)))

    r.header.routing_id = comm_pb2.Header.NAMESPACES

    r.header.photoHeader.requestType=1

    m = r.SerializeToString()

    return m

def buildCompetitionJob(name_space, jobAction, ownerId):

    jobId = str(int(round(time.time() * 1000)))

    r = comm_pb2.Request()    

    r.body.job_op.job_id = jobId

    r.body.job_op.action = comm_pb2.JobOperation.ADDJOB

    r.body.job_op.data.name_space = name_space

    r.body.job_op.data.owner_id = ownerId

    r.body.job_op.data.job_id = jobId

    r.body.job_op.data.status = comm_pb2.JobDesc.JOBQUEUED

    r.header.originator = "python client"  

    r.header.routing_id = comm_pb2.Header.JOBS

    r.header.toNode = str(3)

    msg = r.SerializeToString()

    return msg    

def sendMsg(msg_out, port, host):

   # print "in sendmsg"

    s = socket.socket()         

#    host = socket.gethostname()

#    host = "192.168.0.87"


   # print "\n in sendMsg sending msg: msg_out-->"+msg_out

    s.connect((host, port))        

    msg_len = str(struct.pack('>L', len(msg_out)))    

   # print "type of len ::"

   # print msg_len


    s.sendall(msg_len + msg_out)

    len_buf = receiveMsg(s, 4)
    
   # print "in sendMsg received msg len:len_buf-->"+len_buf

    msg_in_len = struct.unpack('>L', len_buf)[0]

    msg_in = receiveMsg(s, msg_in_len)
   
   # print "in sendMsg received msg: msg_in-->", msg_in

   # print " \n msg_in in send msg:", msg_in

    r = comm_pb2.Request()

    r.ParseFromString(msg_in)

#    print msg_in

#    print r.body.job_status 

#    print r.header.reply_msg

#    print r.body.job_op.data.options

    s.close

    return r

def receiveMsg(socket, n):

 #   print "In receive msg"

    buf = ''

    while n > 0:        

        data = socket.recv(n)                  

        if data == '':

            raise RuntimeError('data not received!')

        buf += data

        n -= len(data)
        
       # print "buf in receiveMsg",buf

    return buf  





def getBroadcastMsg(port):

    # listen for the broadcast from the leader"

          

    sock = socket.socket(socket.AF_INET,  # Internet

                        socket.SOCK_DGRAM)  # UDP

    sock.bind(('', port))

   

    data = sock.recv(1024)  # buffer size is 1024 bytes

    return data

        

   

if __name__ == '__main__':

    # msg = buildPing(1, 2)

    # UDP_PORT = 8080

    # serverPort = getBroadcastMsg(UDP_PORT) 

    host = raw_input("IP:")

    port = raw_input("Port:")

    port = int(port)

   
    choice=raw_input("Enter your choice\n1.Write\n2.Read\n3.Delete\n")
    
    
  
    if choice=="1":

        image_path = raw_input("Enter image path: ")

        re_writeImage = writeImage(image_path, 1) 
    
        result = sendMsg(re_writeImage, port, host)

        whoAmI = result.body.job_status.data[0].owner_id

        response=result.header.photoHeader.responseFlag

        print "response",response
        
        print "result",result

      
 
    if choice=="2":
    
        uuid= raw_input("Enter uuid of image: ")
        
        response_image=readImage(uuid,1)
        
        result = sendMsg(response_image, port, host)
       
        r_data =result.body.photoPayload.data
		#print type(r_data)
        imge=open("test.png","wb")
        imge.write(r_data)
        imge.close
        print "Result",result
       
	
	

    if choice=="3":

        uuid=raw_input("Enter uuid for delete")

        delete_img=deleteImage(uuid,1)

        result = sendMsg(delete_img, port, host)
        
        print "Result",result
       

        
