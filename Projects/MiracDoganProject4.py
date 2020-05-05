import simpy
import numpy as np

WAITING_TIME = []
WAIT_IN_QUEUE = [0, 0]

ARRIVAL_RATE = int(input('Arrival Rate λ :'))  # Getting input from user.
SERVICE_RATE = int(input('Service rate µ :'))   # # Getting input from user.
SYS_CAPACITY = int(input('System Capacity N :'))    # Getting input from user.
NUMBER_OF_CUSTOMER = int(input('Number of Customer :')) # Getting input from user.


class Global:
    IN_QUEUE = 0    # Created for access easily in def()'s
    DEPART_TIME = 0  # Created for access easily in def()'s
    ARRIVE_TIME = 0  # Created for access easily in def()'s
    a = []  # Created for access easily in def()'s
    #service = np.random.exponential(1 / SERVICE_RATE)
    #interArr = np.random.exponential(1 / ARRIVAL_RATE)


def interArrival(ARRIVAL_RATE):
    return np.random.exponential(1 / ARRIVAL_RATE)


def service(SERVICE_RATE):
    return np.random.exponential(1 / SERVICE_RATE)


def BANK(env, serve):
    for i in range(NUMBER_OF_CUSTOMER):  # Running code according to number of customer.
        yield env.timeout(interArrival(ARRIVAL_RATE))
        env.process(customer(env, i + 1, serve))


def customer(env, customer, serve):  # Customer send request to system.
    with serve.request() as request:

        if Global.IN_QUEUE >= SYS_CAPACITY:  # Checking the system capacity.
            Global.ARRIVE_TIME = env.now    # Get environment's time.
            print('%6.3f Customer %s: Came and Reneged' % (Global.ARRIVE_TIME, customer), '(',
                  'Number of Customer in Queue and Service'
                  , Global.IN_QUEUE, ')')   # Print Reneged customer's name.

        else:
            Global.ARRIVE_TIME = env.now    # Get environment's time.
            print('%6.3f Customer %s: Arrived' % (Global.ARRIVE_TIME, customer), '(',
                  'Number of Customer in Queue and Service'
                  , Global.IN_QUEUE, ')')  # Print arrived customer's name.
            Global.IN_QUEUE += 1    # Add 1 customer to Queue list.

            if Global.IN_QUEUE != 0:    # In this if block, we are getting total number of customer who used ATM.
                WAIT_IN_QUEUE[1] += 1
                Global.a = WAIT_IN_QUEUE[1]

            yield request
            print('%6.3f Customer %s: Served ' % (Global.ARRIVE_TIME, customer), '(',
                  'Number of Customer in Queue and Service'
                  , Global.IN_QUEUE, ')')   # Served Customer's name and details.
            serv_time = env.now
            WAIT_IN_QUEUE.append(serv_time - Global.ARRIVE_TIME)    # Getting time, in queue.

            yield env.timeout(service(SERVICE_RATE))
            print('%6.3f Customer %s: Departs' % (Global.ARRIVE_TIME, customer), '(',
                  'Number of Customer in Queue and Service'
                  , Global.IN_QUEUE, ')')

            Global.DEPART_TIME = env.now
            Global.IN_QUEUE -= 1
            WAITING_TIME.append(Global.DEPART_TIME - Global.ARRIVE_TIME)


env = simpy.Environment()   # Create Environment.
serve = simpy.Resource(env, capacity=1)
env.process(BANK(env, serve))
env.run()

print(" ")
print("---Results---")
print(" ")

print("Total Wait in System ", sum(WAITING_TIME))
print("Total Wait in Queue: ", sum(WAIT_IN_QUEUE))
print('Average Waiting Time In The System:', sum(WAITING_TIME) / len(WAITING_TIME))
print('Average Waiting Time In The Queue:', sum(WAIT_IN_QUEUE) / len(WAIT_IN_QUEUE))
print("Total Number of Customer: ", NUMBER_OF_CUSTOMER)
print("Total ATM User: ", Global.a)
print("Total Number of Customer Who Reneged from ATM: ", NUMBER_OF_CUSTOMER - Global.a)
print("Percentage of customers who cannot enter the ATM: ", (NUMBER_OF_CUSTOMER - Global.a) / Global.a, "%")
