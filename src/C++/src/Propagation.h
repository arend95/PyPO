#include <iostream>
#include <vector>
#include <complex>
#include <array>
#include <cmath>
#include <thread>
#include <iomanip>
#include <algorithm>
#include <new>

#include "Utils.h"
#include "Structs.h"

#ifndef __Propagation_h
#define __Propagation_h

// T is either double or float, U is return struct (double or float as well)
template <class T, class U> class Propagation
{
    T k;                   // Wavenumber
    int numThreads;             // Number of CPU threads used
    int gs;             // Flattened gridsize of source grids
    int gt;             // Flattened gridsize of target grids

    int step;                   // Number of points calculated by n-1 threads.
                                // Thread n gets slightly different amount, possibly
    T t_direction;         // Time direction. If -1, propagate field forward in time
                                // If 1, propagate backwards in time
    T EPS;

    int toPrint;

    float C_L;
    float MU_0;
    float EPS_VAC;
    float ZETA_0_INV;
    float M_PIf;


    std::complex<T> j;
    std::complex<T> z0;

    std::array<std::array<T, 3>, 3> eye;

public:

    std::vector<std::thread> threadPool;

    Propagation(T k, int numThreads, int gs, int gt, T epsilon, T t_direction);

    // Make T precision utility kit
    Utils<T> ut;

    // Functions for propagating fields between two surfaces
    void propagateBeam_JM(int start, int stop,
                       T *xt, T *yt, T *zt,
                        T *xs, T *ys, T *zs,
                        T *nxt, T *nyt, T *nzt,
                        T *rJxs, T *rJys, T *rJzs,
                        T *iJxs, T *iJys, T *iJzs,
                        T *rMxs, T *rMys, T *rMzs,
                        T *iMxs, T *iMys, T *iMzs,
                        T *area, U *res);

    void propagateBeam_EH(int start, int stop,
                       T *xt, T *yt, T *zt,
                        T *xs, T *ys, T *zs,
                        T *rJxs, T *rJys, T *rJzs,
                        T *iJxs, T *iJys, T *iJzs,
                        T *rMxs, T *rMys, T *rMzs,
                        T *iMxs, T *iMys, T *iMzs,
                        T *area, U *res);

    void propagateBeam_JMEH(int start, int stop,
                       T *xt, T *yt, T *zt,
                        T *xs, T *ys, T *zs,
                        T *nxt, T *nyt, T *nzt,
                        T *rJxs, T *rJys, T *rJzs,
                        T *iJxs, T *iJys, T *iJzs,
                        T *rMxs, T *rMys, T *rMzs,
                        T *iMxs, T *iMys, T *iMzs,
                        T *area, U *res);

    void propagateBeam_EHP(int start, int stop,
                       T *xt, T *yt, T *zt,
                        T *xs, T *ys, T *zs,
                        T *nxt, T *nyt, T *nzt,
                        T *rJxs, T *rJys, T *rJzs,
                        T *iJxs, T *iJys, T *iJzs,
                        T *rMxs, T *rMys, T *rMzs,
                        T *iMxs, T *iMys, T *iMzs,
                        T *area, U *res);



    std::array<std::array<std::complex<T>, 3>, 2> fieldAtPoint(T *xs, T *ys, T *zs,
                                                                T *rJxs, T *rJys, T *rJzs,
                                                                T *iJxs, T *iJys, T *iJzs,
                                                                T *rMxs, T *rMys, T *rMzs,
                                                                T *iMxs, T *iMys, T *iMzs,
                                                                const std::array<T, 3> &point_target, T *area);


    void parallelProp_JM(T *xt, T *yt, T *zt,
                        T *xs, T *ys, T *zs,
                        T *nxt, T *nyt, T *nzt,
                        T *rJxs, T *rJys, T *rJzs,
                        T *iJxs, T *iJys, T *iJzs,
                        T *rMxs, T *rMys, T *rMzs,
                        T *iMxs, T *iMys, T *iMzs,
                        T *area, U *res);

    void parallelProp_EH(T *xt, T *yt, T *zt,
                        T *xs, T *ys, T *zs,
                        T *rJxs, T *rJys, T *rJzs,
                        T *iJxs, T *iJys, T *iJzs,
                        T *rMxs, T *rMys, T *rMzs,
                        T *iMxs, T *iMys, T *iMzs,
                        T *area, U *res);

    void parallelProp_JMEH(T *xt, T *yt, T *zt,
                        T *xs, T *ys, T *zs,
                        T *nxt, T *nyt, T *nzt,
                        T *rJxs, T *rJys, T *rJzs,
                        T *iJxs, T *iJys, T *iJzs,
                        T *rMxs, T *rMys, T *rMzs,
                        T *iMxs, T *iMys, T *iMzs,
                        T *area, U *res);

    void parallelProp_EHP(T *xt, T *yt, T *zt,
                        T *xs, T *ys, T *zs,
                        T *nxt, T *nyt, T *nzt,
                        T *rJxs, T *rJys, T *rJzs,
                        T *iJxs, T *iJys, T *iJzs,
                        T *rMxs, T *rMys, T *rMzs,
                        T *iMxs, T *iMys, T *iMzs,
                        T *area, U *res);

    // Functions for calculating angular far-field from reflector directly - no phase term
    void propagateToFarField(int start, int stop,
                            T *xt, T *yt,
                            T *xs, T *ys, T *zs,
                            T *rJxs, T *rJys, T *rJzs,
                            T *iJxs, T *iJys, T *iJzs,
                            T *rMxs, T *rMys, T *rMzs,
                            T *iMxs, T *iMys, T *iMzs,
                            T *area, U *res);

    std::array<std::complex<T>, 3> farfieldAtPoint(T *xs, T *ys, T *zs,
                                                T *rJxs, T *rJys, T *rJzs,
                                                T *iJxs, T *iJys, T *iJzs,
                                                T *rMxs, T *rMys, T *rMzs,
                                                T *iMxs, T *iMys, T *iMzs,
                                                const std::array<T, 3> &r_hat,
                                                T *area);

    void parallelFarField(T *xt, T *yt,
                            T *xs, T *ys, T *zs,
                            T *rJxs, T *rJys, T *rJzs,
                            T *iJxs, T *iJys, T *iJzs,
                            T *rMxs, T *rMys, T *rMzs,
                            T *iMxs, T *iMys, T *iMzs,
                            T *area, U *res);

    // Scalar propagation
    void propagateScalarBeam(int start, int stop,
                             T *xt, T *yt, T *zt,
                            T *xs, T *ys, T *zs,
                            T *rEs, T *iEs, T *area, U *res);


    std::complex<T> fieldScalarAtPoint(T *xs, T *ys, T *zs,
                                                T *rEs, T *iEs,
                                                const std::array<T, 3> &point_target,
                                                T *area);

    void parallelPropScalar(T *xt, T *yt, T *zt,
                            T *xs, T *ys, T *zs,
                            T *rEs, T *iEs, T *area, U *res);

    void joinThreads();

    void _debugArray(T *arr, int idx);
    void _debugArray(std::array<T, 3> arr);
    void _debugArray(std::array<std::complex<T>, 3> arr);
};

