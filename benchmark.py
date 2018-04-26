# -*- coding: utf-8 -*-
import time

import msgpack

import json

from person_pb2 import Person

TIMES = 100000

# specific to protobuf
def make_person(size):
    p = Person()
    p.id = 1
    p.name = 'Heungsub Lee'
    p.email = 'sub@nexon.co.kr'
    for x in range(size):
        p.lucky_numbers.append(x)
    return p


def make_dict(size):
    return {'id': 1, 'name': 'Heungsub Lee', 'email': 'sub@nexon.co.kr',
            'lucky_numbers': list(range(size))}


def make_tuple(size):
    return (1, 'Heungsub Lee', 'sub@nexon.co.kr', list(range(size)))


def protobuf_pack(times, size):
    p = make_person(size)
    t = time.time()
    for x in range(times):
        p.SerializeToString()
    return time.time() - t, len(p.SerializeToString())


def protobuf_unpack(times, size):
    s = make_person(size).SerializeToString()
    p = Person()
    t = time.time()
    for x in range(times):
        p.ParseFromString(s)
    return time.time() - t


def json_pack(times, size, make=make_dict):
    d = make(size)
    t = time.time()
    for x in range(times):
        json.dumps(d)
    return time.time() - t, len(json.dumps(d))

def json_unpack(times, size, make=make_dict):
    b = json.dumps(make(size))
    t = time.time()
    for x in range(times):
        json.loads(b)
    return time.time() - t


def msgpack_pack(times, size, make=make_dict):
    d = make(size)
    t = time.time()
    for x in range(times):
        msgpack.packb(d)
    return time.time() - t, len(msgpack.packb(d))


def msgpack_unpack(times, size, make=make_dict):
    b = msgpack.packb(make(size))
    t = time.time()
    for x in range(times):
        msgpack.unpackb(b)
    return time.time() - t


if __name__ == '__main__':
    fmt = '{0:,}ns/pack {1:,}ns/unpack ({2:,} bytes)'
    ns = lambda d: d / TIMES * 10 ** 9
    for size in [0, 10, 100, 1000]:
        print('array size: {0}'.format(size))

        pack_duration, length = protobuf_pack(TIMES, size)
        unpack_duration = protobuf_unpack(TIMES, size)
        print('protobuf'),
        print(fmt.format(ns(pack_duration), ns(unpack_duration), length))

        pack_duration, length = json_pack(TIMES, size)
        unpack_duration = json_unpack(TIMES, size)
        print('json with dict'),
        print(fmt.format(ns(pack_duration), ns(unpack_duration), length))

        pack_duration, length = json_pack(TIMES, size, make=make_tuple)
        unpack_duration = json_unpack(TIMES, size, make=make_tuple)
        print('json with tuple'),
        print(fmt.format(ns(pack_duration), ns(unpack_duration), length))

        pack_duration, length = msgpack_pack(TIMES, size)
        unpack_duration = msgpack_unpack(TIMES, size)
        print('msgpack with dict'),
        print(fmt.format(ns(pack_duration), ns(unpack_duration), length))

        pack_duration, length = msgpack_pack(TIMES, size, make=make_tuple)
        unpack_duration = msgpack_unpack(TIMES, size, make=make_tuple)
        print('msgpack with tuple'),
        print(fmt.format(ns(pack_duration), ns(unpack_duration), length))
