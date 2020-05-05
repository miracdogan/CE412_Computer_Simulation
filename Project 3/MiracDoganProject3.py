import random
import simpy

CUSTOMERS = 1000000  # Total number of customers.
INTERVAL_CUSTOMERS = 60.0  # Generate new customers roughly every x seconds.
MIN_PATIENCE = 1  # Min. customer patience.
MAX_PATIENCE = 10000000  # Max. customer patience.


class TollBooth:  # Values for calculation.
    WAIT_IN_QUEUE = [0.0, 0]
    WAIT_IN_SYSTEM = 0.0
    Array = [0, 0, 0]


def source(env, number, interval, counter, lambda1, lambda2, lambda3):  # Calling env.process(Line=66)
    sortedLambdas = sorted([lambda1, lambda2, lambda3])  # 2, 3, 5      # Sort lambda values.
    lambda_x = 0.0

    for i in range(number):  # for loop will work number of customers.
        tollbooth = random.expovariate(12 / interval)  # Getting a value according to toll booth's mü.
        c = customer(env, ' Car %02d' % (i + 1), counter, tollbooth)
        env.process(c)

        if TollBooth.Array[0] < (CUSTOMERS / 2):  # Adjusting percentage of Road 1 --> %50
            lambda_x = sortedLambdas[2]
            TollBooth.Array[0] += 1  # Adding car to Road 1
        elif TollBooth.Array[1] < ((CUSTOMERS * 2) / 10):  # Adjusting percentage of Road 2 --> %20
            lambda_x = sortedLambdas[0]
            TollBooth.Array[1] += 1  # Adding car to Road 2
        elif TollBooth.Array[2] < ((CUSTOMERS * 3) / 10):  # Adjusting percentage of Road 3 --> %30
            lambda_x = sortedLambdas[1]
            TollBooth.Array[2] += 1  # Adding car to Road 3

        service_time = random.expovariate(lambda_x / interval)
        yield env.timeout(service_time)


def customer(env, name, counter, tollbooth):
    arrive = env.now  # Gets car's arrive time.
    print('%6.3f %s: Entering Toll Booth' % (arrive, name))  # Prints car's name and it's arrive time.

    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)

        wait = env.now - arrive  # Wait time.
        if wait != 0.0:
            TollBooth.WAIT_IN_QUEUE[0] += wait  # If someone's wait time is not equal to 0, code adds wait times.
            TollBooth.WAIT_IN_QUEUE[1] += 1  # If someone waits in the line, add 1 to counter.

        TollBooth.WAIT_IN_SYSTEM += tollbooth + wait  # Wait in system for each car equals to tool booth's time and wait

        if req in results:
            # We got to the counter
            print('%6.3f %s: Waiting Time         %6.3f' % (env.now, name, wait))  # Print current time, name and wait.
            yield env.timeout(tollbooth)
            print('%6.3f %s: Exiting Toll Booth' % (env.now, name))  # Print current tine and name.


env = simpy.Environment()
counter = simpy.Resource(env, capacity=1)
env.process(source(env, CUSTOMERS, INTERVAL_CUSTOMERS, counter, 5, 2, 3))
env.run()

print(" ")
print("---Results---")
print(" ")
print("Total Wait In System", TollBooth.WAIT_IN_SYSTEM)
print("Total Wait In Queue ", TollBooth.WAIT_IN_QUEUE)
print("Wait In System Average", TollBooth.WAIT_IN_SYSTEM / CUSTOMERS)
print("Wait In Queue Average", TollBooth.WAIT_IN_QUEUE[0] / TollBooth.WAIT_IN_QUEUE[1])

print(" ")
print("Road Percentages")
print("Road 1: ", TollBooth.Array[0] / sum(TollBooth.Array))
print("Road 2: ", TollBooth.Array[1] / sum(TollBooth.Array))
print("Road 3: ", TollBooth.Array[2] / sum(TollBooth.Array))
