from google.protobuf import duration_pb2


dur = duration_pb2.Duration()
dur.nanos = 4521
print(dur)