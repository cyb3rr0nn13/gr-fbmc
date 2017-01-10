#
# Copyright 2004,2009,2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy as np

class preamble_config:
    def __init__(self, taps, N, L, pos=3, u=1, q=4, A=1.0):
        """
        Calculates preamble with independent Zadoff-Chu sequence
        :param taps: Filter taps of length O*N
        :param pos: Block position of preamble in first symbol
        :param N: Subcarrier number
        :param L: Periodic length of ZC sequence
        :param u: Parameter for ZC sequence
        :param q: Parameter for ZC sequence
        :param A: Amplitude of ZC sequence
        """
        self.h = np.reshape(taps, (-1, N//2))
        self.N = N
        self.k = pos
        self.L = L
        self.u = u
        self.q = q
        self.A = A
        self.c = self.build_preamble_symbols()

    def get_zadoff_chu(self, length):
        """ Returns Zadoff-Chu sequence of length """
        zc = self.A*np.array([np.exp(-1j*np.pi*self.u*n*(n+1+2*self.q)/self.L) for n in range(length)])
        return zc

    def get_compensated_zadoff_chu(self, length):
        """ Returns Zadoff-Chu sequence with interference compensation """
        Z = self.get_zadoff_chu(length) - length//2 * (sum(self.h[:][:self.k-1]))
        return Z

    def get_c_sequence(self):
        h = self.h
        k = self.k
        Z_tilde = self.get_compensated_zadoff_chu(self.N)
        C1 = np.empty(self.N//2, dtype=complex)
        C2 = np.empty(self.N//2, dtype=complex)

        for i in range(self.N//4 + 1):
            H = np.matrix([[    h[k][i],    h[k][-i]],
                           [   -h[k-1][i], h[k-1][-i]]])
            H = np.linalg.inv(H)
            Z = np.matrix([Z_tilde[i], np.conj(Z_tilde[-i])])
            C = np.array(Z*H)[0]
            C1[i] = C[0]
            C2[i] = 1j*C[1]
        C1[self.N//4+1:] = (np.conj(C1[1:self.N//4]))[::-1]
        C2[self.N//4+1:] = (np.conj(C2[1:self.N//4]))[::-1]
        return np.array([C1, C2])

    def build_preamble_symbols(self):
        """
        Return final preamble symbols of length N
        Map like this:
            a_{2n, 2m'} = c_n^R
            a_{2n, 2m'+1} = c_n^I
        """
        C = self.get_c_sequence()
        c = 2/self.l/self.N * np.fft.fft(C[0] + 1j*C[1])  # c_2n^R
        return c

    def get_preamble(self):
        return self.c