template <class T, class U> Propagation<T, U>::Propagation(T k, int numThreads, int gs, int gt, T epsilon, T t_direction)
{
    this->M_PIf = 3.14159265359f;
    this->C_L = 2.99792458e11f; // mm s^-1
    this->MU_0 = 1.2566370614e-3f; // kg mm s^-2 A^-2
    this->EPS_VAC = 1 / (MU_0 * C_L*C_L);
    this->ZETA_0_INV = 1 / (C_L * MU_0);

    std::complex<T> j(0., 1.);
    std::complex<T> z0(0., 0.);
    this->j = j;
    this->z0 = z0;

    this->k = k;

    this->EPS = epsilon * EPS_VAC; // epsilon is relative permeability

    this->numThreads = numThreads;
    this->gs = gs;
    this->gt = gt;

    this->step = ceil(gt / numThreads);

    threadPool.resize(numThreads);

    this->t_direction = t_direction;

    std::array<std::array<T, 3>, 3> eye;
    eye[0].fill(0.);
    eye[1].fill(0.);
    eye[2].fill(0.);

    eye[0][0] = 1.;
    eye[1][1] = 1.;
    eye[2][2] = 1.;
}

// This function calculates the propagation between source and target, calculates currents
template <class T, class U> void Propagation<T,U>::propagateBeam_JM(int start, int stop,
                                T *xt, T *yt, T *zt,
                                T *xs, T *ys, T *zs,
                                T *nxt, T *nyt, T *nzt,
                                T *rJxs, T *rJys, T *rJzs,
                                T *iJxs, T *iJys, T *iJzs,
                                T *rMxs, T *rMys, T *rMzs,
                                T *iMxs, T *iMys, T *iMzs,
                                T *area, U *res)
{
    // Scalars (T & complex T)
    std::complex<T> e_dot_p_r_perp;    // E-field - perpendicular reflected POI polarization vector dot product
    std::complex<T> e_dot_p_r_parr;    // E-field - parallel reflected POI polarization vector dot product

    // Arrays of Ts
    std::array<T, 3> S_i_norm;         // Normalized incoming Poynting vector
    std::array<T, 3> p_i_perp;         // Perpendicular incoming POI polarization vector
    std::array<T, 3> p_i_parr;         // Parallel incoming POI polarization vector
    std::array<T, 3> S_r_norm;         // Normalized reflected Poynting vector
    std::array<T, 3> p_r_perp;         // Perpendicular reflected POI polarization vector
    std::array<T, 3> p_r_parr;         // Parallel reflected POI polarization vector
    std::array<T, 3> S_out_n;          // Container for Poynting-normal ext products
    std::array<T, 3> point;            // Point on target
    std::array<T, 3> norms;            // Normal vector at point
    std::array<T, 3> e_out_h_r;        // Real part of E-field - H-field ext product

    // Arrays of complex Ts
    std::array<std::complex<T>, 3> e_r;            // Reflected E-field
    std::array<std::complex<T>, 3> h_r;            // Reflected H-field
    std::array<std::complex<T>, 3> n_out_e_i_r;    // Electric current
    std::array<std::complex<T>, 3> temp1;          // Temporary container 1 for intermediate irrelevant values
    std::array<std::complex<T>, 3> temp2;          // Temporary container 2

    std::array<std::complex<T>, 3> jt;
    std::array<std::complex<T>, 3> mt;

    // Return containers
    std::array<std::array<std::complex<T>, 3>, 2> beam_e_h; // Container for storing fieldAtPoint return

    int jc = 0; // Counter

    for(int i=start; i<stop; i++)
    {

        point[0] = xt[i];
        point[1] = yt[i];
        point[2] = zt[i];

        norms[0] = nxt[i];
        norms[1] = nyt[i];
        norms[2] = nzt[i];

        // Calculate total incoming E and H field at point on target
        beam_e_h = fieldAtPoint(xs, ys, zs, rJxs, rJys, rJzs, iJxs, iJys, iJzs,
                                rMxs, rMys, rMzs, iMxs, iMys, iMzs, point, area);

        // Calculate normalised incoming poynting vector.
        ut.conj(beam_e_h[1], temp1);                        // h_conj
        ut.ext(beam_e_h[0], temp1, temp2);                  // e_out_h

        for (int n=0; n<3; n++)
        {
            e_out_h_r[n] = temp2[n].real();                      // e_out_h_r
        }

        //std::cout << this->Et_container.size() << std::endl;

        ut.normalize(e_out_h_r, S_i_norm);                       // S_i_norm

        // Calculate incoming polarization vectors
        ut.ext(S_i_norm, norms, S_out_n);                      // S_i_out_n
        ut.normalize(S_out_n, p_i_perp);                       // p_i_perp
        ut.ext(p_i_perp, S_i_norm, p_i_parr);               // p_i_parr

        // Now calculate reflected poynting vector.
        ut.snell(S_i_norm, norms, S_r_norm);                // S_r_norm

        // Calculate normalised reflected polarization vectors
        ut.ext(S_r_norm, norms, S_out_n);                      // S_r_out_n
        ut.normalize(S_out_n, p_r_perp);                       // p_r_perp
        ut.ext(S_r_norm, p_r_perp, p_r_parr);               // p_r_parr

        // Now, calculate reflected field from target
        ut.dot(beam_e_h[0], p_r_perp, e_dot_p_r_perp);      // e_dot_p_r_perp
        ut.dot(beam_e_h[0], p_r_parr, e_dot_p_r_parr);      // e_dot_p_r_parr

        // Calculate reflected field from reflection matrix
        for(int n=0; n<3; n++)
        {
            e_r[n] = -e_dot_p_r_perp * p_i_perp[n] - e_dot_p_r_parr * p_i_parr[n];

            //this->Et_container[k][i] = e_r[k];
        }

        ut.ext(S_r_norm, e_r, temp1);                       // h_r_temp
        ut.s_mult(temp1, ZETA_0_INV, h_r);                  // h_r

        for(int n=0; n<3; n++)
        {
            temp1[n] = e_r[n] + beam_e_h[0][n]; // e_i_r
            temp2[n] = h_r[n] + beam_e_h[1][n]; // h_i_r
        }

        ut.ext(norms, temp2, jt);
        ut.ext(norms, temp1, n_out_e_i_r);
        ut.s_mult(n_out_e_i_r, -1., mt);

        res->r1x[i] = beam_e_h[0][0].real();//jt[0].real();
        res->r1y[i] = jt[1].real();
        res->r1z[i] = jt[2].real();

        res->i1x[i] = jt[0].imag();
        res->i1y[i] = jt[1].imag();
        res->i1z[i] = jt[2].imag();

        res->r2x[i] = mt[0].real();
        res->r2y[i] = mt[1].real();
        res->r2z[i] = mt[2].real();

        res->i2x[i] = mt[0].imag();
        res->i2y[i] = mt[1].imag();
        res->i2z[i] = mt[2].imag();

        if((i * 100 / this->step) > jc and start == 0 * this->step)
        {
            std::cout << jc << " / 100" << '\r';
            std::cout.flush();
            jc++;
        }

    }
}

