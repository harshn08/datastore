 /* 

 * Gash licenses this file to you under the Apache License,

 * version 2.0 (the "License"); you may not use this file except in compliance

 * with the License. You may obtain a copy of the License at:

 *

 *   http://www.apache.org/licenses/LICENSE-2.0

 *

 * Unless required by applicable law or agreed to in writing, software

 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT

 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the

 * License for the specific language governing permissions and limitations
*/

package poke.resources;


import io.netty.bootstrap.Bootstrap;

import io.netty.channel.Channel;

import io.netty.channel.ChannelFuture;

import io.netty.channel.ChannelOption;

import io.netty.channel.EventLoopGroup;

import io.netty.channel.nio.NioEventLoopGroup;

import io.netty.channel.socket.nio.NioSocketChannel;

import poke.server.conf.NodeDesc;


import java.net.InetSocketAddress;

import java.net.UnknownHostException;

import java.sql.Connection;

import java.sql.DriverManager;

import java.sql.PreparedStatement;


import poke.server.Server;

import poke.server.ServerInitializer;

import poke.server.hash.MurmurHash;

import poke.server.managers.ElectionManager;

import poke.server.resources.Resource;

import poke.server.resources.ResourceFactory;

import poke.server.resources.ResourceUtil;

import eye.Comm.JobDesc;

import eye.Comm.JobOperation;

import eye.Comm.JobStatus;

import eye.Comm.Payload;

import eye.Comm.PokeStatus;

import eye.Comm.Request;

import eye.Comm.*;


import java.nio.charset.*;

import java.util.*;

import java.util.logging.Logger;


import com.google.protobuf.ByteString;

import com.mongodb.BasicDBList;

import com.mongodb.BasicDBObject;

import com.mongodb.DB;

import com.mongodb.DBCollection;

import com.mongodb.DBCursor;

import com.mongodb.DBObject;

import com.mongodb.MongoClient;

import com.google.protobuf.ByteString;


import poke.server.conf.ServerConf;


import java.io.ByteArrayOutputStream;

import java.io.ObjectOutput;

import java.io.ObjectOutputStream;

import java.lang.*;

//import org.apache.commons.codec.binary.Base64;

import java.nio.charset.*;


import org.slf4j.LoggerFactory;



