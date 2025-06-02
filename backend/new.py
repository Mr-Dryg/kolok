import uuid
import sys
import os
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Graph generation functions
def create_graphik():
    exist = []
    x, y = 0, random.randint(0, 4)
    x_all, y_all = np.array([]), np.array([])
    checked_up = True
    checked_down = True
    choice = None
    while len(exist) != 4:
        if x > 5:
            return None, None
        if y == 0 or (y == 1 and x == 0):
            lst = [1, 2, 4]
            for item in exist:
                if item in lst:
                    lst.remove(item)
            if len(exist) != 0:
                if not checked_up:
                    if 2 in lst:
                        lst.remove(2)
                    if 4 in lst:
                        lst.remove(4)
                if 5 in exist and 4 in lst:
                    lst.remove(4)
            if len(lst) != 0:
                choice = random.choice(lst)
                if choice:
                    if choice == 2 or choice == 4:
                        checked_up = False
                        if not checked_down:
                            checked_down = True
                exist.append(choice)
            else:
                return None, None

        elif y == 1:
            lst = [1, 2, 3, 4]
            for item in exist:
                if item in lst:
                    lst.remove(item)
            if len(exist) != 0:
                if not checked_up:
                    if 2 in lst:
                        lst.remove(2)
                    if 4 in lst:
                        lst.remove(4)
                if 5 in exist and 4 in lst:
                    lst.remove(4)
                if not checked_down and 3 in lst:
                    lst.remove(3)
            if len(lst) != 0:
                choice = random.choice(lst)
                if choice:
                    if choice == 2 or choice == 4:
                        checked_up = False
                        if not checked_down:
                            checked_down = True
                    if choice == 3:
                        checked_down = False
                        if not checked_up:
                            checked_up = True
                exist.append(choice)
            else:
                return None, None

        elif y == 2:
            lst = [1, 2, 3, 4, 5]
            for item in exist:
                if item in lst:
                    lst.remove(item)
            if len(exist) != 0:
                if not checked_up:
                    if 2 in lst:
                        lst.remove(2)
                    if 4 in lst:
                        lst.remove(4)
                if 5 in exist and 4 in lst:
                    lst.remove(4)
                if not checked_down:
                    if 3 in lst:
                        lst.remove(3)
                    if 5 in lst:
                        lst.remove(5)
                if 4 in exist and 5 in lst:
                    lst.remove(5)
            if len(lst) != 0:
                choice = random.choice(lst)
                if choice:
                    if choice == 2 or choice == 4:
                        checked_up = False
                        if not checked_down:
                            checked_down = True
                    if choice == 3 or choice == 5:
                        checked_down = False
                        if not checked_up:
                            checked_up = True
                exist.append(choice)
            else:
                return None, None

        elif y == 3 and x != 0:
            lst = [1, 2, 3, 5]
            for item in exist:
                if item in lst:
                    lst.remove(item)
            if len(exist) != 0:
                if not checked_up and 2 in lst:
                    lst.remove(2)
                if not checked_down:
                    if 3 in lst:
                        lst.remove(3)
                    if 5 in lst:
                        lst.remove(5)
                if 4 in exist and 5 in lst:
                    lst.remove(5)
            if len(lst) != 0:
                choice = random.choice(lst)
                if choice:
                    if choice == 2:
                        checked_up = False
                        if not checked_down:
                            checked_down = True
                    if choice == 3 or choice == 5:
                        checked_down = False
                        if not checked_up:
                            checked_up = True
                exist.append(choice)
            else:
                return None, None

        elif y == 4 or (y == 3 and x == 0):
            lst = [1, 3, 5]
            for item in exist:
                if item in lst:
                    lst.remove(item)
            if len(exist) != 0:
                if not checked_down:
                    if 3 in lst:
                        lst.remove(3)
                    if 5 in lst:
                        lst.remove(5)
                if 4 in exist and 5 in lst:
                    lst.remove(5)
            if len(lst) != 0:
                choice = random.choice(lst)
                if choice:
                    if choice == 3 or choice == 5:
                        checked_down = False
                        if not checked_up:
                            checked_up = True
                exist.append(choice)
            else:
                return None, None

        if len(exist) == 1:
            x_all = np.append(x_all, 0.00)
            y_all = np.append(y_all, round(float(y), 2))
        if choice == 1:
            x1, y1, x, y = create_region1(x, y)
            x_all = np.concatenate((x_all, x1))
            y_all = np.concatenate((y_all, y1))
        elif choice == 2:
            x2, y2, x, y = create_region2(x, y)
            x_all = np.concatenate((x_all, x2))
            y_all = np.concatenate((y_all, y2))
        elif choice == 3:
            x3, y3, x, y = create_region3(x, y)
            x_all = np.concatenate((x_all, x3))
            y_all = np.concatenate((y_all, y3))
        elif choice == 4:
            x4, y4, x, y = create_region4(x, y)
            x_all = np.concatenate((x_all, x4))
            y_all = np.concatenate((y_all, y4))
        elif choice == 5:
            x5, y5, x, y = create_region5(x, y)
            x_all = np.concatenate((x_all, x5))
            y_all = np.concatenate((y_all, y5))
    sorted_indices = np.argsort(x_all)
    x_sorted = x_all[sorted_indices]
    y_sorted = y_all[sorted_indices]
    return x_sorted, y_sorted

