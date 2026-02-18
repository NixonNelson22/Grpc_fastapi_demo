import grpc 
import av_pb2, av_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = av_pb2_grpc.AVServiceStub(channel)
resp = stub.GetStream(av_pb2.StreamReq(device_id="cam-001"))
print(f"Latency:{resp.latency_ms}ms, Status:{resp.status}")


