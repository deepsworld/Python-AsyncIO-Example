from multiprocessing import Process, Queue


def square_producer(inputqueue, resultqueue):
    """
    A producer that pops numbers off the inputqueue, squares them and puts the result on resultqueue
    """
    while True:
        num = inputqueue.get()
        if num is None:
            return

        resultqueue.put(num*num)
        print("Produced", num*num)


def consumer(resultqueue):
    """
    A consumer that pops results off the resultqueue and prints them to screen
    """
    while True:
        numsq = resultqueue.get()
        if numsq is None:
            return

        print("Consumed", numsq)


num_producers = 3

# Generate input
inputqueue = Queue()
for i in range(100):
    inputqueue.put(i % 10)
for _ in range(num_producers):
    inputqueue.put(None)  # Ensures that producers terminate

resultqueue = Queue()  # For transfer of data from producer to consumer

# Set up and start producer processes
producers = [Process(target=square_producer, args=(inputqueue, resultqueue)) for _ in range(num_producers)]
for p in producers:
    p.start()

# Set up and start consumer process
consumer = Process(target=consumer, args=(resultqueue,))
consumer.start()

# Wait for producers to finish
for p in producers:
    p.join()

# Wait for consumer to finish
resultqueue.put(None)
consumer.join()

print("All done")