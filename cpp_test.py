import heapq
import random
from collections import namedtuple
from typing import List

Item = namedtuple('Item', ['type', 'timeCreated', 'timeStart', 'duration', 'weight', 'minweight'])

class Container:
    def __init__(self):
        self.items = []
        self.currentWeight = 0
        self.maxWeight = 50

    def add_item(self, item: Item):
        self.items.append(item)
        self.currentWeight += item.weight

    def is_full(self) -> bool:
        return self.currentWeight >= self.maxWeight

    def is_empty(self) -> bool:
        return not self.items

    def remove_item(self) -> Item:
        item = self.items.pop()
        self.currentWeight -= item.weight
        return item

def add_items(pq: List[Item], time: int):
    numItems = random.randint(0, 10)

    for _ in range(numItems):
        type = random.randint(1, 3)
        duration = random.randint(1, 5)
        weight = random.randint(1, 20)
        minweight = random.randint(1, weight)

        item = Item(type, time, time, duration, weight, minweight)

        heapq.heappush(pq, (-item.type, -item.timeCreated, item))

def compression(container: Container):
    print("Container is full, compressing...")

    compressed = []
    uncompressed = []
    currentWeight = container.currentWeight

    while not container.is_empty():
        item = container.remove_item()
        heapq.heappush(compressed, (-item.type, -item.weight, item))
        heapq.heappush(uncompressed, (-item.type, -item.weight, item))

    while compressed:
        item = heapq.heappop(compressed)[-1]
        if currentWeight > container.maxWeight:
            currentWeight = currentWeight - item.weight + item.minweight
            item = item._replace(weight=item.minweight)
        container.add_item(item)

    if currentWeight > container.maxWeight:
        while not container.is_empty():
            container.remove_item()
        while uncompressed:
            item = heapq.heappop(uncompressed)[-1]
            container.add_item(item)

def execute(pq: List[Item], container: Container, timeStart: int):
    tempQueue = []

    while pq:
        item = heapq.heappop(pq)[-1]
        item = item._replace(timeStart=timeStart)
        container.add_item(item)

        if not container.is_full():
            compression(container)
            if not container.is_full():
                removedItem = container.remove_item()
                heapq.heappush(tempQueue, (-removedItem.type, -removedItem.timeCreated, removedItem))

    while tempQueue:
        heapq.heappush(pq, heapq.heappop(tempQueue))

def update_container(container: Container, completedContainer: Container, time: int):
    for i in reversed(range(len(container.items))):
        item = container.items[i]
        if item.timeStart + item.duration == time:
            container.currentWeight -= item.weight
            completedContainer.add_item(item)
            del container.items[i]

def main():
    pq = []
    container = Container()
    completedItems = Container()
    time = 1
    while time < 10:
        update_container(container, completedItems, time)
        add_items(pq, time)
        execute(pq, container, time)
        time += 1
    print("hi")

if __name__ == "__main__":
    main()