def create_region1(start_x, start_y):
    delay = 0.01
    const_value = start_y
    end_x = np.arange(start_x + delay, start_x + 1 + delay, delay)
    end_y = np.full_like(end_x, const_value)
    x, y = start_x + 1, start_y
    return end_x, end_y, x, y

def create_region2(start_x, start_y):
    delay = 0.01
    end_x = np.arange(start_x + delay, start_x + 1 + delay, delay)
    end_y = np.arange(start_y + delay, start_y + 1 + delay, delay)
    x, y = start_x + 1, start_y + 1
    return end_x, end_y, x, y

def create_region3(start_x, start_y):
    delay = 0.01
    end_x = np.arange(start_x + delay, start_x + 1 + delay, delay)
    end_y = -end_x + (start_y + start_x)
    x, y = start_x + 1, start_y - 1
    return end_x, end_y, x, y

def create_region4(start_x, start_y):
    delay = 0.01
    end_x = np.arange(start_x + delay, start_x + 2 + delay, delay)
    end_y = np.arange(start_y + delay, start_y + 2 + delay, delay)
    x, y = start_x + 2, start_y + 2
    return end_x, end_y, x, y

def create_region5(start_x, start_y):
    delay = 0.01
    end_x = np.arange(start_x + delay, start_x + 2 + delay, delay)
    end_y = -end_x + (start_y + start_x)
    x, y = start_x + 2, start_y - 2
    return end_x, end_y, x, y

def determine_directions(y_list):
    directions = ["stand"] * len(y_list)
    for i in range(1, len(y_list)):
        if y_list[i] in {0.0, 1.0, 2.0, 3.0, 4.0}:
            directions[i] = "stand"
        elif y_list[i] > y_list[i - 1]:
            directions[i] = "up"
        elif y_list[i] < y_list[i - 1]:
            directions[i] = "down"
    return directions

def find_blocks(x_list, y_list, directions):
    blocks = []
    types = []
    direction = None
    for i, x in enumerate(x_list):
        if y_list.count(y_list[i]) == 3:
            current_direction = directions[i]
            if current_direction != direction:
                direction = current_direction
                blocks.append([x])
                types.append(direction)
            elif direction in ["up", "down"]:
                blocks[-1].append(x)
    return blocks, types


