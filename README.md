Accounts service.

Manages the users that can login to this application.

app.py - main entrypoint.

test_client.py - used to verify app.py is working.

protos/ - the folder where all the compiled protos should exist.


#### NOTE: may have to change imports a bit.

In `protos/accounts_pb2_grpc.py`
```python
import accounts_pb2 as accounts__pb2

```
becomes:
```python
import protos.accounts_pb2 as accounts__pb2
```