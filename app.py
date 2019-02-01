# Help the system find the proto library:
import sys
sys.path.append('./protos')

from concurrent import futures
import os
import time
import random

import grpc
import sqlite3
from google.protobuf import empty_pb2

# import your gRPC bindings here:
from protos import accounts_pb2
from protos import accounts_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


# Using a dictionary for now.
USERS = [
    {
        "id": "1",
        "name": "Administrator",
        "email": "admin@example.com",
        "password": "password"
    }
]

# Helper Functions:

def getUsersIndex(pk):
    for index, user in enumerate(USERS):
        if int(user['id']) == int(pk):
            return index
    return -1


def getUserByID(pk):
    user = list(filter(lambda user: int(user['id']) == int(pk), USERS))
    if len(user) == 1:
        return user[0]
    return False

def getUserByEmail(email):
    user = list(filter(lambda user: user['email'] == email, USERS))
    if len(user) == 1:
        return user[0]
    return False

def getUserByEmailAndPassword(email, password):
    user = list(filter(lambda user: user['email'] == email and user['password'] == password, USERS))
    if len(user) == 1:
        return user[0]
    return False


class AccountServicer(accounts_pb2_grpc.AccountServiceServicer):
# class AccountServicer(object):

    def AuthenticateByEmail(self, request, context):
        user = getUserByEmailAndPassword(request.email, request.password)
        if user:
            print("Authenticated: {}".format(request.email))
            return accounts_pb2.Account(
                id=str(user['id']),
                name=str(user['name']),
                email=str(user['email']))
        context.set_code(grpc.StatusCode.UNAUTHENTICATED)

    def GetByID(self, request, context):
        account = getUserByID(request.id)
        if account:
            return accounts_pb2.Account(
                id=str(account['id']),
                name=str(account['name']),
                email=str(account['email']))
        context.set_code(grpc.StatusCode.NOT_FOUND)

    def List(self, request, context):
        serialized_accounts = []
        for user in USERS:
            serialized_accounts.append(
                accounts_pb2.Account(
                    id=str(user['id']),
                    name=str(user['name']),
                    email=str(user['email'])
                )
            )

        return accounts_pb2.ListAccountsResponse(
            accounts=serialized_accounts
        )

    def Create(self, request, context):
        # Check to see if they already exist:
        if getUserByEmail(request.account.email):
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return

        USERS.append(
            {
                "id": random.randint(2, 100),
                "name": request.account.name,
                "email": request.account.email,
                "password": request.password
            }
        )
        user = getUserByEmail(request.account.email)
        print("User Created: {}".format(user['email']))
        return accounts_pb2.Account(
                id=str(user['id']),
                name=str(user['name']),
                email=str(user['email']))

    def Update(self, request, context):
        # Check to see if they already exist:
        user = getUserByID(request.id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return
        if request.account.name:
            user["name"] = request.account.name
        if request.account.email:
            user["email"] = request.account.email
        if request.password:
            user["password"] = request.password

        user = getUserByEmail(request.account.email)
        print("User Updated: {}".format(user['id']))
        return accounts_pb2.Account(
                id=str(user['id']),
                name=str(user['name']),
                email=str(user['email']))

    def Delete(self, request, context):
        # Check to see if they already exist:
        index = getUsersIndex(request.id)
        if index == -1:
            context.set_code(grpc.StatusCode.UNKNOWN)
            return

        if int(USERS[index]['id']) != int(request.id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return

        del USERS[index]

        user = getUserByID(request.id)

        if user:
            context.set_code(grpc.StatusCode.UNKNOWN)
            return

        print("Deleted user {}".format(request.id))
        return empty_pb2.Empty()


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
