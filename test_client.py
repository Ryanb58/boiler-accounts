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

        # Test authentication.
        try:
            response = stub.AuthenticateByEmail(accounts_pb2.AuthenticateByEmailRequest(email='admin@example.com', password='password'))
            print("Account ID received: " + response.id)
        except grpc.RpcError as e:
            status_code = e.code()
            if status_code.name == "UNAUTHENTICATED":
                print("Sorry you are UNAUTHENTICATED")
            elif status_code.name == "UNAVAILABLE":
                print("Server is unavailable.")
            else:
                print(e)

        print('-'*20)
        print("LIST:")

        # Test the list endpoint.
        response = stub.List(accounts_pb2.ListAccountsRequest(page_size=1, page_token="1"))
        for account in response.accounts:
            print(account)

        print('-'*20)
        print("CREATE:")

        account = accounts_pb2.Account(
            name="Leslie Knope",
            email='lknope@example.com'
        )

        createAccountRequest = accounts_pb2.CreateAccountRequest(
            account=account,
            password='password'
        )

        # Test the list endpoint.
        response = stub.Create(createAccountRequest)
        print(response)

        print('-'*20)
        print("LIST:")

        # Test the list endpoint.
        response = stub.List(accounts_pb2.ListAccountsRequest(page_size=1, page_token="1"))
        id_to_update = None
        for account in response.accounts:
            print(account)
            id_to_update = account.id

        print('-'*20)
        print("Update:")

        account = accounts_pb2.Account(
            name="Andy Dwyr",
            email='adwyr@example.com'
        )

        updateAccountRequest = accounts_pb2.UpdateAccountRequest(
            id=id_to_update,
            account=account,
            password='password',
        )

        # Test the list endpoint.
        response = stub.Update(updateAccountRequest)
        print(response)

        print('-'*20)
        print("LIST:")

        # Test the list endpoint.
        response = stub.List(accounts_pb2.ListAccountsRequest(page_size=1, page_token="1"))
        id_to_update = None
        for account in response.accounts:
            print(account)
            id_to_update = account.id

        print('-'*20)
        print("Delete:")

        deleteAccountRequest = accounts_pb2.DeleteAccountRequest(
            id=id_to_update,
        )

        # Test the list endpoint.
        response = stub.Delete(deleteAccountRequest)
        print(response)
        print('-'*20)
        print("LIST:")

        # Test the list endpoint.
        response = stub.List(accounts_pb2.ListAccountsRequest(page_size=1, page_token="1"))
        id_to_update = None
        for account in response.accounts:
            print(account)
            id_to_update = account.id

        print('-'*20)



if __name__ == '__main__':
    run()
