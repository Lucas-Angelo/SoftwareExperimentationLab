# Example of the Shapiro-Wilk Normality Test https://machinelearningmastery.com/statistical-hypothesis-tests-in-python-cheat-sheet/
from scipy.stats import shapiro
sig = 0.05
data = [100,59,98,103,130,70,109,88,76,123]
stat, p = shapiro(data)
print('stat=%.3f, p=%.3f' % (stat, p))
if p > sig:
	print('Probably Gaussian')
else:
	print('Probably not Gaussian')
data = [205,188,130,98,100,174,207,198,172,209]
stat, p = shapiro(data) 
print('stat=%.3f, p=%.3f' % (stat, p))
if p > sig:
	print('Probably Gaussian')
else:
	print('Probably not Gaussian')
