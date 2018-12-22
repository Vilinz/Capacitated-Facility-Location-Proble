import math
import random
import time

fp_anneal = open('1', 'w')
fp_tabu = open('2', 'w')


class CFLP:
    def __init__(self):
        self.facility_num = 0
        self.customer_num = 0
        self.capacity = []
        self.opening_cost = []
        self.demand = []
        self.assignment = []

        self.T = 120
        self.cooling_rate = 0.98
        self.repeat = 200

        self.total_demand = 0
        self.current_cost = 0
        self.current_state_of_customer = []
        self.current_capacity = []
        self.result_state = []

        self.new_state_of_customer = []
        self.new_capacity = []

        self.nei_state_of_customer = []
        self.nei_capacity = []
        self.tabu_list = []

    def read_data(self, file_name):
        print('Running dataset ' + file_name)
        with open('Instances/' + file_name) as f:
            self.facility_num, self.customer_num = f.readline().strip().split()
            self.facility_num = int(self.facility_num)
            self.customer_num = int(self.customer_num)
            demand_line = int(self.customer_num/10)
            for _ in range(self.facility_num):
                c, o = f.readline().strip().split()
                self.capacity.append(int(c))
                self.opening_cost.append(int(o))
            for _ in range(demand_line):
                temp = f.readline().strip().split(' ')
                for i in temp:
                    t = i.strip(' ')
                    if t == '':
                        continue
                    self.demand.append(int(float(t)))
            for _ in range(self.facility_num):
                temp1 = []
                for __ in range(int(self.customer_num/10)):
                    temp = f.readline().strip().split(' ')
                    for i in temp:
                        t = i.strip(' ')
                        if t == '':
                            continue
                        temp1.append(int(float(t)))
                self.assignment.append(temp1)
            # print(self.facility_num)
            # print(self.customer_num)
            # print("opening cost ", self.opening_cost)
            # print("capacity", self.capacity)
            # print("demand ", self.demand)
            # print("assignment ", self.assignment)
        f.close()

    def init_solution(self):
        for i in range(self.customer_num):
            self.current_state_of_customer.append(-1)
        for i in self.demand:
            self.total_demand += i
        self.current_capacity = self.capacity.copy()

        total_cost = 0
        temp = []
        while total_cost < self.total_demand:
            r = random.randint(0, self.facility_num - 1)
            if r not in temp:
                temp.append(r)
                total_cost += self.capacity[r]

        index = 0
        for i in range(self.customer_num):
            if self.current_capacity[temp[index]] - self.demand[i] >= 0:
                self.current_capacity[temp[index]] -= self.demand[i]
                self.current_state_of_customer[i] = temp[index]
            else:
                index += 1
                i -= 1
                # self.current_state_of_customer[i] = index
                # self.current_capacity[index] -= self.demand[i]
        self.current_cost = self.calculate_cost(self.current_state_of_customer)
        self.new_capacity = self.current_capacity.copy()
        self.new_state_of_customer = self.current_state_of_customer.copy()

    def calculate_cost(self, customer):
        cost = 0
        temp = []
        for i in range(self.customer_num):
            cost += self.assignment[customer[i]][i]
            if customer[i] not in temp:
                temp.append(customer[i])
        for i in temp:
            cost += self.opening_cost[i]
        return cost

    def gen_new_solution(self):
        tag = True
        self.new_capacity = self.current_capacity.copy()
        self.new_state_of_customer = self.current_state_of_customer.copy()
        while tag:
            ran_customer = random.randint(0, self.customer_num - 1)
            ran_facility = random.randint(0, self.facility_num - 1)
            # print("ran ", ran_facility, ran_customer)
            if self.new_capacity[ran_facility] >= self.demand[ran_customer]:
                tag = False
                self.new_capacity[ran_facility] -= self.demand[ran_customer]
                origin = self.new_state_of_customer[ran_customer]
                self.new_state_of_customer[ran_customer] = ran_facility
                if origin == -1:
                    break
                self.new_capacity[origin] += self.demand[ran_customer]
            else:
                continue

    def gen_nei_solution(self):
        tag = True
        self.nei_capacity = self.current_capacity.copy()
        self.nei_state_of_customer = self.current_state_of_customer.copy()
        ran_customer = 0
        origin = 0
        while tag:
            ran_customer = random.randint(0, self.customer_num - 1)
            ran_facility = random.randint(0, self.facility_num - 1)
            # print("ran ", ran_facility, ran_customer)
            if self.nei_capacity[ran_facility] >= self.demand[ran_customer]:
                tag = False
                self.nei_capacity[ran_facility] -= self.demand[ran_customer]
                origin = self.nei_state_of_customer[ran_customer]
                self.nei_state_of_customer[ran_customer] = ran_facility
                if origin == -1:
                    break
                self.nei_capacity[origin] += self.demand[ran_customer]
            else:
                continue
        return ran_customer, origin

    def simulated_annealing(self):
        global fp_anneal
        time_start = time.time()
        while self.T > 0.01:
            i = 0
            while i < self.repeat:
                i += 1
                self.gen_new_solution()
                self.current_cost = self.calculate_cost(self.current_state_of_customer)
                new_cost = self.calculate_cost(self.new_state_of_customer)
                if new_cost < self.current_cost:
                    self.current_capacity = self.new_capacity.copy()
                    self.current_state_of_customer = self.new_state_of_customer.copy()
                    # print("current cost ", new_cost)
                else:
                    num = math.exp((self.current_cost - new_cost) / self.T)
                    ran = random.random()
                    # print("num ", num)
                    # print("ran ", ran)
                    if num >= ran:
                        self.current_capacity = self.new_capacity.copy()
                        self.current_state_of_customer = self.new_state_of_customer.copy()
                        # print("current cost ", new_cost)
            self.T *= self.cooling_rate
        time_end = time.time()
        used_time = time_end - time_start
        fp_anneal.write('time ' + str(used_time) + '\n')
        fp_anneal.write('cost ' + str(self.current_cost) + '\n')
        temp = []
        result_state = []
        for i in range(self.customer_num):
            if self.current_state_of_customer[i] not in temp:
                temp.append(self.new_state_of_customer[i])
        temp.sort()
        for i in range(self.facility_num):
            result_state.append(0)
        for i in temp:
            result_state[i] = 1
        # print('cost ' + str(self.current_cost))
        # print(result_state)
        # print(self.current_state_of_customer)
        # print(self.current_capacity)
        fp_anneal.write('facility state ' + str(result_state) + '\n')
        fp_anneal.write('current state of customer ' + str(self.current_state_of_customer) + '\n\n')

    def tabu_search(self):
        global fp_tabu
        self.nei_state_of_customer = self.current_state_of_customer.copy()
        self.nei_capacity = self.current_capacity.copy()
        # print(self.current_state_of_customer)
        # print(self.nei_capacity)
        self.tabu_list = [[0 for i in range(self.customer_num)]for i in range(self.facility_num)]
        # print(tabu_list)
        repeat = 30000
        count = 0
        nei_count = int(self.customer_num/4)
        best_solution_customer = self.current_state_of_customer.copy()
        best_solution_capacity = self.current_capacity.copy()
        best_cost = self.calculate_cost(best_solution_customer)

        time_start = time.time()
        while count < repeat:
            count += 1
            i = nei_count
            self.gen_new_solution()
            new_cost = self.calculate_cost(self.new_state_of_customer)
            ran_customer = 0
            origin = 0
            while i > 1:
                i -= 1
                ran_customer, origin = self.gen_nei_solution()
                nei_cost = self.calculate_cost(self.nei_state_of_customer)
                # print("nei ", nei_cost)
                # print("new ", new_cost)
                if nei_cost < new_cost:
                    self.new_state_of_customer = self.nei_state_of_customer.copy()
                    self.new_capacity = self.nei_capacity.copy()
                    new_cost = nei_cost
            if new_cost < best_cost:
                # print("new ", new_cost)
                best_solution_customer = self.new_state_of_customer.copy()
                best_solution_capacity = self.new_capacity.copy()
                best_cost = new_cost
            if self.tabu_list[origin][ran_customer] < count:
                self.tabu_list[origin][ran_customer] = count + 20
                self.current_state_of_customer = self.new_state_of_customer.copy()
                self.current_capacity = self.new_capacity.copy()
        time_end = time.time()
        used_time = time_end - time_start
        temp = []
        result_state = []
        for i in range(self.customer_num):
            if best_solution_customer[i] not in temp:
                temp.append(best_solution_customer[i])
        temp.sort()
        for i in range(self.facility_num):
            result_state.append(0)
        for i in temp:
            result_state[i] = 1
        fp_tabu.write('time ' + str(used_time) + '\n')
        fp_tabu.write('cost ' + str(best_cost) + '\n')
        fp_tabu.write('facility state ' + str(result_state) + '\n')
        fp_tabu.write('customer state ' + str(best_solution_customer) + '\n\n')

        print(best_cost)
        print(result_state)
        print(best_solution_customer)
        print(best_solution_capacity)