template <class T, class U> void Propagation<T, U>::propagateBeam_EH(int start, int stop,
                                T *xt, T *yt, T *zt,
                                T *xs, T *ys, T *zs,
                                T *rJxs, T *rJys, T *rJzs,
                                T *iJxs, T *iJys, T *iJzs,
                                T *rMxs, T *rMys, T *rMzs,
                                T *iMxs, T *iMys, T *iMzs,
                                T *area, U *res)
{
    // Arrays of Ts
    std::array<T, 3> point;            // Point on target

    // Return containers
    std::array<std::array<std::complex<T>, 3>, 2> beam_e_h; // Container for storing fieldAtPoint return

    int jc = 0; // Counter

    for(int i=start; i<stop; i++)
    {

        point[0] = xt[i];
        point[1] = yt[i];
        point[2] = zt[i];

        // Calculate total incoming E and H field at point on target
        beam_e_h = fieldAtPoint(xs, ys, zs, rJxs, rJys, rJzs, iJxs, iJys, iJzs,
                                rMxs, rMys, rMzs, iMxs, iMys, iMzs, point, area);

        res->r1x[i] = beam_e_h[0][0].real();
        res->r1y[i] = beam_e_h[0][1].real();
        res->r1z[i] = beam_e_h[0][2].real();

        res->i1x[i] = beam_e_h[0][0].imag();
        res->i1y[i] = beam_e_h[0][1].imag();
        res->i1z[i] = beam_e_h[0][2].imag();

        res->r2x[i] = beam_e_h[1][0].real();
        res->r2y[i] = beam_e_h[1][1].real();
        res->r2z[i] = beam_e_h[1][2].real();

        res->i2x[i] = beam_e_h[1][0].imag();
        res->i2y[i] = beam_e_h[1][1].imag();
        res->i2z[i] = beam_e_h[1][2].imag();

        if((i * 100 / this->step) > jc and start == 0 * this->step)
        {
            std::cout << jc << " / 100" << '\r';
            std::cout.flush();
            jc++;
        }
    }
}

