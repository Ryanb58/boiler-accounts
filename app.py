from concurrent import futures
import os
import time
import sqlite3

import grpc

# import your gRPC bindings here:
from protos import accounts_pb2
from protos import accounts_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


# Using a dictionary for now.
USERS = [
    {
        "id": 1,
        "name": "Administrator",
        "email": "admin@example.com",
        "password": "password"
    }
]

# Helper Functions:

def getUserByEmail(email, password):
    user = list(filter(lambda user: user['email'] == email and user['password'] == password, USERS))
    if len(user) == 1:
        return user[0]
    return False


class AccountServicer(accounts_pb2_grpc.AccountServiceServicer):
# class AccountServicer(object):

    def dbConnect(self):
        self.dbconnection = sqlite3.connect("app.sqlite", check_same_thread=False)
        return self.dbconnection.cursor()

    def AuthenticateByEmail(self, request, context):
        user = getUserByEmail(request.email, request.password)
        if user:
            print("Authenticated: {}".format(request.email))
            return accounts_pb2.Account(
                id=str(user['id']),
                name=str(user['name']),
                email=str(user['email']))
        context.set_code(grpc.StatusCode.UNAUTHENTICATED)


def serve():
    print("Starting server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    accounts_pb2_grpc.add_AccountServiceServicer_to_server(AccountServicer(), server)
    server.add_insecure_port('[::]:22222')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    # Start gRPC server.
    serve()
