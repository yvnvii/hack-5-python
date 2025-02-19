#!/usr/bin/env python
"""
WF model code
"""

import os
import argparse
import random
import numpy as np

class Population:

    def __init__(self,N = 10,f = 0.2, with_np = False):
        self.N = N
        self.f = f
        self.freq = []
        self.with_np = with_np
        derived_count = round(N*f)

        if(with_np == True):
            #self.pop as numpy
            arr0 = np.zeros(N-derived_count, dtype =int)
            arr1 = np.ones(derived_count, dtype = int)
            self.pop = np.concatenate([arr0, arr1])
        else:
            self.pop = [0]*(N - derived_count)+[1]*derived_count

    def __repr__(self):
        return f"Population(N={self.N}, f={self.f})"

    def step(self, ngens = 1, file = "outfile"):
        
        f = open(file, "w")
        f.write(", ".join(map(str, self.pop))+"\n")

        if self.with_np == True:
            for i in range (ngens):
                self.pop = np.random.choice(self.pop, self.N)
                self.freq.append(np.mean(self.pop))
                if self.isMonomorphic():
                    break
        else:            
            for i in range (ngens):
                self.pop = random.choices(self.pop, k=self.N)
                self.freq.append(sum(self.pop)/self.N)
                f.write(", ".join(map(str,self.pop))+"\n")
                if self.isMonomorphic():
                    f.close()
                    break
        f.close()

    def isMonomorphic(self):
        if (sum(self.pop) == 0 or sum(self.pop) == len(self.pop)):
            return True
        else:
            return False

def test_wf(N = 100, f = 0.5, steps = 10, outfile = "outfile.txt", verbose = False):
    
    if verbose:
        print(f"Simulation: population {N}, frequency {f}, generations {steps}")

    p = Population(N = N, f = f)
    p.step(ngens = steps, file = outfile)

    return p.freq

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", help = "Population size", dest = "n", type = int, default = 100)
    parser.add_argument("-f", help = "Frequency", dest = "f", type = float, default = 0.5)
    parser.add_argument("-g", help = "The number of generations", dest = "steps", type = int, default = 10)
    parser.add_argument("-o", help = "An output file to write out the community state at each given step.", dest = "outfile", type = str, default = "outfile.txt")
    parser.add_argument("-v", "--verbose", help = "increase output verbosity", action = "store_true")
    args = parser.parse_args()
    print(test_wf(args.n, args.f, args.steps,args.outfile, args.verbose))
