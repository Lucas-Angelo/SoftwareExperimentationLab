# Example of the Spearman's Rank Correlation Test https://machinelearningmastery.com/statistical-hypothesis-tests-in-python-cheat-sheet/
from scipy.stats import spearmanr
from scipy.stats import kendalltau
from scipy.stats import pearsonr

sig = 0.05
data1 = [100,59,98,103,130,70,109,88,76,123]
data2 = [205,188,130,98,100,174,207,198,172,209]
stat, p = spearmanr(data1, data2)
print('stat=%.3f, p=%.3f' % (stat, p))
if p > sig:
	print('Probably independent')
else:
	print('Probably dependent')

stat, p = kendalltau(data1, data2)
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably independent')
else:
	print('Probably dependent')

stat, p = pearsonr(data1, data2)
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably independent')
else:
	print('Probably dependent')