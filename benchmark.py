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


# results:
# array size: 0
# protobuf
# 907.28759765625ns/pack 843.5702323913574ns/unpack (33 bytes)
# json with dict
# 3,270.719051361084ns/pack 2,978.06978225708ns/unpack (82 bytes)
# json with tuple
# 2,778.627872467041ns/pack 2,378.230094909668ns/unpack (42 bytes)
# msgpack with dict
# 2,166.6789054870605ns/pack 497.3196983337403ns/unpack (60 bytes)
# msgpack with tuple
# 2,027.0705223083496ns/pack 296.12064361572266ns/unpack (32 bytes)
# array size: 10
# protobuf
# 1,429.3789863586426ns/pack 988.0113601684571ns/unpack (45 bytes)
# json with dict
# 4,387.631416320801ns/pack 3,850.617408752441ns/unpack (110 bytes)
# json with tuple
# 3,761.0697746276855ns/pack 3,166.840076446533ns/unpack (70 bytes)
# msgpack with dict
# 2,507.0595741271973ns/pack 622.3607063293457ns/unpack (70 bytes)
# msgpack with tuple
# 2,318.9902305603027ns/pack 384.6597671508789ns/unpack (42 bytes)
# array size: 100
# protobuf
# 4,182.839393615723ns/pack 1,831.190586090088ns/unpack (135 bytes)
# json with dict
# 12,705.35945892334ns/pack 11,313.188076019287ns/unpack (470 bytes)
# json with tuple
# 11,933.109760284424ns/pack 10,283.150672912598ns/unpack (430 bytes)
# msgpack with dict
# 4,882.488250732422ns/pack 1,341.2714004516602ns/unpack (162 bytes)
# msgpack with tuple
# 4,677.979946136475ns/pack 1,105.659008026123ns/unpack (134 bytes)
# array size: 1000
# protobuf
# 30,826.74741744995ns/pack 11,967.191696166992ns/unpack (1,908 bytes)
# json with dict
# 83,852.73933410645ns/pack 81,058.94804000854ns/unpack (4,970 bytes)
# json with tuple
# 83,297.77240753174ns/pack 81,444.72122192383ns/unpack (4,930 bytes)
# msgpack with dict
# 28,215.28911590576ns/pack 17,366.54043197632ns/unpack (2,678 bytes)
# msgpack with tuple
# 27,305.78899383545ns/pack 17,013.661861419678ns/unpack (2,650 bytes)