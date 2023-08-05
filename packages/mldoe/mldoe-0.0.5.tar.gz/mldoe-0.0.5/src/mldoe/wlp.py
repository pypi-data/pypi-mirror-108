import numpy as np
from numba import njit
from math import factorial as fac

def binom(n: int,k: int):
    """
    Compute the binomial coefficient of n chooses k.
    Adapted to return 0 for error cases.

    """
    try:
        return fac(n) // fac(k) // fac(n-k)
    except ValueError:
        return 0

@njit
def ham_dist(mat):
    """
    Compute the hamming distance between all pairs of rows in a matrix.
    :param mat: Input matrix
    :type mat: numpy.array
    :return: vector of all the hamming distances
    :rtype: list

    """
    N,_ = mat.shape
    ham_mat = np.zeros((1,N*N))
    for i  in range(N):
        for j in range(N):
            index = i*N+j
            if i > j:
                reverse_index = j*N+i
                ham_mat[0,index] = ham_mat[0,reverse_index]
            else:
                ham_mat[0,index] = (mat[i,:] != mat[j,:]).sum()
    return list(map(int,ham_mat[0]))

def distance_distribution(mat,m: int):
    """
    Compute the distance distribution of a design with m four-level factor.
    Return a matrix where each the rows are the hamming distance values for the
    four-level part of the design, and where the columns are the hamming distance
    values for the two-level part of the design.
        :param mat: Design matrix
    :type mat: numpy.array
    :param m: Number of four-level factors
    :type m: int
    :return: matrix of the distance distribution 
    :rtype: numpy.array

    """
    N,nm = mat.shape
    n = nm - m
    dd_mat = np.zeros((m+1,n+1))
    flvl_h_mat = ham_dist(mat[:,:m])
    tlvl_h_mat = ham_dist(mat[:,m:])
    for i in range(N*N):
        # Four-level part
        row = flvl_h_mat[i]
        # Two-level part
        col = tlvl_h_mat[i]
        dd_mat[row,col] += 1
    return dd_mat // N

def krawtchouck(j: int,x: int,n: int,s: int):
    """
    Compute the krawtchouck polynomial :math:`P_j(x,n,s) = ` for a given value 
    of n,j and a prime number s. Simplified forms of the polynomials are used when
    x = 0 or j = 0.
    """
    if j == 0:
        return 1
    if x == 0:
        return (s-1)**j  * binom(n,j)
    val = 0
    for i in range(j+1):
        val += ((-1)**i *(s-1)**(j-i) * binom(x,i) * binom(n-x,j-i))
    return val 

def kw_mat(n,s):
    """
    Compute a matrix with all the krawtchouck polynomial values for a given value of n.
    """
    kw = np.zeros((n+1,n+1))
    if s == 2:
        # when j = 0, P = 1
        kw[0,:] = 1
        for j in range(1,n+1):
            for x in range(n+1):
                if x == 0:
                    kw[j,x] = binom(n, j)
                else:
                    kw[j,x] = kw[j,x-1] - kw[j-1,x] - kw[j-1,x-1]
    else:
        for j in range(n+1):
            for x in range(n+1):
                kw[j,x] = krawtchouck(j,x,n,s)
    return kw 
    

def wlp(mat,m):
    """
    Compute the generalized word-length pattern of a design using the method from
    Xu (2001).
    
    :param mat: design matrix
    :type mat: numpy.array
    :param m: number of four-level factors
    :type m: int
    :return: world-length pattern
    :rtype: 1D numpy.array

    """
    N,nm = mat.shape
    n = nm - m
    dd = distance_distribution(mat, m)
    w_mat= np.zeros((m+1,n+1))
    kw_tlvl = kw_mat(n, 2)
    kw_flvl = kw_mat(m, 4)
    for j in range(n+1):
        for i in range(m+1):
            val = 0
            for jj in range(n+1):
                for ii in range(m+1):
                    sol = dd[ii,jj]
                    sol *= kw_flvl[i,ii]
                    sol *= kw_tlvl[j,jj]
                    val += sol
            w_mat[i,j] = int(val // N)
    f_wmat = np.flip(w_mat,axis=1)
    wlp_lst = np.zeros(n+1+m)
    index = 0
    for i in range(n-1,-(m+1),-1):
        wlp_lst[index] = int(np.diagonal(f_wmat,offset=i).sum())
        index += 1
    return wlp_lst