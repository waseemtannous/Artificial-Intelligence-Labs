from random import shuffle, randint
import time


class MinimalConflicts:

    def run(self):
        startTime = time.time()
        bestNumConflicts = float('inf')
        repeat = 0
        found = False
        for _ in range(self.args.GA_MAXITER):
            iterTime = time.time()
            print(self.board)
            max_conflict, index = self.getMaxConflictState()
            temp = 0
            for i in range(len(self.board)):
                temp += self.getNumOfConflicts(i)

            currentConflicts = temp

            if bestNumConflicts == currentConflicts:
                repeat += 1
            elif currentConflicts < bestNumConflicts:
                bestNumConflicts = currentConflicts
                repeat = 1

            if max_conflict == 0 or repeat == self.args.LOCAL_STOP_ITER:
                print('Generation time: ', time.time() - iterTime)
                print()
                found = True
                print('found.')
                break

            self.getNewPlace(index, max_conflict)
            print('Generation time: ', time.time() - iterTime)
            print()
        print('Time elapsed: ', time.time() - startTime)
        if not found:
            print('reached local optimum.')

    def __init__(self, args):
        self.args = args
        self.board = [i for i in range(self.args.NQUEENS)]
        shuffle(self.board)

    def getMaxConflictState(self):  # returns the queen with highest conflicts
        num_conflict_arr = []
        max_conf = 0
        for i in range(0, len(self.board)):
            num_of_conflict = self.getNumOfConflicts(i)
            num_conflict_arr.append(num_of_conflict)
            if num_of_conflict > max_conf:
                max_conf = num_of_conflict

        max_conflict_queen = []
        sum = 0
        for i in range(len(num_conflict_arr)):
            if num_conflict_arr[i] == max_conf:
                sum += 1
                max_conflict_queen.append(i)
        random_Quenn = randint(0, sum - 1)
        return max_conf, max_conflict_queen[random_Quenn]

    def getNumOfConflicts(self, index): # returns the number of conflicts a queen makes
        count = 0
        for i in range(len(self.board)):
            if i == index:
                continue
            if self.board[i] == self.board[index]:
                count += 1
            elif abs(i - index) == abs(self.board[i] - self.board[index]):
                count += 1
        return count

    def getNewPlace(self, index, max_conflict): # returns the best place to put the queen
        min_conflict, save_new_index = max_conflict, index
        for i in range(len(self.board)):
            self.board[index] = i
            if self.getNumOfConflicts(index) <= min_conflict:
                min_conflict, save_new_index = self.getNumOfConflicts(index), i
        self.board[index] = save_new_index
