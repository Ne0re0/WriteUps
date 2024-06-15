import numpy as np
import random
from queue import Queue
from pwn import *


def find_path(maze_func,start,end):
    # BFS algorithm to find the shortest path
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = np.zeros_like(maze_func, dtype=bool)
    visited[start] = True
    queue = Queue()
    queue.put((start, []))
    while not queue.empty():
        (node, path) = queue.get()
        for dx, dy in directions:
            next_node = (node[0]+dx, node[1]+dy)
            if (next_node == end):
                return path + [next_node]
            if (next_node[0] >= 0 and next_node[1] >= 0 and 
                next_node[0] < maze_func.shape[0] and next_node[1] < maze_func.shape[1] and 
                maze_func[next_node] == 0 and not visited[next_node]):
                visited[next_node] = True
                queue.put((next_node, path + [next_node]))



if __name__ == '__main__' : 
    solved = 0
    p = remote("10.2.0.224",1234)
    output = p.recvuntil("il faut donc envoyer 'non'.".encode("utf-8"))
    print(output.decode())
    while True : 
        output = ""
        maze = []
        line_number = -1
        while True :

            output = p.recvline().decode()
            print(f'"{output[:-1]}"')

            if "═" in output or "║" in output or "╗" in output or "╚" in output or "╩" in output or "╦" in output or "╠" in output:
                line_number += 1
                maze.append([])
                for char in output : 
                    if char == " " : 
                        maze[line_number].append(0)
                    else :
                        maze[line_number].append(1)

                end_line = [1]*len(maze[0])
                end_line[-3] = 0
                if maze[line_number] == end_line :
                    maze_np = np.array(maze)
                    path = find_path(maze_np,(1,0),(len(maze)-1,len(maze[0])-3))
                    print(path)
                    if path != None : 
                        print("oui")
                        p.sendline("oui".encode("utf-8"))
                        
                    else :
                        print("non")
                        p.sendline("non".encode("utf-8"))
                    solved += 1
                    break
        print(solved)


    output = p.clean().decode()
    print(output)