def main():
    global fp_anneal
    global fp_tabu
    cflp = CFLP()
    data = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10',
            'p11', 'p12', 'p13', 'p14', 'p15', 'p16', 'p17', 'p18', 'p19', 'p20',
            'p21', 'p22', 'p23', 'p24', 'p25', 'p26', 'p27', 'p28', 'p29', 'p30',
            'p31', 'p32', 'p33', 'p34', 'p35', 'p36', 'p37', 'p38', 'p39', 'p40',
            'p41', 'p42', 'p43', 'p44', 'p45', 'p46', 'p47', 'p48', 'p49', 'p50',
            'p51', 'p52', 'p53', 'p54', 'p55', 'p56', 'p57', 'p58', 'p59', 'p60',
            'p61', 'p62', 'p63', 'p64', 'p65', 'p66', 'p67', 'p68', 'p69', 'p70', 'p71']

    # data = ['p2']

    print('run annealing-----a')
    print('run tabu----------t')
    command = input('$ ')
    if command == 'a':
        print('run all examples----------a')
        print('run single example--------s')
        command_in = input('$ ')
        if command_in == 'a':
            for i in data:
                print('annealing')
                fp_tabu.write(i + '\n')
                cflp = CFLP()
                cflp.read_data(i)
                cflp.init_solution()
                cflp.simulated_annealing()
        elif command_in == 's':
            name = input('file name\n$ ')
            cflp.read_data(name)
            cflp.init_solution()
            cflp.simulated_annealing()
        else:
            print('command error')
    elif command == 't':
        print('run all examples----------a')
        print('run single example--------s')
        command_in = input('$ ')
        if command_in == 'a':
            for i in data:
                print('tabu')
                fp_tabu.write(i + '\n')
                cflp = CFLP()
                cflp.read_data(i)
                cflp.init_solution()
                cflp.tabu_search()
        elif command_in == 's':
            name = input('file name\n$ ')
            cflp.read_data(name)
            cflp.init_solution()
            cflp.tabu_search()
        else:
            print('command error')
    else:
        print('command error')
    fp_tabu.close()
    fp_anneal.close()


if __name__ == '__main__':
    main()
