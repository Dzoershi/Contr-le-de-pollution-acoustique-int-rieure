# -*- coding: utf-8 -*-


# Python packages
import matplotlib.pyplot
import numpy
import os


# MRG packages
import _env
import preprocessing
import processing
import postprocessing
#import solutions

### Constant for gradient descent 


EPSILON1 = 5*10**(-2)
EPSILON2 = 10**(-2)

def reLinearProj(chi, l):
    (M,N) = numpy.shape(chi) 
    for i in range(M):
        for j in range(N):
            chi[i, j] = max(0, min(chi[i, j] + l, 1))
    return chi

# Attention :  j'ai enlevé omega (la fréquence) dans les paramètres (pour le moment je ne vois pas en quoi cela influe sur notre methode d'optimisation)
def your_optimization_procedure(domain_omega, spacestep, f, f_dir, f_neu, f_rob,
                           beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                           Alpha, mu, chi, V_obj):
    """This function return the optimized density.

    Parameter:
        cf solvehelmholtz's remarks
        Alpha: complex, it corresponds to the absorbtion coefficient;
        mu: float, it is the initial step of the gradient's descent;
        V_obj: float, it characterizes the volume constraint on the density chi.
    """

    k = 0
    (M, N) = numpy.shape(domain_omega)
    numb_iter = 100
    energy = numpy.zeros((numb_iter+1, 1), dtype=numpy.float64)
    while k < numb_iter and mu > 10**(-5):
        print('---- iteration number = ', k)
        print('1. computing solution of Helmholtz problem, i.e., u')
        ######  On update les conditions aux bord de Robin (puisque l'on a changé chi)
        alpha_rob = Alpha * chi
        u = processing.solve_helmholtz(domain_omega, spacestep, wavenumber, f, f_dir, f_neu, f_rob,
                        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob)
        print('2. computing solution of adjoint problem, i.e., p')
        ######  On souhaite résoudre le problème 
        f_adj = -2*u.conj()
        f_adj_dir = numpy.zeros((M, N), dtype=numpy.complex128)
        p = processing.solve_helmholtz(domain_omega, spacestep, wavenumber, f_adj, f_adj_dir, f_neu, f_rob,     # résolution de l'edp adjointe
                        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob)
        print('3. computing objective function, i.e., energy')
        ene = compute_objective_function(domain_omega, u, spacestep)                                            # Calcul de l'energie pour u 
        energy[k] = ene
        print('4. computing parametric gradient')
        grad = -numpy.real(Alpha*u*p)      
        # print("Valeur du gradient : ", grad[49])
        while ene >= energy[k] and mu > 10 ** -5:
            print('    a. computing gradient descent')
            new_chi = chi - mu*grad
            print('    b. computing projected gradient')
            l = 0
            new_chi_proj = reLinearProj(new_chi, l)
            ### We aim to keep a constant volume proportion V_obj
            V_chi = numpy.sum(numpy.sum(new_chi_proj)) / S     
            while abs(V_chi - V_obj) > EPSILON1:
                if V_chi > V_obj:
                    l -= EPSILON2 
                else:
                    l += EPSILON2
                new_chi_proj = reLinearProj(chi, l)
                V_chi = numpy.sum(numpy.sum(new_chi_proj)) / S     
            print('    c. computing solution of Helmholtz problem, i.e., u')
            alpha_rob = Alpha * new_chi_proj 
            u = processing.solve_helmholtz(domain_omega, spacestep, wavenumber, f, f_dir, f_neu, f_rob,
                        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob)
            print('    d. computing objective function, i.e., energy (E)')
            ene = compute_objective_function(domain_omega, u, spacestep)
            print("energie: ",ene)
            if ene <  energy[k]:
                # The step is increased if the energy decreased
                mu = mu * 1.1
                chi = new_chi_proj
            else:
                # The step is decreased is the energy increased
                mu = mu / 2
        k += 1
    print('end. computing solution of Helmholtz problem, i.e., u')
    return chi, energy, u, grad