template <class T, class U> void Propagation<T, U>::propagateBeam_JMEH(int start, int stop,
                                T *xt, T *yt, T *zt,
                                T *xs, T *ys, T *zs,
                                T *nxt, T *nyt, T *nzt,
                                T *rJxs, T *rJys, T *rJzs,
                                T *iJxs, T *iJys, T *iJzs,
                                T *rMxs, T *rMys, T *rMzs,
                                T *iMxs, T *iMys, T *iMzs,
                                T *area, U *res)
{
    // Scalars (T & complex T)
    std::complex<T> e_dot_p_r_perp;    // E-field - perpendicular reflected POI polarization vector dot product
    std::complex<T> e_dot_p_r_parr;    // E-field - parallel reflected POI polarization vector dot product

    // Arrays of Ts
    std::array<T, 3> S_i_norm;         // Normalized incoming Poynting vector
    std::array<T, 3> p_i_perp;         // Perpendicular incoming POI polarization vector
    std::array<T, 3> p_i_parr;         // Parallel incoming POI polarization vector
    std::array<T, 3> S_r_norm;         // Normalized reflected Poynting vector
    std::array<T, 3> p_r_perp;         // Perpendicular reflected POI polarization vector
    std::array<T, 3> p_r_parr;         // Parallel reflected POI polarization vector
    std::array<T, 3> S_out_n;          // Container for Poynting-normal ext products
    std::array<T, 3> point;            // Point on target
    std::array<T, 3> norms;            // Normal vector at point
    std::array<T, 3> e_out_h_r;        // Real part of E-field - H-field ext product

    // Arrays of complex Ts
    std::array<std::complex<T>, 3> e_r;            // Reflected E-field
    std::array<std::complex<T>, 3> h_r;            // Reflected H-field
    std::array<std::complex<T>, 3> n_out_e_i_r;    // Electric current
    std::array<std::complex<T>, 3> temp1;          // Temporary container 1 for intermediate irrelevant values
    std::array<std::complex<T>, 3> temp2;          // Temporary container 2

    std::array<std::complex<T>, 3> jt;
    std::array<std::complex<T>, 3> mt;

    // Return containers
    std::array<std::array<std::complex<T>, 3>, 2> beam_e_h; // Container for storing fieldAtPoint return

    int jc = 0; // Counter

    for(int i=start; i<stop; i++)
    {

        point[0] = xt[i];
        point[1] = yt[i];
        point[2] = zt[i];

        norms[0] = nxt[i];
        norms[1] = nyt[i];
        norms[2] = nzt[i];

        // Calculate total incoming E and H field at point on target
        beam_e_h = fieldAtPoint(xs, ys, zs, rJxs, rJys, rJzs, iJxs, iJys, iJzs,
                                rMxs, rMys, rMzs, iMxs, iMys, iMzs, point, area);

        //res->r1x[i] = 0.;//beam_e_h[0][0].real();

        res->r3x[i] = beam_e_h[0][0].real();
        res->r3y[i] = beam_e_h[0][1].real();
        res->r3z[i] = beam_e_h[0][2].real();

        res->i3x[i] = beam_e_h[0][0].imag();
        res->i3y[i] = beam_e_h[0][1].imag();
        res->i3z[i] = beam_e_h[0][2].imag();

        res->r4x[i] = beam_e_h[1][0].real();
        res->r4y[i] = beam_e_h[1][1].real();
        res->r4z[i] = beam_e_h[1][2].real();

        res->i4x[i] = beam_e_h[1][0].imag();
        res->i4y[i] = beam_e_h[1][1].imag();
        res->i4z[i] = beam_e_h[1][2].imag();

        // Calculate normalised incoming poynting vector.
        ut.conj(beam_e_h[1], temp1);                        // h_conj

        ut.ext(beam_e_h[0], temp1, temp2);                  // e_out_h

        for (int n=0; n<3; n++)
        {
            e_out_h_r[n] = temp2[n].real();                      // e_out_h_r
        }

        //std::cout << this->Et_container.size() << std::endl;

        ut.normalize(e_out_h_r, S_i_norm);                       // S_i_norm

        // Calculate incoming polarization vectors
        ut.ext(S_i_norm, norms, S_out_n);                      // S_i_out_n

        ut.normalize(S_out_n, p_i_perp);                       // p_i_perp
        ut.ext(p_i_perp, S_i_norm, p_i_parr);               // p_i_parr

        // Now calculate reflected poynting vector.
        ut.snell(S_i_norm, norms, S_r_norm);                // S_r_norm

        // Calculate normalised reflected polarization vectors
        ut.ext(S_r_norm, norms, S_out_n);                      // S_r_out_n

        ut.normalize(S_out_n, p_r_perp);                       // p_r_perp
        ut.ext(S_r_norm, p_r_perp, p_r_parr);               // p_r_parr

        // Now, calculate reflected field from target
        ut.dot(beam_e_h[0], p_r_perp, e_dot_p_r_perp);      // e_dot_p_r_perp
        ut.dot(beam_e_h[0], p_r_parr, e_dot_p_r_parr);      // e_dot_p_r_parr

        //res->r1x[i] = beam_e_h[0][0].real();

        // Calculate reflected field from reflection matrix
        for(int n=0; n<3; n++)
        {
            e_r[n] = -e_dot_p_r_perp * p_i_perp[n] - e_dot_p_r_parr * p_i_parr[n];

            //this->Et_container[k][i] = e_r[k];
        }

        ut.ext(S_r_norm, e_r, temp1);                       // h_r_temp
        ut.s_mult(temp1, ZETA_0_INV, h_r);                  // h_r

        for(int n=0; n<3; n++)
        {
            temp1[n] = e_r[n] + beam_e_h[0][n]; // e_i_r
            temp2[n] = h_r[n] + beam_e_h[1][n]; // h_i_r
        }

        ut.ext(norms, temp2, jt);
        ut.ext(norms, temp1, n_out_e_i_r);
        ut.s_mult(n_out_e_i_r, -1., mt);



        res->r1x[i] = jt[0].real();
        res->r1y[i] = jt[1].real();
        res->r1z[i] = jt[2].real();

        res->i1x[i] = jt[0].imag();
        res->i1y[i] = jt[1].imag();
        res->i1z[i] = jt[2].imag();

        res->r2x[i] = mt[0].real();
        res->r2y[i] = mt[1].real();
        res->r2z[i] = mt[2].real();

        res->i2x[i] = mt[0].imag();
        res->i2y[i] = mt[1].imag();
        res->i2z[i] = mt[2].imag();



        if((i * 100 / this->step) > jc and start == 0 * this->step)
        {
            std::cout << jc << " / 100" << '\r';
            std::cout.flush();
            jc++;
        }
    }
}

