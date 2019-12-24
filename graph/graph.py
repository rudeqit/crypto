#!/usr/bin/env python3

# Take it from here: https://github.com/plutasnyy/Cycles-in-graphs

from random import randint
import copy
import time

class Graph:

    def __init__(self, number_of_vertices, density):
        '''
        minimum destinity -> n * (n-1) / 2 * d >= n - 1
        is equal to d >= 2/n
        '''        
        if density < 200 / number_of_vertices:
            density = 200 / number_of_vertices

        self.matrix = []
        self.number_of_vertices = int(number_of_vertices)

        self.create_full_graph()
        self.delete_edges(density)

        self.number_of_edges = self.count_edge()

    def find_non_empty_index(self):
        x, y = 0, 0
        x_counter, y_counter = 1, 1
        temp = self.number_of_vertices
        while (self.matrix[x][y] == 0 or x_counter <= 1 or y_counter <= 1):
            x, y = randint(1,temp), randint(1,temp)
            x_counter = self.matrix[x].count(1)
            y_counter = self.matrix[y].count(1)
        return x, y

    def delete_edges(self, density):
        full_count_edges = self.number_of_vertices * (self.number_of_vertices - 1) / 2
        for i in range(int(full_count_edges * (100 - density) / 100)):
            x, y = self.find_non_empty_index()
            self.matrix[x][y] = self.matrix[y][x] = 0
    
    def count_edge(self):
        temp = 0
        for i in self.matrix:
            temp += i.count(1)
        return temp / 2

    def create_full_graph(self):
        for i in range(0, self.number_of_vertices + 1):
            X = []
            for j in range(0, self.number_of_vertices + 1):
                if j * i == 0 or j == i:
                    X.append(0)
                else:
                    X.append(1)
            self.matrix.append(X)

    def print_neighbours_list(self):
        # print(self.matrix) 
        for i in range(1, self.number_of_vertices + 1):
            X = [x for x in range(len(self.matrix[i])) if self.matrix[i][x]]
            print(i, X)

    def delete_reverse_list(self, temp_list):
        for i in temp_list:
            if i[::-1] in temp_list:
                temp_list.remove(i[::-1])

    def print_list(self, temp_list):
        for i in temp_list:
            print(i)

    def find_hamilton_cycle(self, vertice, visited=[], one_path=False):
        if one_path == False or self.capture_hamilton == False:
            visited.append(vertice)
            if len(visited) == self.number_of_vertices:
                if self.matrix[visited[0]][visited[-1]] == 1:
                    visited.append(visited[0])
                    self.hamilton_cycle.append(copy.deepcopy(visited)) # list() copy the array, without it doesn`t work
                    self.capture_hamilton = True
            for i in range(1, self.number_of_vertices + 1):
                if self.matrix[vertice][i] == 1 and i not in visited:
                    self.find_hamilton_cycle(i,copy.deepcopy(visited), one_path)
            visited.pop()

    def hamilton(self, one_path=False):
        self.capture_hamilton = False
        self.hamilton_cycle = []

        self.find_hamilton_cycle(1, [], one_path)

        self.delete_reverse_list(self.hamilton_cycle)

        if len(self.hamilton_cycle) > 0:
            print("Hamilton cicle: ")
            self.print_list(self.hamilton_cycle)

        return self.hamilton_cycle

if __name__ == "__main__":
    graph = Graph(5, 70)
    graph.print_neighbours_list()

    start = time.time()
    graph.hamilton()
    print("hamilton", time.time() - start)
    