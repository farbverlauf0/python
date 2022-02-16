def latex_table(lst):
    begin = r'\begin{tabular}{' + '| c ' * len(lst[0]) + r'|}\hline'
    middle = '\n'.join(map(lambda row: ' & '.join(map(str, row)) + r'\\ \hline ', lst))
    return begin + '\n' + middle + '\n' + r'\end{tabular}'


inp = [['cat', 12, 4], ['dog', 20, 8], ['human', 75, 32]]
outp = latex_table(inp)

with open('table.tex', 'a') as f:
    f.write('\\documentclass{article}\n\\usepackage[utf8]{inputenc}\\begin{document}\n')
    f.write(outp)
    f.write('\n\\end{document}')
