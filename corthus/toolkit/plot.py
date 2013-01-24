
import sys
import matplotlib
import numpy as np

matplotlib.use('Agg')


def plot_flat(fun, rangex, rangey,
              path=[],
              path2=[],
              filename=None):
    import matplotlib.pyplot as plt

    print >> sys.stderr, 'Plotting...',
    sys.stderr.flush()

    size = max(rangex, rangey)/20 # in inches
    fig = plt.figure(figsize=(size, size), dpi=300)
    ax = fig.add_subplot(111)

    data = np.array([np.array([fun(x, y) for x in xrange(rangex)])
                     for y in xrange(rangey)])

    cax = ax.imshow(data, interpolation='nearest',
                    #cmap='gist_ncar'
                    vmin=0, vmax=200,
                    cmap='binary'
                    )
    fig.colorbar(cax)
    if path:
        X, Y, Q = zip(*path)
        ax.scatter(X, Y,
                   #s=np.multiply(Q, 3),
                   s=16,
                   marker='o',
                   lw = 1,
                   c=(0, 0, 0, 0))
    if path2:
        X, Y, Q = zip(*path2)
        ax.scatter(X, Y,
                   #s=np.multiply(Q, 3),
                   s=16,
                   marker='.',
                   lw = 0,
                   c=(0, 0, 0, 1))

    if filename:
        plt.savefig(filename, dpi=300)
        print >> sys.stderr, 'Wrote plot to %s.' % filename
    else:
        plt.show()


def plot_cost_matrix(cost, path=[], path2=[], plot_filename=None):
    plot_flat(lambda x, y: cost[x][y],
              len(cost), len(cost[0]),
              path=path,
              path2=path2,
              filename=plot_filename)

#    plot_flat(lambda x, y: similarity('a'*x, 'b'*y), 100, 100,
#              plot_filename='similarity.png')

