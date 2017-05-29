# -*- coding: utf-8 -*-
from queue import PriorityQueue
from heapq import heapify
from termcolor import colored


class CmdQueue(PriorityQueue):
    def _get(self):
        return self.queue[0]

    def remove(self, name):
        self.queue.remove(name)
        heapify(self.queue)  # So remove is now a O(len(self.queue)) op.


SHELL_WORD = colored('shell>', 'green')
cmd_queue = CmdQueue()
current_process = None
resource_dict = dict()
process_dict = dict()


def parse_input(v):
    v_list = v.split(' ')
    while len(v_list) <= 2:
        v_list.append(' ')
    return tuple(v_list)


def handle_input(v):
    global current_process
    v = v.lower().strip()
    if v == 'exit':
        return None
    cmd, name, value = parse_input(v)
    if cmd == 'cr':
        # Create process
        if name in process_dict.keys():
            return colored('There is already a process called "{}".'.format(name), 'red')
        try:
            value = int(value)
        except ValueError:
            return colored('Parameter {} is wrong'.format(value))
        cmd_queue.put((2 - int(value), name))
        process_dict[name] = int(value)
    elif cmd == 'de':
        if name not in process_dict.keys():
            return colored('No process called "{}".'.format(name), 'red')
        cmd_queue.remove((process_dict.pop(name), name))
    elif cmd == 'req':
        try:
            value = int(value)
        except ValueError:
            return colored('Parameter {} is wrong'.format(value))
        if name in resource_dict.keys():
            resource_dict[name] += int(value)
        else:
            resource_dict[name] = int(value)
    elif cmd == 'rel':
        if name not in resource_dict.keys():
            return colored('No resource called "{}".'.format(name), 'red')
        try:
            value = int(value)
        except ValueError:
            return colored('Parameter {} is wrong'.format(value))
        if value > resource_dict[name]:
            return colored(
                'Process "{}" has {} "{}" but try releasing {}'.format(
                    current_process[1],
                    resource_dict[name],
                    name,
                    value
                ), 'red')
        resource_dict[name] -= value
    elif cmd == 'to':
        cmd_queue.remove(current_process)
        process_dict.pop(current_process[1])
    if current_process != cmd_queue.get():
        resource_dict.clear()
        current_process = cmd_queue.get()
        return colored(current_process[1], 'yellow')


if __name__ == '__main__':
    while True:
        print(SHELL_WORD)
        return_value = handle_input(input())
        if not return_value:
            break
        else:
            print(return_value)