template <class T, class U> void Propagation<T, U>::propagateBeam_EHP(int start, int stop,
                                T *xt, T *yt, T *zt,
                                T *xs, T *ys, T *zs,
                                T *nxt, T *nyt, T *nzt,
                                T *rJxs, T *rJys, T *rJzs,
                                T *iJxs, T *iJys, T *iJzs,
                                T *rMxs, T *rMys, T *rMzs,
                                T *iMxs, T *iMys, T *iMzs,
                                T *area, U *res)
{
    // Scalars (T & complex T)
    std::complex<T> e_dot_p_r_perp;    // E-field - perpendicular reflected POI polarization vector dot product
    std::complex<T> e_dot_p_r_parr;    // E-field - parallel reflected POI polarization vector dot product

    // Arrays of Ts
    std::array<T, 3> S_i_norm;         // Normalized incoming Poynting vector
    std::array<T, 3> p_i_perp;         // Perpendicular incoming POI polarization vector
    std::array<T, 3> p_i_parr;         // Parallel incoming POI polarization vector
    std::array<T, 3> S_r_norm;         // Normalized reflected Poynting vector
    std::array<T, 3> p_r_perp;         // Perpendicular reflected POI polarization vector
    std::array<T, 3> p_r_parr;         // Parallel reflected POI polarization vector
    std::array<T, 3> S_out_n;          // Container for Poynting-normal ext products
    std::array<T, 3> point;            // Point on target
    std::array<T, 3> norms;            // Normal vector at point
    std::array<T, 3> e_out_h_r;        // Real part of E-field - H-field ext product

    // Arrays of complex Ts
    std::array<std::complex<T>, 3> e_r;            // Reflected E-field
    std::array<std::complex<T>, 3> h_r;            // Reflected H-field
    std::array<std::complex<T>, 3> n_out_e_i_r;    // Electric current
    std::array<std::complex<T>, 3> temp1;          // Temporary container 1 for intermediate irrelevant values
    std::array<std::complex<T>, 3> temp2;          // Temporary container 2

    // Return containers
    std::array<std::array<std::complex<T>, 3>, 2> beam_e_h; // Container for storing fieldAtPoint return

    int jc = 0; // Counter

    for(int i=start; i<stop; i++)
    {

        point[0] = xt[i];
        point[1] = yt[i];
        point[2] = zt[i];

        norms[0] = nxt[i];
        norms[1] = nyt[i];
        norms[2] = nzt[i];

        // Calculate total incoming E and H field at point on target
        beam_e_h = fieldAtPoint(xs, ys, zs, rJxs, rJys, rJzs, iJxs, iJys, iJzs,
                                rMxs, rMys, rMzs, iMxs, iMys, iMzs, point, area);

        // Calculate normalised incoming poynting vector.
        ut.conj(beam_e_h[1], temp1);                        // h_conj
        ut.ext(beam_e_h[0], temp1, temp2);                  // e_out_h

        for (int n=0; n<3; n++)
        {
            e_out_h_r[n] = temp2[n].real();                      // e_out_h_r
        }

        //std::cout << this->Et_container.size() << std::endl;

        ut.normalize(e_out_h_r, S_i_norm);                       // S_i_norm

        // Calculate incoming polarization vectors
        ut.ext(S_i_norm, norms, S_out_n);                      // S_i_out_n
        ut.normalize(S_out_n, p_i_perp);                       // p_i_perp
        ut.ext(p_i_perp, S_i_norm, p_i_parr);               // p_i_parr

        // Now calculate reflected poynting vector.
        ut.snell(S_i_norm, norms, S_r_norm);                // S_r_norm

        // Calculate normalised reflected polarization vectors
        ut.ext(S_r_norm, norms, S_out_n);                      // S_r_out_n
        ut.normalize(S_out_n, p_r_perp);                       // p_r_perp
        ut.ext(S_r_norm, p_r_perp, p_r_parr);               // p_r_parr

        // Now, calculate reflected field from target
        ut.dot(beam_e_h[0], p_r_perp, e_dot_p_r_perp);      // e_dot_p_r_perp
        ut.dot(beam_e_h[0], p_r_parr, e_dot_p_r_parr);      // e_dot_p_r_parr

        // Calculate reflected field from reflection matrix
        for(int n=0; n<3; n++)
        {
            e_r[n] = -e_dot_p_r_perp * p_i_perp[n] - e_dot_p_r_parr * p_i_parr[n];
        }

        ut.ext(S_r_norm, e_r, temp1);                       // h_r_temp
        ut.s_mult(temp1, ZETA_0_INV, h_r);                  // h_r

        res->r1x[i] = e_r[0].real();
        res->r1y[i] = e_r[1].real();
        res->r1z[i] = e_r[2].real();

        res->i1x[i] = e_r[0].imag();
        res->i1y[i] = e_r[1].imag();
        res->i1z[i] = e_r[2].imag();

        res->r2x[i] = h_r[0].real();
        res->r2y[i] = h_r[1].real();
        res->r2z[i] = h_r[2].real();

        res->i2x[i] = h_r[0].imag();
        res->i2y[i] = h_r[1].imag();
        res->i2z[i] = h_r[2].imag();

        res->r3x[i] = S_r_norm[0];
        res->r3y[i] = S_r_norm[1];
        res->r3z[i] = S_r_norm[2];

        if((i * 100 / this->step) > jc and start == 0 * this->step)
        {
            std::cout << jc << " / 100" << '\r';
            std::cout.flush();
            jc++;
        }
    }
}

template <class T, class U> void Propagation<T, U>::propagateScalarBeam(int start, int stop,
                                T *xt, T *yt, T *zt,
                                T *xs, T *ys, T *zs,
                                T *rEs, T *iEs, T *area, U *res)
{
    std::array<T, 3> point_target;
    std::complex<T> ets;

    int jc = 0;

    for(int i=start; i<stop; i++)
    {
        point_target[0] = xt[i];
        point_target[1] = yt[i];
        point_target[2] = zt[i];

        ets = fieldScalarAtPoint(xs, ys, zs, rEs, iEs, point_target, area);

        res->rx[i] = ets.real();
        res->ix[i] = ets.imag();

        if((i * 100 / this->step) > jc and start == 0 * this->step)
        {
            std::cout << jc << " / 100" << '\r';
            std::cout.flush();
            jc++;
        }
    }
}

