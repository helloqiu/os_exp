# -*- coding: utf-8 -*-
from termcolor import colored


class CmdQueue(object):
    def __init__(self):
        self.queue = list((list(), list(), list()))

    def put(self, process):
        self.queue[process.priority].append(process)

    def remove(self, process_name):
        for i in self.queue:
            for j in i:
                if process_name == j.name:
                    i.remove(j)

    def get(self, name=None):
        if name:
            for i in self.queue:
                for j in i:
                    if name == j.name:
                        return j
            return None
        for i in self.queue:
            if len(i) > 0:
                return i[0]


class Process(object):
    def __init__(self, name, priority):
        self.priority = priority
        self.name = name
        self.resource = dict(r1=0, r2=0, r3=0, r4=0)
        self.ready = True
        self.resource_request = dict(r1=0, r2=0, r3=0, r4=0)

    def add_resource(self, k, v):
        self.resource[k] += v

    def reduce_resource(self, k, v):
        self.resource[k] -= v


SHELL_WORD = colored('shell>', 'green')
cmd_queue = CmdQueue()
current_process = None
resource = dict(r1=1, r2=2, r3=3, r4=4)


def parse_input(v):
    v_list = v.split(' ')
    while len(v_list) <= 2:
        v_list.append(' ')
    return tuple(v_list)


def chose_resource_process(r):
    for i in cmd_queue.queue:
        for j in i:
            if j.resource[r] > 0:
                i.remove(j)
                i.insert(0, j)


def process_exist(name):
    for i in cmd_queue.queue:
        for j in i:
            if name == j.name:
                return True
    return False


def destroy_process(process):
    global resource
    for k in process.resource.keys():
        resource[k] += process.resource[k]


def get_next():
    global resource
    while True:
        process = cmd_queue.get()
        ok = True
        if process.ready:
            return process
        else:
            for k in process.resource_request.keys():
                if resource[k] < process.resource_request[k]:
                    cmd_queue.remove(process.name)
                    cmd_queue.put(process)
                    ok = False
                    break
            if not ok:
                continue
            for k in process.resource_request.keys():
                resource[k] -= process.resource_request[k]
                process.resource_request[k] = 0
            process.ready = True
            return process


def handle_input(v):
    global current_process
    v = v.lower().strip()
    if v == 'exit':
        return None
    cmd, name, value = parse_input(v)
    if cmd == 'cr':
        if process_exist(name):
            return colored('There is already a process called "{}".'.format(name), 'red')
        try:
            value = int(value)
        except ValueError:
            return colored('Parameter {} is wrong'.format(value))
        cmd_queue.put(Process(name, 2 - value))
        # process_dict[name] = int(value)
        # resource_dict[name] = dict()
    elif cmd == 'de':
        if not process_exist(name):
            return colored('No process called "{}".'.format(name), 'red')
        p = cmd_queue.get(name)
        cmd_queue.remove(name)
        destroy_process(p)
        # for key in resource_dict[name].keys():
        #    resource[key] += resource_dict[name][key]
        # resource_dict.pop(name)
    elif cmd == 'req':
        try:
            value = int(value)
        except ValueError:
            return colored('Parameter {} is wrong'.format(value))
        if resource[name] < value:
            # chose_resource_process(name)
            cmd_queue.remove(current_process.name)
            cmd_queue.put(current_process)
            current_process.ready = False
            current_process.resource_request[name] += value
        else:
            # current_rd = resource_dict[current_process[1]]
            # if name in current_rd.keys():
            #    current_rd[name] += int(value)
            # else:
            #    current_rd[name] = int(value)
            current_process.add_resource(name, value)
            resource[name] -= value
    elif cmd == 'rel':
        try:
            value = int(value)
        except ValueError:
            return colored('Parameter {} is wrong'.format(value))
        if value > current_process.resource[name]:
            return colored(
                'Process "{}" has {} "{}" but try releasing {}'.format(
                    current_process.name,
                    current_process.resource[name],
                    name,
                    value
                ), 'red')
        current_process.reduce_resource(name, value)
        resource[name] += value
    elif cmd == 'to':
        cmd_queue.remove(current_process.name)
        cmd_queue.put(current_process)
    # current_process = cmd_queue.get()
    current_process = get_next()
    return colored(current_process.name, 'yellow')


if __name__ == '__main__':
    while True:
        print(SHELL_WORD)
        return_value = handle_input(input())
        if not return_value:
            break
        else:
            print(return_value)
