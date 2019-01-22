from __future__ import print_function

import grpc

from protos import accounts_pb2
from protos import accounts_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('0.0.0.0:22222') as channel:
        stub = accounts_pb2_grpc.AccountServiceStub(channel)
        try:
            response = stub.AuthenticateByEmail(accounts_pb2.AuthenticateByEmailRequest(email='admin2@example.com', password='password'))
            print("Account client received: " + response.id)
        except grpc.RpcError as e:
            status_code = e.code()
            if status_code.name == "UNAUTHENTICATED":
                print("Sorry you are UNAUTHENTICATED")
            elif status_code.name == "UNAVAILABLE":
                print("Server is unavailable.")
            else:
                print(e)

if __name__ == '__main__':
    run()
