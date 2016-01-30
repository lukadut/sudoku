from bn import Factor

# ----------------------------------------------------------------------------

"""
Bayesian Network Definition
           Pod obciążeniem (O)            Błąd systemu (S)
          /                  \                /
         *                    *              /
    Wina zasilacza (Z)   Wina chłodz. (C)   /
                 \            |            /
                  *           *           *
                   Komputer się wyłącza (W)
"""

O = ('O', ['obciazenie', 'bezczynnosc'])
fO = Factor([O], [0.3, 0.7])

Z = ('Z', ['zasilacz winny', 'zasilacz ok'])
fZ = Factor([O,Z], [0.4, 0.6,\
                    0.2, 0.8])

C = ('C', ['chlodzenie winne', 'chlodzenie ok'])
fC = Factor([O,C], [0.8, 0.2,\
                    0.1, 0.9])

S = ('S', ['system winny', 'system ok'])
fS = Factor([S], [0.25, 0.75])

W = ('W', ['komputer sie wylacza', 'komputer ok'])
fW = Factor([Z,C,S,W], [1.0, 0.0,\
                        1.0, 0.0,\
                        1.0, 0.0,\
                        1.0, 0.0,\
                        0.5, 0.5,\
                        0.5, 0.5,\
                        0.5, 0.5,\
                        0.05, 0.95])

# ----------------------------------------------------------------------------

def simple_inference(query_list, evidence_list=[], \
                     factor_multiply=fO*fZ*fC*fS*fW, \
                     variable_list=['O', 'Z', 'C', 'S', 'W']):
    for ev in evidence_list:
        factor_multiply -= ev
    for var in variable_list:
        if var not in query_list:
            factor_multiply += var
    factor_multiply.normalize()
    print(factor_multiply)

# ----------------------------------------------------------------------------

print("Jakie jest prawdopodobieństwo awarii komputera?")
query_list, evidence_list = ['W'], []
simple_inference(query_list, evidence_list)

print("Jakie jest prawdopodobieństwo awarii komputera w zależności od obciążenia?")
query_list, evidence_list = ['W', 'O'], []
simple_inference(query_list, evidence_list)

print("Jakie jest prawdopodobieństwo awarii komputera, jeśli zasilacz jest winny?")
query_list, evidence_list = ['W'], [('Z', 'zasilacz winny')]
simple_inference(query_list, evidence_list)

print("Jakie jest prawdopodobieństwo awarii komputera, jeśli chłodzenie jest winne?")
query_list, evidence_list = ['W'], [('Z', 'zasilacz winny')]
simple_inference(query_list, evidence_list)

print("Jakie jest prawdopodobieństwo awarii komputera, jeśli jest bezczynny i system jest winny?")
query_list, evidence_list = ['W'], [('O', 'bezczynnosc'), ('S', 'system winny')]
simple_inference(query_list, evidence_list)

print("Jakie jest prawdopodobieństwo awarii komputera, jeśli jest obciążony i system jest winny?")
query_list, evidence_list = ['W'], [('O', 'obciazenie'), ('S', 'system winny')]
simple_inference(query_list, evidence_list)

print("Jakie jest prawdopodobieństwo, że winny jest zasilacz?")
query_list, evidence_list = ['Z'], []
simple_inference(query_list, evidence_list)

print("Jakie jest prawdopodobieństwo, że komputer jest obciążony, jeśli winny jest zasilacz?")
query_list, evidence_list = ['O'], [('Z', 'zasilacz winny')]
simple_inference(query_list, evidence_list)

print("Jakie jest prawdopodobieństwo, że winne jest chłodzenie?")
query_list, evidence_list = ['C'], []
simple_inference(query_list, evidence_list)

print("Jakie jest prawdopodobieństwo, że winny jest system?")
query_list, evidence_list = ['S'], []
simple_inference(query_list, evidence_list)
