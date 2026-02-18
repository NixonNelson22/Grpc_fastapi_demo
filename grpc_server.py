import grpc 
from concurrent import futures
import redis
import av_pb2, av_pb2_grpc
import time, random


r = redis.Redis(host='localhost', port=6379)

class AVServicer(av_pb2_grpc.AVServiceServicer):
    def GetStream(self, req, context):
        device = req.device_id
        cached = r.get(f"av:{device}")
        if cached :
            latency = float(cached)
            status = "cached"
        else:
            latency = round(random.uniform(20,100),2)
            r.setex(f"av:{device}",300, latency)
            status = "computed"
        return av_pb2.StreamResp(latency_ms=latency,status=status)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
av_pb2_grpc.add_AVServiceServicer_to_server(AVServicer(),server)
server.add_insecure_port('[::]:50051')
server.start()
print("gRPC on 50051 , redis 6379")
server.wait_for_termination()