template <class T, class U> std::array<std::array<std::complex<T>, 3>, 2> Propagation<T, U>::fieldAtPoint(T *xs, T *ys, T *zs,
                                                                             T *rJxs, T *rJys, T *rJzs,
                                                                             T *iJxs, T *iJys, T *iJzs,
                                                                             T *rMxs, T *rMys, T *rMzs,
                                                                             T *iMxs, T *iMys, T *iMzs,
                                                                             const std::array<T, 3> &point_target, T *area)
{
    // Scalars (T & complex T)
    T r;                           // Distance between source and target points
    T r_inv;                       // 1 / r
    T omega;                       // Angular frequency of field
    std::complex<T> Green;         // Container for Green's function
    std::complex<T> r_in_s;        // Container for inner products between wavevctor and currents

    // Arrays of Ts
    std::array<T, 3> source_point; // Container for xyz co-ordinates
    std::array<T, 3> r_vec;        // Distance vector between source and target points
    std::array<T, 3> k_hat;        // Unit wavevctor
    std::array<T, 3> k_arr;        // Wavevector

    // Arrays of complex Ts
    std::array<std::complex<T>, 3> e_field;        // Electric field on target
    std::array<std::complex<T>, 3> h_field;        // Magnetic field on target
    std::array<std::complex<T>, 3> js;             // Electric current at source point
    std::array<std::complex<T>, 3> ms;             // Magnetic current at source point
    std::array<std::complex<T>, 3> e_vec_thing;    // Electric current contribution to e-field
    std::array<std::complex<T>, 3> h_vec_thing;    // Magnetic current contribution to h-field
    std::array<std::complex<T>, 3> k_out_ms;       // Outer product between k and ms
    std::array<std::complex<T>, 3> k_out_js;       // Outer product between k and js
    std::array<std::complex<T>, 3> temp;           // Temporary container for intermediate values

    // Return container
    std::array<std::array<std::complex<T>, 3>, 2> e_h_field; // Return container containing e and h-fields

    e_field.fill(z0);
    h_field.fill(z0);

    omega = C_L * k;

    for(int i=0; i<gs; i++)
    {
        source_point[0] = xs[i];
        source_point[1] = ys[i];
        source_point[2] = zs[i];

        js[0] = {rJxs[i], iJxs[i]};
        js[1] = {rJys[i], iJys[i]};
        js[2] = {rJzs[i], iJzs[i]};

        ms[0] = {rMxs[i], iMxs[i]};
        ms[1] = {rMys[i], iMys[i]};
        ms[2] = {rMzs[i], iMzs[i]};

        ut.diff(point_target, source_point, r_vec);
        ut.abs(r_vec, r);

        r_inv = 1 / r;

        ut.s_mult(r_vec, r_inv, k_hat);
        ut.s_mult(k_hat, k, k_arr);

        // e-field
        ut.dot(k_hat, js, r_in_s);
        ut.s_mult(k_hat, r_in_s, temp);
        ut.diff(js, temp, e_vec_thing);

        ut.ext(k_arr, ms, k_out_ms);

        // h-field
        ut.dot(k_hat, ms, r_in_s);
        ut.s_mult(k_hat, r_in_s, temp);
        ut.diff(ms, temp, h_vec_thing);

        ut.ext(k_arr, js, k_out_js);

        //printf("%.16g\n", r);

        Green = exp(this->t_direction * j * k * r) / (4 * M_PIf * r) * area[i] * j;

        for( int n=0; n<3; n++)
        {
            e_field[n] += (-omega * MU_0 * e_vec_thing[n] + k_out_ms[n]) * Green;
            h_field[n] += (-omega * EPS * h_vec_thing[n] - k_out_js[n]) * Green;
        }
        //printf("%.16g, %.16g\n", Green.real(), Green.imag()); // %s is format specifier
    }

    // Pack e and h together in single container
    e_h_field[0] = e_field;
    e_h_field[1] = h_field;

    //std::cout << ut.abs(e_field) << std::endl;

    return e_h_field;
}

template <class T, class U> std::complex<T> Propagation<T, U>::fieldScalarAtPoint(T *xs, T *ys, T *zs,
                                                T *rEs, T *iEs,
                                                const std::array<T, 3> &point_target,
                                                T *area)
{
    std::complex<T> field(0., 0.);
    std::complex<T> j(0., 1.);
    std::complex<T> _field;

    T r;
    std::array<T, 3> r_vec;
    std::array<T, 3> point_source;

    for(int i=0; i<gs; i++)
    {
        point_source[0] = xs[i];
        point_source[1] = ys[i];
        point_source[2] = zs[i];

        _field = {rEs[i], iEs[i]};

        ut.diff(point_target, point_source, r_vec);
        ut.abs(r_vec, r);

        field += - k * k * _field * exp(-j * k * r) / (4 * M_PIf * r) * area[i];

    }
    return field;
}

template <class T, class U> void Propagation<T, U>::parallelProp_JM(T *xt, T *yt, T *zt,
                                T *xs, T *ys, T *zs,
                                T *nxt, T *nyt, T *nzt,
                                T *rJxs, T *rJys, T *rJzs,
                                T *iJxs, T *iJys, T *iJzs,
                                T *rMxs, T *rMys, T *rMzs,
                                T *iMxs, T *iMys, T *iMzs,
                                T *area, U *res)
{
    int final_step;

    for(int n=0; n<numThreads; n++)
    {
        //std::cout << n << std::endl;
        if(n == (numThreads-1))
        {
            final_step = gt;
        }

        else
        {
            final_step = (n+1) * step;
        }

        //std::cout << final_step << std::endl;

        threadPool[n] = std::thread(&Propagation::propagateBeam_JM,
                                    this, n * step, final_step,
                                    xt, yt, zt,
                                    xs, ys, zs,
                                    nxt, nyt, nzt,
                                    rJxs, rJys, rJzs,
                                    iJxs, iJys, iJzs,
                                    rMxs, rMys, rMzs,
                                    iMxs, iMys, iMzs,
                                    area, res);
    }
    joinThreads();
}

