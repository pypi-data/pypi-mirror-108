# -*- coding: utf-8 -*-

import numpy as np
from .optimizer import Optimizer, CandidateState 
from scipy.stats import cauchy

"""
R. Tanabe and A. S. Fukunaga, “Improving the search performance of SHADE using 
linear population size reduction”, in Proceedings of the 2014 IEEE Congress 
on EvolutionaryComputation (CEC), pp. 1658–1665, Beijing, China, July 2014.
"""


class Solution(CandidateState):
    """DE solution class"""
    
    def __init__(self, optimizer: Optimizer):
        CandidateState.__init__(self, optimizer)
        #super(Particle, self).__init__(optimizer) # ugly version of the above
        
        self.CR = None
        self.F = None
        self.V = np.zeros([optimizer.dimensions]) * np.nan # mutant vector


class DE(Optimizer):
    """Differential Evolution class"""

    def __init__(self):
        """Initialization"""
        Optimizer.__init__(self)
        #super(PSO, self).__init__() # ugly version of the above

        self.X0 = None
        self.method = 'SHADE'
        self.params = {}

    def _check_params(self):
        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.method == 'SHADE':
            mandatory_params = 'initial_population_size external_archive_size_factor historical_memory_size p_mutation'.split()
            if 'initial_population_size' not in self.params:
                self.params['initial_population_size'] = self.dimensions * 18
                defined_params += 'initial_population_size'.split()
            if 'external_archive_size_factor' not in self.params:
                self.params['external_archive_size_factor'] = 2.6
                defined_params += 'external_archive_size_factor'.split()
            if 'historical_memory_size' not in self.params: # a.k.a. H
                self.params['historical_memory_size'] = 6
                defined_params += 'historical_memory_size'.split()
            if 'p_mutation' not in self.params:
                self.params['p_mutation'] = 0.11
                defined_params += 'p_mutation'.split()    
            optional_params = ''.split()
        elif self.method == 'LSHADE':
            mandatory_params = 'initial_population_size external_archive_size_factor historical_memory_size p_mutation'.split()
            if 'initial_population_size' not in self.params:
                self.params['initial_population_size'] = self.dimensions * 18
                defined_params += 'initial_population_size'.split()
            if 'external_archive_size_factor' not in self.params:
                self.params['external_archive_size_factor'] = 2.6
                defined_params += 'external_archive_size_factor'.split()
            if 'historical_memory_size' not in self.params: # a.k.a. H
                self.params['historical_memory_size'] = 6
                defined_params += 'historical_memory_size'.split()
            if 'p_mutation' not in self.params:
                self.params['p_mutation'] = 0.11
                defined_params += 'p_mutation'.split()  
            optional_params = ''.split()
        else:
            assert False, f'Unknown method! {self.method}'

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)
        
        assert isinstance(self.params['initial_population_size'], int) \
            and self.params['initial_population_size'] > 0, \
            "initial_population_size should be positive integer"
        assert self.params['external_archive_size_factor'] > 0, \
            "external_archive_size should be positive"
        assert isinstance(self.params['historical_memory_size'], int) \
            and self.params['historical_memory_size'] > 0, \
            "historical_memory_size should be positive integer"
        
    def _init_method(self):
        
        # Bounds for position
        self.lb = np.array(self.lb)
        self.ub = np.array(self.ub)

        # Generate a population
        self.Pop = np.array([Solution(self) for c in \
                             range(self.params['initial_population_size'])], dtype=Solution)
        
        # Generate a trial population
        self.Trials = np.array([Solution(self) for c in \
                                range(self.params['initial_population_size'])], dtype=Solution)
        
        # Initalize Archive
        self.A = np.empty([0])
        
        # Prepare historical memory
        self.M_CR = np.full(self.params['historical_memory_size'], 0.5)
        self.M_F = np.full(self.params['historical_memory_size'], 0.5)

        # Generate initial positions
        for i in range(self.params['initial_population_size']):
            
            # Random position
            self.Pop[i].X = np.random.uniform(self.lb, self.ub)
            
            # Using specified particles initial positions
            if self.X0 is not None:
                if i < np.shape(self.X0)[0]:
                    self.Pop[i].X = self.X0[i]

        # Evaluate
        self.collective_evaluation(self.Pop)
        
        self._progress_log()
        
    def _run(self):
        self._check_params()
        self._init_method()
        
        k = 0 # memory index

        for self.it in range(1, self.iterations + 1):
            
            S_CR = np.empty([0])
            S_F = np.empty([0])
            S_dF = np.empty([0])
            
            # find pbest
            top = max(round(np.size(self.Pop) * self.params['p_mutation']), 1)
            pbest = np.random.choice(np.sort(self.Pop)[0:top])
            
            for p, t in zip(self.Pop, self.Trials):
                
                # Update CR, F
                r = np.random.randint(self.params['historical_memory_size'])
                if np.isnan(self.M_CR[r]):
                    p.CR = 0
                else:
                    p.CR = np.random.normal(self.M_CR[r], 0.1)
                    p.CR = np.clip(p.CR, 0, 1)
                p.F = -1
                while p.F <= 0:
                    p.F = min(cauchy.rvs(self.M_F[r], 0.1), 1)
                
                # Compute mutant vector
                r1 = r2 = p
                while r1 is r2 or r1 is p or r2 is p:
                    r1 = np.random.choice(self.Pop)
                    r2 = np.random.choice(np.append(self.Pop, self.A))
                p.V = p.X + p.F * (pbest.X - p.X) + p.F * (r1.X - r2.X)
                p.V = np.clip(p.V, (p.X + self.lb)/2, (p.X + self.ub)/2)
                
                # Compute trial vector
                t.CR = p.CR
                t.F = p.F
                jrand = np.random.randint(self.dimensions)
                for j in range(self.dimensions):
                    if np.random.rand() <= p.CR or j == jrand:
                        t.X[j] = p.V[j]
                    else:
                        t.X[j] = p.X[j]

            # Evaluate population
            self.collective_evaluation(self.Trials)
            
            # Survival for next generation
            for p, t in zip(self.Pop, self.Trials):
                if t.f <= p.f:
                    p.X = np.copy(t.X)
                    p.f = t.f                    
                # Update external archive
                if t.f < p.f:
                    self.A = np.append(self.A, p)
                    if np.size(self.A) > round(np.size(self.Pop) * self.params['external_archive_size_factor']):
                        self.A = np.delete(self.A, 
                                           np.random.randint(np.size(self.A)))
                    S_CR = np.append(S_CR, t.CR) 
                    S_F = np.append(S_F, t.F)
                    S_dF = np.append(S_dF, p.f - t.f)

            # Memory update
            if np.size(S_CR) != 0 and np.size(S_F) != 0:
                w = S_dF / np.sum(S_dF)
                if np.isnan(self.M_CR[k]) or np.max(S_CR) < 1e-100:
                    self.M_CR[k] = np.nan
                else:
                    self.M_CR[k] = np.sum(w * S_CR**2) / np.sum(w * S_CR)
                self.M_F[k] = np.sum(w * S_F**2) / np.sum(w * S_F)
                k += 1
                if k >= self.params['historical_memory_size']:
                    k = 0
                    
            # Linear Population Size Reduction (LPSR)
            if self.method == 'LSHADE':
                N_init = self.params['initial_population_size']
                if self.maximum_evaluations:
                    N_new = round(((4 - N_init) / self.maximum_evaluations) \
                                        * self.evaluations_count + N_init)
                else:
                    N_new = round(((4 - N_init) / self.iterations) \
                                        * self.it + N_init)
                if N_new < np.size(self.Pop):
                    self.Pop = np.sort(self.Pop)[:N_new]
                    self.Trials = self.Trials[:N_new]          
                
            # Update history
            # self.results.cHistory.append(self.best.copy()) # superseded by progress_log()
            self._progress_log()
            
            # Check stopping conditions
            if self._stopping_criteria():
                break

        return self.best
