import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st

file = open(f'{os.getcwd()}/trials.txt','r')
data = file.readline().split(',')
data = [int(x) for x in data]
data = np.array(data)

plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})

# Plot Histogram on x
x = data
bins = range(min(data),max(data))

plt.hist(x, bins = bins , density = True, log = True)
plt.gca().set(title='Roomba Results', ylabel='Frequency', xlabel = 'Steps')
plt.yscale('log')
# plt.show()

mean = np.mean(data)
std_dev = np.std(data)


#Terrible stepwise version of a confidence interval
def confidence(percent, data):
    low, high = 45,45
    prob = np.count_nonzero(data ==45)/len(data)
    while True:
        # print(prob)
        if prob > percent or high > 71:
            break
        low -= 1
        high += 1
        prob += (np.count_nonzero(data ==low) + np.count_nonzero(data ==high))/len(data)
    return (low,high,((prob*1000000)//1)/1000000)

print(f'Datapoints:{len(data)}\nMean:{mean}\nStandard Deviation:{std_dev}\n95% CI:{confidence(.95,data)}')