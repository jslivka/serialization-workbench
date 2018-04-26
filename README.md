# Serialization Tests

Serializers (requires python3)

* msgpack - https://msgpack.org/

* JSON - standard language-supported JSON serialization

* Protobuf - https://github.com/google/protobuf

## Run

Install protobuf:

`brew install protobuf`

Compile the python library for the 'Person' object (from the project root):

`protoc -I=. --python_out=. person.proto`

Install deps:

`pip3 install -r requirements.txt`

Run the benchmark:

`python3 benchmark.py`
