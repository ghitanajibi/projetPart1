##### Defining the class bond and its subclasses

import matplotlib.pyplot as plt



class Bond(object):
    def __init__(self, min_amount, min_term, rate):
        self.min_amount = min_amount
        self.min_term = min_term
        self.rate = rate

#calculating the investment

    def Inv(self, time):
        coeff = (1 + self.rate) ** time

        return coeff * self.min_amount

#defining sub classes

#short term
Short_term = Bond(1000, 2, 0.01)

#
# #long term

Long_term = Bond(3000, 5, 0.03)

# print(Short_term.Inv(10))

# running a loop to obtain the short term and long term investments over 100 years

time = []
ST_investment = []
LT_investment = []

for t in range(1, 101):
    time.append(t)
    ST_investment.append(Short_term.Inv(t))
    LT_investment.append(Long_term.Inv(t))
print([time, ST_investment, ST_investment])

# plotting the results

# Short term plot
plt.plot(time, ST_investment)
plt.xlabel('Time')
plt.ylabel('Investment')
plt.title('Investment Evolution for short term bonds')
plt.grid(True)
plt.show()

# Long term plot
plt.plot(time, LT_investment)
plt.xlabel('Time')
plt.ylabel('Investment')
plt.title('Investment Evolution for long term bonds')
plt.grid(True)
plt.show()
