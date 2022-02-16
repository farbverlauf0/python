def latex_table(lst):
    begin = r'\begin{tabular}{' + '| c ' * len(lst[0]) + r'|}\hline '
    middle = ''.join(map(lambda row: ' & '.join(map(str, row)) + r'\\\hline ', lst))
    return begin + middle + r'\end{tabular}'
  
  
inp = [['cat', 12, 4], ['dog', 20, 8], ['human', 75, 32]]
outp = latex_table(inp)

with open('table.txt', 'w') as f:
    f.write(outp)
