# -*- coding: utf-8 -*-

from terminal import CmdQueue


def test_get():
    q = CmdQueue()
    q.put((1, '4'))
    q.put((0, '1'))
    q.put((0, '2'))
    q.put((0, '3'))
    v = q.get()
    assert v[1] == '1'
    v = q.get()
    assert v[1] == '1'
    q.remove((0, '1'))
    v = q.get()
    assert v[1] == '2'
    q.remove((0, '2'))
    v = q.get()
    assert v[1] == '3'
    q.remove((0, '3'))
    v = q.get()
    assert v[1] == '4'