def compute_objective_function(domain_omega, u, spacestep):
    """
    This function compute the objective function:
    J(u,domain_omega)= \int_{domain_omega}||u||^2 

    Parameter:
        domain_omega: Matrix (NxP), it defines the domain and the shape of the
        Robin frontier;
        u: Matrix (NxP), it is the solution of the Helmholtz problem, we are
        computing its energy;
        spacestep: float, it corresponds to the step used to solve the Helmholtz
        equation.
    """
    # every element has the same size : spacestep^2
    # coordinates_to_mask = numpy.argwhere(domain_omega != _env.NODE_INTERIOR)
    # u = numpy.array(u, copy=True)
    # mask = numpy.zeros(u.shape, dtype=bool)
    # mask[coordinates_to_mask[:,0], coordinates_to_mask[:,1]] = True
    # u_masked = numpy.ma.array(data=u, mask=coordinates_to_mask)
    # u_line = numpy.reshape(u_masked, -1)
    # energy = numpy.sum(numpy.absolute(u_line)**2) * (spacestep**2)
    u_line = numpy.reshape(u, -1)
    energy = numpy.sum(numpy.absolute(u_line)**2) * (spacestep**2)
    return energy


if __name__ == '__main__':


    # ----------------------------------------------------------------------
    # -- Fell free to modify the function call in this cell.
    # ----------------------------------------------------------------------
    # -- set parameters of the geometry
    N = 50  # number of points along x-axis
    M = 2 * N  # number of points along y-axis
    level = 0 # level of the fractal
    spacestep = 1.0 / N  # mesh size

    # -- set parameters of the partial differential equation
    kx = -1.0
    ky = -1.0
    wavenumber = numpy.sqrt(kx**2 + ky**2)  # wavenumber
    wavenumber = 10.0

    # ----------------------------------------------------------------------
    # -- Do not modify this cell, these are the values that you will be assessed against.
    # ----------------------------------------------------------------------
    # --- set coefficients of the partial differential equation
    beta_pde, alpha_pde, alpha_dir, beta_neu, alpha_rob, beta_rob = preprocessing._set_coefficients_of_pde(M, N)

    # -- set right hand sides of the partial differential equation
    f, f_dir, f_neu, f_rob = preprocessing._set_rhs_of_pde(M, N)

    # -- set geometry of domain
    domain_omega, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level)

    # ----------------------------------------------------------------------
    # -- Fell free to modify the function call in this cell.
    # ----------------------------------------------------------------------
    # -- define boundary conditions
    # planar wave defined on top
    f_dir[:, :] = 0.0
    f_dir[0, 0:N] = 1.0
    # spherical wave defined on top
    #f_dir[:, :] = 0.0
    #f_dir[0, int(N/2)] = 10.0

    # -- initialize
    alpha_rob[:, :] = - wavenumber * 1j

    # -- define material density matrix
    chi = preprocessing._set_chi(M, N, x, y)
    chi = preprocessing.set2zero(chi, domain_omega)

    # -- define absorbing material
    Alpha = 10.0 - 10.0 * 1j
    # -- this is the function you have written during your project
    #import compute_alpha
    #Alpha = compute_alpha.compute_alpha(...)
    alpha_rob = Alpha * chi

    # -- set parameters for optimization
    S = 0  # surface of the fractal
    for i in range(0, M):
        for j in range(0, N):
            if domain_omega[i, j] == _env.NODE_ROBIN:
                S += 1
    V_0 = 1  # initial volume of the domain
    V_obj = numpy.sum(numpy.sum(chi)) / S  # constraint on the density
    mu = 5  # initial gradient step
    mu1 = 10**(-5)  # parameter of the volume functional

    # ----------------------------------------------------------------------
    # -- Do not modify this cell, these are the values that you will be assessed against.
    # ----------------------------------------------------------------------
    # -- compute finite difference solution
    u = processing.solve_helmholtz(domain_omega, spacestep, wavenumber, f, f_dir, f_neu, f_rob,
                        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob)
    chi0 = chi.copy()
    u0 = u.copy()

    # ----------------------------------------------------------------------
    # -- Fell free to modify the function call in this cell.
    # ----------------------------------------------------------------------
    # -- compute optimization
    energy = numpy.zeros((100+1, 1), dtype=numpy.float64)
    chi, energy, u, grad = your_optimization_procedure(domain_omega, spacestep, f, f_dir, f_neu, f_rob,
                           beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                           Alpha, mu, chi, V_obj)
    #chi, energy, u, grad = solutions.optimization_procedure(domain_omega, spacestep, wavenumber, f, f_dir, f_neu, f_rob,
    #                    beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
    #                    Alpha, mu, chi, V_obj, mu1, V_0)
    # --- en of optimization

    chin = chi.copy()
    un = u.copy()

    # -- plot chi, u, and energy
    postprocessing.plot_domain(domain_omega)
    postprocessing._plot_uncontroled_solution(u0, chi0)
    postprocessing._plot_controled_solution(un, chin)
    err = un - u0
    postprocessing._plot_error(err)
    postprocessing._plot_energy_history(energy)
    print("Valeur des énergies : ", energy)

    print('End.')