class Task:
    def __init__(self):
        self.time_start = datetime.now()
        self.id = str(uuid.uuid4())
        self.x_values, self.y_values = self.generate_graph()
        # print(self.x_values, self.y_values)
        self.x_list = np.round(self.x_values, 2).tolist()
        self.y_list = np.round(self.y_values, 2).tolist()
        self.correct_2 = None
        self.correct_3 = None
        self.correct_more = None
        self.y_2 = None
        self.start_x_3 = None
        self.end_x_3 = None
        self.prepare_conditions()
        self.path = None

    def get_correct_ans_1(self):
        x0 = self.y_2
        y0 = None
        for i in range(len(self.x_list)):
            if self.x_list[i] == x0:
                y0 = self.y_list[i]
                break
        left = None
        dots = set()
        res = ''
        for i in range(len(self.x_list) - 1):
            if self.y_list[i] == y0:
                if self.y_list[i] == self.y_list[i + 1] and left is None:
                    left = self.x_list[i]
                elif self.y_list[i] != self.y_list[i + 1]:
                    if left is None:
                        dots.add(self.x_list[i])
                    else:
                        res += f'[{int(left)};{int(self.x_list[i])}]U'
                        left = None
        if self.y_list[-1] == y0:
            if left is None:
                dots.add(self.x_list[-1])
            else:
                res += f'[{int(left)};{int(self.x_list[-1])}]U'
        res += '{' + ';'.join(sorted(map(lambda x: str(int(x)), dots))) + '}'
        if res[-1] == 'U':
            res = res[:-1]
        return res

    def generate_graph(self):
        while True:
            x_values, y_values = create_graphik()
            if x_values is not None and y_values is not None:
                return x_values, y_values

    def get_graph_data(self):
        return self.x_list, self.y_list
    
    def draw_graph(self):
        plt.plot(self.x_list, self.y_list, label="f(x)")
        plt.grid(True)
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.xlim([0, 5.2])
        plt.ylim([0, 4.2])
        plt.xticks(np.arange(0, 6, 1))
        plt.yticks(np.arange(0, 5, 1))
        self.path = os.path.join(os.path.dirname(__file__), 'img', f"{self.id}.png")
        plt.savefig(self.path)
        plt.clf()

    def prepare_conditions(self):
        # 2 intersections
        i_2 = [i for i in range(len(self.x_list)) if self.y_list.count(self.y_list[i]) == 2]
        pos = random.choice(i_2)
        self.y_2 = self.y_list[pos]
        self.x_2 = self.x_list[pos]  
        self.correct_2 = sorted([self.x_list[i] for i in i_2 if self.y_list[i] == self.y_2])

        # 3 intersections
        directions = determine_directions(self.y_list)
        blocks, types = find_blocks(self.x_list, self.y_list, directions)
        lst_blocks = [i for i in range(len(blocks)) if len(blocks[i]) == 99]
        if lst_blocks:
            num = random.choice(lst_blocks)
            self.start_x_3 = int(blocks[num][0])
            self.end_x_3 = self.start_x_3 + 1
            check = random.choice(blocks[num])
            check_y = next((self.y_list[i] for i in range(len(self.x_list)) if self.x_list[i] == check), None)
            self.correct_3 = sorted([x for x in self.x_list if self.y_list[self.x_list.index(x)] == check_y])
        else:
            self.correct_3 = []

        # More than 3 intersections
        triple_x = sorted([self.x_list[i] for i in range(len(self.x_list)) if self.y_list.count(self.y_list[i]) > 3])
        if len(triple_x) == 101:
            start_x = int(triple_x[0])
            end_x = start_x + 1
            self.correct_more = f"[{start_x};{end_x}]"
            self.answer_more = f"{round(start_x + (end_x - start_x) / 2, 2)}"
        elif len(triple_x) == 102:
            if triple_x[0] + 0.01 == triple_x[1]:
                start_x = int(triple_x[0])
                oneMoreX = "{" + str(int(triple_x[-1])) + "}"
            elif triple_x[-2] + 0.01 == triple_x[-1]:
                start_x = int(triple_x[1])
                oneMoreX = "{" + str(int(triple_x[0])) + "}"
            end_x = start_x + 1
            self.correct_more = f"[{start_x};{end_x}] U {oneMoreX}"
            self.answer_more = f"{round(start_x + (end_x - start_x) / 2, 2)}"

        else:
            self.correct_more = ""
            self.answer_more = ""

    def get_question_data(self):
        # print(self.correct_more)
        return self.x_2, self.start_x_3, self.end_x_3, self.answer_more

    def check_answers(self, user_2, user_3, user_more):
        # print('cor 1:', self.get_correct_ans_1())
        # print('cor 2:', self.correct_3)
        # print('cor 3:', self.correct_more)

        self.time_finish = datetime.now()
        self.time_solving = self.time_finish - self.time_start
        result_2 = set(user_2.split('U')) == set(self.get_correct_ans_1().split('U'))

        user_3 = user_3.strip('{').strip('}').split(";")
        result_3 = len(self.correct_3) == 0 or (len(user_3) == 3 and set([round(eval(expr, {"x": self.correct_3[0]}), 2) for expr in user_3]) == set(self.correct_3))
        
        result_more = set(user_more.replace(' ', '').split('U')) == set(self.correct_more.replace(' ', '').split('U'))
        return result_2, result_3, result_more
