# -*- coding: utf-8 -*-

from terminal import CmdQueue, Process


def test_get():
    q = CmdQueue()
    q.put(Process('4', 1))
    q.put(Process('1', 0))
    q.put(Process('2', 0))
    q.put(Process('3', 0))
    v = q.get()
    assert v.name == '1'
    v = q.get()
    assert v.name == '1'
    q.remove('1')
    v = q.get()
    assert v.name == '2'
    q.remove('2')
    v = q.get()
    assert v.name == '3'
    q.remove('3')
    v = q.get()
    assert v.name == '4'
