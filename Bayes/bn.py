# -*- coding: utf-8 -*-
"""
Simple Bayesian Network inference implementation.
Discrete variables, variable elimination method.
    (c) Przemysław Głomb, IITiS PAN, 'Active Shape Network' project.
History:
    2012120x: added unittest
"""
import numpy as np
import itertools as it
import copy
import unittest

class Factor(dict):

    def __init__(self, variables, values=None):
        """
        Create factor structure given variables, fill values if given.
        """
        dict.__init__(self)
        self.var = variables
        self.vnames, vdom = [v[0] for v in self.var], [v[1] for v in self.var]
        idx = [tuple(v) for v in it.product(*vdom)]
        vals = values if values != None else len(idx) * [0.0]
        for key, val in zip(idx, vals):
            self[key] = val

    def __str__(self):
        """
        Pretty print a factor.
        """
        str1, str2, prec = [], [], 4
        for i, key in enumerate(sorted(self.keys())):
            str1.append('f' + str(key).replace('\'', '').replace(',)', ')'))
            str2.append(str(round(self[key], prec)) + '\n')
        lengths = [len(l) for l in str1]
        maxl = max(lengths)
        for i in range(len(str1)):
            ni = maxl - len(str1[i]) + 1
            str1[i] += ' ' * ni + str2[i]
        n = np.median(lengths) / (2 * len(self.var))
        vnames = [' '*n + str(v[0]).replace('\'', '') + ' '*n for v in self.var]
        return ''.join(vnames) + '\n' + ''.join(str1)

    def make_index(self, master, slave):
        """
        Index for converting from factor to sub-factor.
        """
        vm, vs = [m[0] for m in master.var], [s[0] for s in slave.var]
        idx = [vm.index(s) for s in vs if s in vm]
        if idx == []:
            return []

        keys = np.array(list(master.keys()))[:, np.array(idx)]
        return [tuple(keys[i]) for i in range(keys.shape[0])]

    def __add__(self, variable):
        """
        Sum out a variable from a factor.
        """
        if variable not in self.vnames:
            return copy.deepcopy(self)
        vnew = [v for v in self.var if v[0] != variable]
        fnew = Factor(vnew)
        kn = self.make_index(self, fnew)
        for key, key2 in zip(self.keys(), kn):
            fnew[key2] += self[key]
        return fnew

    def __mul__(self, f2):
        """
        Multiply two factors together.
        """
        assert isinstance(f2, Factor)
        v1, v2 = self.var, f2.var
        vnew = v1 + [v for v in v2 if v not in v1]
        vnew.sort(key=lambda x:x[0])
        fnew = Factor(vnew)
        kn = [self.make_index(fnew, vv) for vv in [self, f2]]
        for key, k0, k1 in zip(fnew.keys(), kn[0], kn[1]):
            fnew[key] = self[k0] * f2[k1]
        return fnew

    def __sub__(self, vv):
        """
        Incorporate evidence for a variable.
        """
        assert isinstance(vv, tuple)
        variable, value = vv
        fnew = copy.deepcopy(self)
        if variable in self.vnames:
            index = self.vnames.index(variable)
            for key in fnew.keys():
                if key[index] != value:
                    fnew[key] = 0.0
        return fnew

    def __eq__(self, other):
        """
        Equality of factors.
        """
        assert isinstance(other, Factor)
        r1 = self.keys() == other.keys()
        v = [abs(round(a - b, 9)) for a, b in \
             zip(self.values(), other.values())]
        r2 = sum(v) == 0
        r3 = self.var == other.var
        return r1 and r2 and r3
    
    def normalize(self):
        """
        Normalize so that factor sums to one.
        """
        fsum = sum(self.values())
        for k in self.keys():
            self[k] /= fsum

# ----------------------------------------------------------------------------

class TestFactor(unittest.TestCase):

    def test_1(self):
        """
        Modeling and Reasoning with Bayesian Networks, ch. 6.
        """
        tf = [True, False]
        B, C, D, E = ('B', tf), ('C', tf), ('D', tf), ('E', tf)
        f1 = Factor([B, C, D], [0.95, 0.05, 0.9, 0.1, 0.8, 0.2, 0, 1])
        f2 = Factor([D, E], [0.448, 0.192, 0.112, 0.248])
        f1D = Factor([B, C], [1.0, 1.0, 1.0, 1.0])
        self.assertEqual(f1D, f1 + 'D')
        f12 = f1 * f2
        self.assertAlmostEqual(f12[(True, True, True, True)], 0.4256)
        self.assertAlmostEqual(f12[(True, True, True, False)], 0.1824)
        self.assertAlmostEqual(f12[(True, True, False, True)], 0.0056)
        self.assertAlmostEqual(f12[(False, False, False, False)], 0.248)
    
    def test_2(self):
        """
        Modeling and Reasoning with Bayesian Networks, ch. 6.
        """
        tf = [True, False]
        A, B, C = ('A', tf), ('B', tf), ('C', tf)
        fA = Factor([A], [0.6, 0.4])
        fBA = Factor([A, B], [0.9, 0.1, 0.2, 0.8])
        fCB = Factor([B, C], [0.3, 0.7, 0.5, 0.5])
        f_res = Factor([C], [0.192, 0.408])
        #print fA, fBA, fCB
        #print (fBA - ('A', True))
        #print (fCB - ('A', True))
        #print ((fA - ('A', True)) * (fBA - ('A', True)) + 'A') * (fCB - ('A', True)) + 'B'
        #print f_res
        self.assertEqual(f_res, fA * fBA * fCB - ('A', True) + 'A' + 'B')
        self.assertEqual(f_res, fA * fBA * fCB + 'B' - ('A', True) + 'A')
        fxx = (fA - ('A', True)) * (fBA - ('A', True)) * (fCB - ('A', True))
        self.assertEqual(f_res, fxx + 'A' + 'B')
        self.assertEqual(f_res, (fCB * fBA + 'B') * fA - ('A', True) + 'A')
        fyy = ((fA - ('A', True)) * (fBA - ('A', True)) + 'A') * \
            (fCB - ('A', True)) + 'B'
        self.assertEqual(f_res, fyy)
    
    def test_3(self):
        """
        Probabilistic Graphical Models, ch. 3.
        """
        D = ('D', ['d0', 'd1'])
        fD = Factor([D], [0.6, 0.4])
        I = ('I', ['i0', 'i1'])
        fI = Factor([I], [0.7, 0.3])
        S = ('S', ['s0', 's1'])
        fS_I = Factor([I, S], [0.95, 0.05,\
                               0.2, 0.8])
        G = ('G', ['g1', 'g2', 'g3'])
        fG_DI = Factor([I, D, G], [0.3, 0.4, 0.3,\
                                   0.05, 0.25, 0.7,\
                                   0.9, 0.08, 0.02,\
                                   0.5, 0.3, 0.2])
        L = ('L', ['l0', 'l1'])
        fL_G = Factor([G, L], [0.1, 0.9,\
                               0.4, 0.6,\
                               0.99, 0.01])
        #print fD, fI, fS_I, fG_DI, fL_G
        #print fmul, sum(fmul.values()) 