template <class T, class U> void Propagation<T, U>::parallelProp_EH(T *xt, T *yt, T *zt,
                                T *xs, T *ys, T *zs,
                                T *rJxs, T *rJys, T *rJzs,
                                T *iJxs, T *iJys, T *iJzs,
                                T *rMxs, T *rMys, T *rMzs,
                                T *iMxs, T *iMys, T *iMzs,
                                T *area, U *res)
{
    int final_step;

    for(int n=0; n<numThreads; n++)
    {
        //std::cout << n << std::endl;
        if(n == (numThreads-1))
        {
            final_step = gt;
        }

        else
        {
            final_step = (n+1) * step;
        }

        //std::cout << final_step << std::endl;

        threadPool[n] = std::thread(&Propagation::propagateBeam_EH,
                                    this, n * step, final_step,
                                    xt, yt, zt,
                                    xs, ys, zs,
                                    rJxs, rJys, rJzs,
                                    iJxs, iJys, iJzs,
                                    rMxs, rMys, rMzs,
                                    iMxs, iMys, iMzs,
                                    area, res);
    }
    joinThreads();
}

template <class T, class U> void Propagation<T, U>::parallelProp_JMEH(T *xt, T *yt, T *zt,
                                T *xs, T *ys, T *zs,
                                T *nxt, T *nyt, T *nzt,
                                T *rJxs, T *rJys, T *rJzs,
                                T *iJxs, T *iJys, T *iJzs,
                                T *rMxs, T *rMys, T *rMzs,
                                T *iMxs, T *iMys, T *iMzs,
                                T *area, U *res)
{
    int final_step;

    for(int n=0; n<numThreads; n++)
    {
        if(n == (numThreads-1))
        {
            final_step = gt;
        }

        else
        {
            final_step = (n+1) * step;
        }

        threadPool[n] = std::thread(&Propagation::propagateBeam_JMEH,
                                    this, n * step, final_step,
                                    xt, yt, zt,
                                    xs, ys, zs,
                                    nxt, nyt, nzt,
                                    rJxs, rJys, rJzs,
                                    iJxs, iJys, iJzs,
                                    rMxs, rMys, rMzs,
                                    iMxs, iMys, iMzs,
                                    area, res);
    }
    joinThreads();
}

template <class T, class U> void Propagation<T, U>::parallelProp_EHP(T *xt, T *yt, T *zt,
                                T *xs, T *ys, T *zs,
                                T *nxt, T *nyt, T *nzt,
                                T *rJxs, T *rJys, T *rJzs,
                                T *iJxs, T *iJys, T *iJzs,
                                T *rMxs, T *rMys, T *rMzs,
                                T *iMxs, T *iMys, T *iMzs,
                                T *area, U *res)
{
    int final_step;

    for(int n=0; n<numThreads; n++)
    {
        //std::cout << n << std::endl;
        if(n == (numThreads-1))
        {
            final_step = gt;
        }

        else
        {
            final_step = (n+1) * step;
        }

        threadPool[n] = std::thread(&Propagation::propagateBeam_EHP,
                                    this, n * step, final_step,
                                    xt, yt, zt,
                                    xs, ys, zs,
                                    nxt, nyt, nzt,
                                    rJxs, rJys, rJzs,
                                    iJxs, iJys, iJzs,
                                    rMxs, rMys, rMzs,
                                    iMxs, iMys, iMzs,
                                    area, res);
    }
    joinThreads();
}

template <class T, class U> void Propagation<T, U>::parallelPropScalar(T *xt, T *yt, T *zt,
                                    T *xs, T *ys, T *zs,
                                    T *rEs, T *iEs, T *area, U *res)
{
    int final_step;

    for(int n=0; n<numThreads; n++)
    {
        if(n == (numThreads-1))
        {
            final_step = gt;
        }

        else
        {
            final_step = (n+1) * step;
        }

        threadPool[n] = std::thread(&Propagation::propagateScalarBeam,
                                    this, n * step, final_step,
                                    xt, yt, zt,
                                    xs, ys, zs,
                                    rEs, iEs, area, res);
    }
    joinThreads();
}

// Far-field functions to calculate E-vector in far-field
template <class T, class U> void Propagation<T, U>::propagateToFarField(int start, int stop,
                                T *xt, T *yt,
                                T *xs, T *ys, T *zs,
                                T *rJxs, T *rJys, T *rJzs,
                                T *iJxs, T *iJys, T *iJzs,
                                T *rMxs, T *rMys, T *rMzs,
                                T *iMxs, T *iMys, T *iMzs,
                                T *area, U *res)
{
    // Scalars (T & complex T)
    T theta;
    T phi;
    T cosEl;

    std::complex<T> e_th;
    std::complex<T> e_ph;

    std::complex<T> e_Az;
    std::complex<T> e_El;

    // Arrays of Ts
    std::array<T, 2> point_ff;            // Angular point on far-field
    std::array<T, 3> r_hat;                // Unit vector in far-field point direction

    // Arrays of complex Ts
    std::array<std::complex<T>, 3> e;            // far-field E-field

    int jc = 0;
    for(int i=start; i<stop; i++)
    {
        theta   = xt[i];
        phi     = yt[i];
        cosEl   = std::sqrt(1 - sin(theta) * sin(phi) * sin(theta) * sin(phi));

        r_hat[0] = cos(theta) * sin(phi);
        r_hat[1] = sin(theta) * sin(phi);
        r_hat[2] = cos(phi);

        // Calculate total incoming E and H field at point on target
        e = farfieldAtPoint(xs, ys, zs, rJxs, rJys, rJzs, iJxs, iJys, iJzs,
                            rMxs, rMys, rMzs, iMxs, iMys, iMzs, r_hat, area);

        res->r1x[i] = e[0].real();
        res->r1y[i] = e[1].real();
        res->r1z[i] = e[2].real();

        res->i1x[i] = e[0].imag();
        res->i1y[i] = e[1].imag();
        res->i1z[i] = e[2].imag();

        // TODO: Calculate H far fields
        res->r2x[i] = 0.;
        res->r2y[i] = 0.;
        res->r2z[i] = 0.;

        res->i2x[i] = 0.;
        res->i2y[i] = 0.;
        res->i2z[i] = 0.;

        if((i * 100 / this->step) > jc and start == 0 * this->step)
        {
            std::cout << jc << " / 100" << '\r';
            std::cout.flush();
            jc++;
        }
    }
}

