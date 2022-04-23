import numpy as np
import random
import matplotlib.pyplot as plt

dists = [np.random.beta(1, 5, size=1000), np.random.chisquare(100, 1000), np.random.exponential(1, 1000), np.random.gamma(1, size=1000),
         np.random.geometric(0.1, 10000), np.random.laplace(size=1000), np.random.logistic(size=1000), np.random.lognormal(4, 6, 10000), 
         np.random.logseries(0.3, 1000000), np.random.normal(size=1000), np.random.pareto(1, 1000), np.random.poisson(size=1000),
         np.random.power(1.0, 1000), np.random.rayleigh(size=1000), np.random.standard_cauchy(1000), np.random.standard_exponential(1000),
         np.random.standard_gamma(0.5, 1000), np.random.standard_normal(1000), np.random.standard_t(3, 1000)]
titles = ['Beta', 'Chisquare', 'Exponential', 'Gamma', 'Geometric', 'Laplace', 'Logistic', 
          'Lognormal', 'Logseries', 'Normal', 'Pareto', 'Poisson', 'Power', 'Rayleigh',
          'Standard cauchy', 'Standard exp', 'Standard gamma', 'Standard normal', 'Standard']

i = 0
for dist in dists[4:5]:
    plt.style.use('seaborn')
    f,((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize = (6, 4.5))
    axs = [ax1, ax2, ax3, ax4]
    variables = dist
    variables.sort()
    x = variables
    y = np.arange(len(variables))/float(len(variables))
    for ax in axs:
        ax.plot(x, 1-y)
    f.suptitle(titles[i], fontsize='large')
    ax2.semilogx()
    ax3.semilogy()
    ax4.semilogx()
    ax4.semilogy()
    ax3.set_xlabel('Lin')
    ax4.set_xlabel('Log')
    ax1.set_ylabel('Lin')
    ax3.set_ylabel('Log')
    f.tight_layout()
    plt.show()
    i += 1