#        print fI[('i1',)], fD[('d0',)], fG_DI[('i1', 'd0', 'g2')], \
#                 fS_I[('i1', 's1')], fL_G[('g2', 'l0')], '=',
#        print fI[('i1',)] * fD[('d0',)] * fG_DI[('i1', 'd0', 'g2')] * \
#                 fS_I[('i1', 's1')] * fL_G[('g2', 'l0')]
#        print fmul[('d0', 'g2', 'i1', 'l0', 's1')]
        fmul = fD * fI * fS_I * fG_DI * fL_G
        self.assertEqual(fmul[('d0', 'g2', 'i1', 'l0', 's1')], 0.004608)
        q = fD * fI * fS_I * fG_DI * fL_G \
                + 'D' + 'I' + 'G' + 'S'
        self.assertEqual(np.round(q[('l1',)], 3), 0.502)
        q = fD * fI * fS_I * fG_DI * fL_G - ('I', 'i0') \
                + 'D' + 'I' + 'G' + 'S'
        q.normalize()
        self.assertEqual(np.round(q[('l1',)], 3), 0.389)
        q = fD * (fI - ('I', 'i0')) * fS_I * fG_DI * fL_G \
                + 'D' + 'I' + 'G' + 'S'
        q.normalize()
        self.assertEqual(np.round(q[('l1',)], 3), 0.389)
        q = fD * fI * fS_I * fG_DI * fL_G - ('I', 'i0') - ('D', 'd0') \
                + 'D' + 'I' + 'G' + 'S'
        q.normalize()
        self.assertEqual(np.round(q[('l1',)], 3), 0.513)
        q = fD * fI * fS_I * fG_DI * fL_G - ('G', 'g3') \
                + 'D' + 'L' + 'G' + 'S'
        q.normalize()
        self.assertEqual(np.round(q[('i1',)], 3), 0.079)
        q = fD * fI * fS_I * fG_DI * fL_G - ('G', 'g3') - ('D', 'd1') \
                + 'D' + 'L' + 'G' + 'S'
        q.normalize()
        self.assertEqual(np.round(q[('i1',)], 2), 0.11)
        q = fD * fI * fS_I * fG_DI * fL_G - ('L', 'l0') \
                + 'D' + 'L' + 'G' + 'S'
        q.normalize()
        self.assertEqual(np.round(q[('i1',)], 3), 0.14)
        q = fD * fI * fS_I * fG_DI * fL_G - ('L', 'l0') - ('G', 'g3')\
                + 'D' + 'L' + 'G' + 'S'
        q.normalize()
        self.assertEqual(np.round(q[('i1',)], 3), 0.079)
        q = fD * fI * fS_I * fG_DI * fL_G - ('S', 's1') - ('G', 'g3')\
                + 'D' + 'L' + 'G' + 'S'
        q.normalize()
        self.assertEqual(np.round(q[('i1',)], 3), 0.578)
        
# ----------------------------------------------------------------------------

def show_example():
    X = ['x1', 'x2']
    Y = ['y1', 'y2']
    Z = ['z1', 'z2']
    f1 = Factor([('Z', Z), ('Y', Y)], [0.1, 0.9, 0.5, 0.5])
    f2 = Factor([('X', X), ('Y', Y)], [0.1, 0.3, 0.2, 0.4])
    print('factor f1')
    print(f1)
    print('factor f2')
    print(f2)
    print("f1 + 'Y' =")
    print(f1 + 'Y')
    print("f1 * f2 = ")
    print(f1 * f2)
    print("f1 - ('Y', 'y1') =")
    print(f1 - ('Y', 'y1'))
    print('f1 * f2 + X - (Y, \'y1\') = ')
    print(f1 * f2 + 'X' - ('Y', 'y1'))

# ----------------------------------------------------------------------------

if __name__ == '__main__':
    #show_example()
    unittest.main()