template <class T, class U> std::array<std::complex<T>, 3> Propagation<T, U>::farfieldAtPoint(T *xs, T *ys, T *zs,
                                                T *rJxs, T *rJys, T *rJzs,
                                                T *iJxs, T *iJys, T *iJzs,
                                                T *rMxs, T *rMys, T *rMzs,
                                                T *iMxs, T *iMys, T *iMzs,
                                                const std::array<T, 3> &r_hat,
                                                T *area)
{
    // Scalars (T & complex T)
    T omega_mu;                       // Angular frequency of field times mu
    T r_hat_in_rp;                 // r_hat dot product r_prime
    std::complex<T> r_in_s;        // Container for inner products between wavevctor and currents

    // Arrays of Ts
    std::array<T, 3> source_point; // Container for xyz co-ordinates

    // Arrays of complex Ts
    std::array<std::complex<T>, 3> e;        // Electric field on far-field point
    std::array<std::complex<T>, 3> _js;      // Temporary Electric current at source point
    std::array<std::complex<T>, 3> _ms;      // Temporary Magnetic current at source point

    std::array<std::complex<T>, 3> js;      // Build radiation integral
    std::array<std::complex<T>, 3> ms;      // Build radiation integral

    std::array<std::complex<T>, 3> _ctemp;
    std::array<std::complex<T>, 3> js_tot_factor;
    std::array<std::complex<T>, 3> ms_tot_factor;

    // Matrices
    std::array<std::array<T, 3>, 3> rr_dyad;       // Dyadic product between r_hat - r_hat
    std::array<std::array<T, 3>, 3> eye_min_rr;    // I - rr

    e.fill(z0);
    js.fill(z0);
    ms.fill(z0);

    omega_mu = C_L * k * MU_0;

    ut.dyad(r_hat, r_hat, rr_dyad);
    ut.matDiff(this->eye, rr_dyad, eye_min_rr);

    for(int i=0; i<gs; i++)
    {
        source_point[0] = xs[i];
        source_point[1] = ys[i];
        source_point[2] = zs[i];

        ut.dot(r_hat, source_point, r_hat_in_rp);

        std::complex<T> expo = exp(j * k * r_hat_in_rp) * area[i];

        std::complex<T> jx(rJxs[i], iJxs[i]);
        js[0] += jx * expo;

        std::complex<T> jy(rJys[i], iJys[i]);
        js[1] += jy * expo;

        std::complex<T> jz(rJzs[i], iJzs[i]);
        js[2] += jz * expo;

        std::complex<T> mx(rMxs[i], iMxs[i]);
        ms[0] += mx * expo;

        std::complex<T> my(rMys[i], iMys[i]);
        ms[1] += my * expo;

        std::complex<T> mz(rMzs[i], iMzs[i]);
        ms[2] += mz * expo;
    }

    ut.matVec(eye_min_rr, js, _ctemp);
    ut.s_mult(_ctemp, omega_mu, js_tot_factor);

    ut.ext(r_hat, ms, _ctemp);
    ut.s_mult(_ctemp, k, ms_tot_factor);

    for (int n=0; n<3; n++)
    {
        e[n] = -js_tot_factor[n] + ms_tot_factor[n];
    }

    return e;
}

template <class T, class U> void Propagation<T, U>::parallelFarField(T *xt, T *yt,
                                T *xs, T *ys, T *zs,
                                T *rJxs, T *rJys, T *rJzs,
                                T *iJxs, T *iJys, T *iJzs,
                                T *rMxs, T *rMys, T *rMzs,
                                T *iMxs, T *iMys, T *iMzs,
                                T *area, U *res)
{
    int final_step;

    for(int n=0; n<numThreads; n++)
    {
        if(n == (numThreads-1))
        {
            final_step = gt;
        }

        else
        {
            final_step = (n+1) * step;
        }

        threadPool[n] = std::thread(&Propagation::propagateToFarField,
                                    this, n * step, final_step,
                                    xt, yt,
                                    xs, ys, zs,
                                    rJxs, rJys, rJzs,
                                    iJxs, iJys, iJzs,
                                    rMxs, rMys, rMzs,
                                    iMxs, iMys, iMzs,
                                    area, res);
    }
    joinThreads();
}

template <class T, class U> void Propagation<T, U>::joinThreads()
{
    for (std::thread &t : threadPool)
    {
        if (t.joinable())
        {
            t.join();
        }
    }
}

template <class T, class U> void Propagation<T, U>::_debugArray(T *arr, int idx)
{
    T toPrint = arr[idx];
    std::cout << "Value of c-style array, element " << idx << ", is : " << toPrint << std::endl;
}

template <class T, class U> void Propagation<T, U>::_debugArray(std::array<T, 3> arr)
{
    std::cout << "Value of length-3 real array, element 0, is : " << arr[0] << std::endl;
    std::cout << "Value of length-3 real array, element 1, is : " << arr[1] << std::endl;
    std::cout << "Value of length-3 real array, element 2, is : " << arr[2] << std::endl;
}

template <class T, class U> void Propagation<T, U>::_debugArray(std::array<std::complex<T>, 3> arr)
{
    std::cout << "Value of length 3 complex array, element 0, is : "
                << arr[0].real() << " + " << arr[0].imag() << "j"
                <<  std::endl;

    std::cout << "Value of length 3 complex array, element 1, is : "
                << arr[1].real() << " + " << arr[1].imag() << "j"
                <<  std::endl;

    std::cout << "Value of length 3 complex array, element 2, is : "
                << arr[2].real() << " + " << arr[2].imag() << "j"
                <<  std::endl;
}


#endif