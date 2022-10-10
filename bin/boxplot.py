import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os



def main():
    # todo: load the "results.csv" file from the mia-results directory
    # todo: read the data into a list
    # todo: plot the Dice coefficients per label (i.e. white matter, gray matter, hippocampus, amygdala, thalamus)
    #  in a boxplot
    # alternative: instead of manually loading/reading the csv file you could also use the pandas package
    # but you will need to install it first ('pip install pandas') and import it to this file ('import pandas as pd')
    #pass  # pass is just a placeholder if there is no other code
    print(os.path.dirname(__file__))

    scriptDir = os.path.dirname(__file__)
    dir = os.path.join(scriptDir, './mia-result/2022-10-10-21-12-42/results.csv')

    dat = pd.read_csv(dir, sep=";")

    dat.boxplot(by = 'LABEL', column = ['DICE'], grid = False)
    plt.savefig(os.path.join(scriptDir, './mia-result/2022-10-10-21-12-42/boxplotD.png'), format = 'png')
    plt.show()
    dat.boxplot(by='LABEL', column=['HDRFDST'], grid=False)
    plt.savefig(os.path.join(scriptDir, './mia-result/2022-10-10-21-12-42/boxplotH.png'), format = 'png')
    plt.show()

if __name__ == '__main__':
    main()
