# -*- coding: utf-8 -*-


# Python packages
import matplotlib.pyplot
import numpy
import os


# MRG packages
import _env


def myimshow(tab, **kwargs):
    """Customized plot."""

    if 'dpi' in kwargs and kwargs['dpi']:
        dpi = kwargs['dpi']
    else:
        dpi = 100

    # -- create figure
    fig = matplotlib.pyplot.figure(dpi=dpi)
    ax = matplotlib.pyplot.axes()

    if 'title' in kwargs and kwargs['title']:
        title = kwargs['title']
    if 'cmap' in kwargs and kwargs['cmap']:
        cmap = kwargs['cmap']
    else:
        cmap = 'jet'
    #if 'clim' in kwargs and kwargs['clim']:
    #    clim = kwargs['clim']
    if 'vmin' in kwargs and kwargs['vmin']:
        vmin = kwargs['vmin']
    if 'vmax' in kwargs and kwargs['vmax']:
        vmax = kwargs['vmax']

    # -- plot curves
    if 'cmap' in kwargs and kwargs['cmap']:
        matplotlib.pyplot.imshow(tab, cmap=cmap)
    else:
        matplotlib.pyplot.imshow(tab, cmap=cmap)
    if 'title' in kwargs and kwargs['title']:
        matplotlib.pyplot.title(title)
    else:
        matplotlib.pyplot.imshow(tab, cmap=cmap)
    if 'colorbar' in kwargs and kwargs['colorbar']:
        matplotlib.pyplot.colorbar()

#    if 'clim' in kwargs and kwargs['clim']:
#        matplotlib.pyplot.clim(clim)
    if 'vmin' in kwargs and kwargs['vmin']:
        matplotlib.pyplot.clim(vmin, vmax)

    if 'filename' in kwargs and kwargs['filename']:
        output_file = kwargs['filename']
        (root, ext) = os.path.splitext(output_file)
        matplotlib.pyplot.savefig(root + '_plot' + ext, format=ext[1:])
        matplotlib.pyplot.close()
    else:
        matplotlib.pyplot.show()
        matplotlib.pyplot.close()

    matplotlib.pyplot.close(fig)

    return


def _plot_uncontroled_solution(u, chi):
#def _plot_uncontroled_solution(x_plot, y_plot, x, y, u, chi):

    myimshow(numpy.real(u), title='$\operatorname{Re}(u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_u0_re.jpg')
    myimshow(numpy.imag(u), title='$\operatorname{Im}(u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_u0_im.jpg')
    myimshow(chi, title='$\chi_{0}$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_chi0_re.jpg')
    # k_begin = 0
    # k_end = len(x) - 1
    # for k in range(k_begin, k_end):
    #     x_plot[k] = k
    #     y_plot[k] = chi[int(y[k]), int(x[k])]
    # matplotlib.pyplot.plot(x_plot, y_plot)
    # matplotlib.pyplot.title('$\chi_{0}$ in $\Omega$')
    # matplotlib.pyplot.show()

    return


def _plot_controled_solution(u, chi):
#def _plot_controled_solution(x_plot, y_plot, x, y, u, chi):

    myimshow(numpy.real(u), title='$\operatorname{Re}(u_{n})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_un_re.jpg')
    myimshow(numpy.imag(u), title='$\operatorname{Im}(u_{n})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_un_im.jpg')
    myimshow(chi, title='$\chi_{n}$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_chin_re.jpg')
    # k_begin = 0
    # k_end = len(x) - 1
    # for k in range(k_begin, k_end):
    #     x_plot[k] = k
    #     y_plot[k] = chi[int(y[k]), int(x[k])]
    # matplotlib.pyplot.plot(x_plot, y_plot)
    # matplotlib.pyplot.title('$\chi_{n}$ in $\Omega$')
    # matplotlib.pyplot.show()

    return


def _plot_error(err):

    myimshow(numpy.real(err), title='$\operatorname{Re}(u_{n}-u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin = -1, vmax = 1, filename='fig_err_real.jpg')
    myimshow(numpy.imag(err), title='$\operatorname{Im}(u_{n}-u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin = -1, vmax = 1, filename='fig_err.jpg')

    return

def _plot_energy_history(energy):

    matplotlib.pyplot.plot(energy) #, cmap = 'jet')#, vmin = 1e-4, vmax = 1e-0)
    matplotlib.pyplot.title('Energy')
    #matplotlib.pyplot.colorbar()
    #matplotlib.pyplot.show()
    filename = 'fig_energy_real.jpg'
    matplotlib.pyplot.savefig(filename)
    matplotlib.pyplot.close()

    return

# we can now plot domains
def plot_domain(domain, title='Domain', filename='fig_domain.jpg'):
    """
    NODE_INTERIOR = -1  # nodes located in the interior
    NODE_COMPLEMENTARY = -2  # nodes located in the complement of (interior + frontier)
    NODE_DIRICHLET = 1  # nodes with dirichlet boundary condition
    NODE_NEUMANN = 2  # nodes with neumann boundary condition
    NODE_ROBIN = 3  # nodes with robin boundary condition
    """

    domain_array = numpy.array(domain)

    interior_nodes = numpy.argwhere(domain_array==_env.NODE_INTERIOR)
    complementary_nodes = numpy.argwhere(domain_array==_env.NODE_COMPLEMENTARY)
    dirichlet_nodes = numpy.argwhere(domain_array==_env.NODE_DIRICHLET)
    neumann_nodes = numpy.argwhere(domain_array==_env.NODE_NEUMANN)
    robin_nodes = numpy.argwhere(domain_array==_env.NODE_ROBIN)

    interior_col = [254,254,254] # white
    complementary_col = [145,1,254] # purple
    dirichlet_col = [1,237,254] # light blue
    neumann_col = [254,17,1] # red
    robin_col = [110,254,1] # green

    domain_col = numpy.zeros((*domain_array.shape, 3), dtype=numpy.int64)

    domain_col[interior_nodes[:,0], interior_nodes[:,1], :] = interior_col
    domain_col[complementary_nodes[:,0], complementary_nodes[:,1], :] = complementary_col
    domain_col[dirichlet_nodes[:,0], dirichlet_nodes[:,1], :] = dirichlet_col
    domain_col[neumann_nodes[:,0], neumann_nodes[:,1], :] = neumann_col
    domain_col[robin_nodes[:,0], robin_nodes[:,1], :] = robin_col

    matplotlib.pyplot.imshow(domain_col)
    matplotlib.pyplot.title(title)
    filename = filename
    matplotlib.pyplot.savefig(filename)
    matplotlib.pyplot.close()