public class JobResource implements Resource {

//public PreparedStatement pst;

MongoClient mongoClient;

DB db;

DBCollection collection;

List<String> iplist;


@Override

public Request process(Request request) {

// TODO Auto-generated method stub

Request reply=null;

//slave part	

try{

mongoClient = new MongoClient();

db = mongoClient.getDB("cmpe275");

collection = db.getCollection("TestClient");

BasicDBObject userDoc = new BasicDBObject();


if(request.getHeader().getPhotoHeader().getRequestType().toString().equals("write"))

{

String uuid=UUID.randomUUID().toString().substring(0,5);


System.out.println("fetching IP s from resources Fectory");

iplist=ResourceFactory.determineIP(request,uuid);

for(int i=0;i<iplist.size();i++)

{

System.out.println("IP s are::"+iplist.get(i));

WriteMul(iplist.get(i), uuid, request);

}

Request.Builder rb = Request.newBuilder();

JobOperation jobOp = request.getBody().getJobOp();

rb.setHeader(ResourceUtil.buildHeader(request.getHeader().getRoutingId(), PokeStatus.SUCCESS, "Successfully stored",request.getHeader().getOriginator(),request.getHeader().getTag()));

Payload.Builder pb = Payload.newBuilder();

JobStatus.Builder jb = JobStatus.newBuilder();

jb.setJobId(jobOp.getJobId());

jb.setStatus(PokeStatus.SUCCESS);

jb.setJobState(JobDesc.JobCode.JOBRECEIVED);

JobDesc.Builder jd = JobDesc.newBuilder();

jd.setStatus(JobDesc.JobCode.JOBRECEIVED);

jd.setOwnerId(request.getBody().getJobOp().getData().getOwnerId());

jd.setJobId(request.getBody().getJobOp().getJobId());

jd.setNameSpace(request.getBody().getJobOp().getData().getNameSpace());

jb.addData(jd.build());

PhotoPayload.Builder phb= PhotoPayload.newBuilder();

phb.setUuid(uuid);

//phb.setData((ByteString)image);

pb.setPhotoPayload(phb.build());

pb.setJobStatus(jb.build());

rb.setBody(pb.build());

reply = rb.build();

}

else if(request.getHeader().getPhotoHeader().getRequestType().toString().equals("read"))

{

System.out.println("in else if in read()");

ByteString image = null;

Request.Builder rb = Request.newBuilder();


JobOperation jobOp = request.getBody().getJobOp();


rb.setHeader(ResourceUtil.buildHeader(request.getHeader().getRoutingId(), PokeStatus.SUCCESS, "Successfully stored",request.getHeader().getOriginator(),request.getHeader().getTag()));


Payload.Builder pb = Payload.newBuilder();


JobStatus.Builder jb = JobStatus.newBuilder();


jb.setJobId(jobOp.getJobId());


jb.setStatus(PokeStatus.SUCCESS);


jb.setJobState(JobDesc.JobCode.JOBRECEIVED);


JobDesc.Builder jd = JobDesc.newBuilder();


//jd.setNameSpace("result");


//jd.setJobId(jobOp.getJobId());

jd.setJobId(request.getBody().getJobOp().getJobId());


jd.setNameSpace(request.getBody().getJobOp().getData().getNameSpace());


jd.setStatus(JobDesc.JobCode.JOBRECEIVED);


jd.setOwnerId(request.getBody().getJobOp().getData().getOwnerId());


jb.addData(jd.build());


PhotoPayload.Builder phb= PhotoPayload.newBuilder();



String uuid=request.getBody().getPhotoPayload().getUuid();


DBCursor result=collection.find(new BasicDBObject("_id",uuid));

    while(    result.hasNext())

    {

        DBObject img=result.next();

        System.out.println("Result"+ result.toString());

        uuid = ""+img.get("uuid");

        System.out.println(uuid);

        ByteArrayOutputStream bos = new ByteArrayOutputStream();

        ObjectOutput out = null;

        out = new ObjectOutputStream(bos);   

          out.writeObject(img.get("image"));

          byte[] bytes = bos.toByteArray();    

         

        image = ByteString.copyFrom(bytes);

        System.out.println("Image"+image);

    }    

   

pb.setPhotoPayload(phb.build());


pb.setJobStatus(jb.build());


rb.setBody(pb.build());


reply = rb.build();

System.out.println("Built Reply\n"+reply);

phb.setData(image);


pb.setPhotoPayload(phb.build());


pb.setJobStatus(jb.build());


rb.setBody(pb.build());

reply=rb.build();


}

else{

System.out.println("Deleting from all nodes");

String uuid=request.getBody().getPhotoPayload().getUuid();

iplist=ResourceFactory.determineIP(request,uuid);

for(int i=0;i<iplist.size();i++)

{

System.out.println("IP s are::"+iplist.get(i));

delMul(iplist.get(i), uuid, request);

}

}

}


catch (Exception ex){

ex.printStackTrace();



}

return reply;

}



public void WriteMul(String ip,String uuid,Request request) throws Exception{

MongoClient mongoClient;

DB db;

DBCollection collection;

Request reply=null;

mongoClient = new MongoClient(ip);

db = mongoClient.getDB("cmpe275");

collection = db.getCollection("TestClient");

BasicDBObject userDoc = new BasicDBObject();


System.out.println("request.getHeader().getPhotoHeader().getRequestType(): " + request.getHeader().getPhotoHeader().getRequestType());



System.out.println("We are inside the if condition for write process.");

   

byte[]img = request.getBody().getPhotoPayload().getData().toByteArray();

System.out.println("IMG: " + img);

userDoc.put("_id", uuid);

userDoc.put("image", img);

   

collection.insert(userDoc);

if(ip!="localhost") mongoClient.close();


}



public void delMul(String ip,String uuid,Request request) throws Exception{

MongoClient mongoClient;

DB db;

DBCollection collection;

System.out.println("in delMul");

mongoClient = new MongoClient(ip);

db = mongoClient.getDB("cmpe275");

collection = db.getCollection("TestClient");

//DBObject dbObject = collection.findOne(new BasicDBObject("_id", uuid));

//collection.remove(dbObject);
System.out.println("uuid \ndbObject "+uuid);
collection.remove(new BasicDBObject().append("_id", uuid));

if(ip!="localhost") mongoClient.close();


}


}


