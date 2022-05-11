import matplotlib.pyplot as plt
from bisect import bisect_left
import numpy as np 

class Statistics:
    def __init__(self, file_path=None, std=False) -> None:
        if file_path != None:
            file = open(file_path, 'r')
            self.std = std
            times_str = file.readlines()

            if not std:
                self.times = list(map(float, times_str))
            else:
                self.times = []

                for j in range(0,50000):
                    temp = []
                    for i in range(j,len(times_str),50000):
                        temp.append(float(times_str[i]))
                    self.times.append(temp)

                print(len(self.times))
                print(self.times[0])
                print(len(self.times[0]))
                
            
    def limit_five(self):
        total_time = 0
        total_primes = 0
        for time in self.times:
            
            if round(total_time) == 5:
                return total_primes
            
            total_primes += 1
            total_time += time

        return total_primes, total_time

    def take_closest(self, myList, myNumber):
        pos = bisect_left(myList, myNumber)
        if pos == 0:
            return myList[0], pos
        if pos == len(myList):
            return myList[-1], pos
        before = myList[pos - 1]
        after = myList[pos]
        if after - myNumber < myNumber - before:
            return after, pos
        else:
            return before, pos

    def return_xy(self):
        x_time = []
        y_count = []

        if not self.std:
            for i in range(len(self.times)):
                x_time.append(self.times[i])
                y_count.append(i+1)

            print(x_time[0], y_count[0])

        else:
            for i in range(len(self.times)):
                x_time.append(np.mean(self.times[i]) if i == 0 else x_time[i-1] + np.mean(self.times[i]))
                y_count.append(i+1)

        return x_time, y_count

    def plot_LUT_graph(self, title, file_name):
        
        x_time, y_count = self.return_xy()
        plt.plot(x_time, y_count)

        time, index = self.take_closest(x_time, 5)

        print(time, index)
        
        plt.plot(time, index, ls="", marker="o", label="points")
        plt.annotate(f"({round(time,6)}, {index})", (time, index), xytext=(time-1.5, index))
        
        plt.xlabel('Time (s)')
        plt.ylabel('Generated Keys')

        plt.title(title)

        #plt.savefig(file_name)

        plt.show()

    def plot_std_graph(self, title, file_name):
        x_time = []
        y_count = []
        error = []

        for i in range(len(self.times)):
            x_time.append(np.mean(self.times[i]))
            y_count.append(i+1)
            if i%2000 == 0:
                error.append(np.std(self.times[i]))
            else:
                error.append(0)
            #print(x_time[i], y_count[i], error[i])

        #plt.ylim(0,10)
        #plt.xlim(0,0.1)
        #plt.plot(x_time, y_count)
        plt.errorbar(x_time, y_count, xerr=error, fmt='-')


        time, index = self.take_closest(x_time, 5)

        print(time, index)
        print(x_time[index], y_count[index], error[index])
        print(self.times[index])
        
        plt.plot(time, index, ls="", marker="o", label="points")
        plt.annotate(f"({round(time,6)}, {index+1})", (time, index+1), horizontalalignment='left', verticalalignment='top')
        
        plt.xlabel('Time (s)')
        plt.ylabel('Generated Keys')

        plt.title(title)

        plt.savefig(file_name)

        plt.show()

    @staticmethod
    def plot_all(x1,y1,label1, x2,y2, label2, x3, y3, label3):
        plt.plot(x1,y1, label=label1)
        plt.plot(x2,y2, label=label2)
        plt.plot(x3,y3, label=label3)

        temp = Statistics()
        time, index = temp.take_closest(x1, 5)
        plt.plot(time, index, ls="", marker="o", label=label1)
        plt.annotate(f"({round(time,6)}, {index})", (time, index), horizontalalignment='left', verticalalignment='top')

        time, index = temp.take_closest(x2, 5)
        plt.plot(time, index, ls="", marker="o", label=label2)
        plt.annotate(f"({round(time,6)}, {index})", (time, index), xytext=(time+0.2, -10000), ha='center')

        time, index = temp.take_closest(x3, 5)
        plt.plot(time, index, ls="", marker="o", label=label3)
        plt.annotate(f"({round(time,6)}, {index})", (time, index), xytext=(time-0.2, index+10000), ha='center')

        plt.xlim(0,6)

        plt.xlabel('Time (s)')
        plt.ylabel('primes')

        plt.title("Comparisson all methods")

        plt.legend()

        plt.savefig("all_methods.png")

        plt.show()