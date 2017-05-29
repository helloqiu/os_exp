# -*- coding: utf-8 -*-

from terminal import Process


def test_process():
    p = Process('test', 1)
    assert p.name == 'test'
    assert p.priority == 1
    for k in p.resource:
        assert p.resource[k] == 0
    p.add_resource('r1', 1)
    assert p.resource['r1'] == 1
    p.reduce_resource('r1', 1)
    assert p.resource['r1'] == 0
