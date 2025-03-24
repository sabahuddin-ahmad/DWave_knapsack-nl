# Copyright 2025 D-Wave
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

## ------- import packages -------
from dwave.system import LeapHybridNLSampler
from dwave.optimization import Model

def set_sampler():
    """Return a sampler"""
    ## TODO: Import the package and add sampler here
    sampler = LeapHybridNLSampler()

    return sampler

def build_nl(values, weights, capacity, max_items_allowed):
    """ Build the NL model for our problem

    Requirements:
        Objective: 
            - Maximize the total value of the container
            
        Constraints:
            - Total weight of the shipped container should not exceed the capacity weight
            - At most max_items_allowed can be included in the container
            
    Args:
        values (list):
            A 1 D array-like (row vector) listing the value of each item
            
        weights (list):
            A 1 D array-like (row vector) listing the weight of each item
            
        capacity (int):
            Maximum weight the container can hold
               
        max_items_allowed (int):
            The maximum number of items that can be included in the container
               
    Returns:
        A model encoding the knapsack problem
    """
   
    ## TODO: Import the package and construct the model
    model = Model()

    # Create the binary variables 
    nbr_items = len(weights)
    x = model.binary(nbr_items)

    # Add constants 
    values = model.constant(values)
    weights = model.constant(weights)
    capacity = model.constant(capacity)
    max_items_allowed = model.constant(max_items_allowed)

    ## TODO: Set the objective mentioned in the README
    model.minimize((-values*x).sum())

    ## TODO: Add constraints to reflect the restrictions in the README
    model.add_constraint((weights*x).sum() <= capacity)
    model.add_constraint(x.sum() <= max_items_allowed)
        
    return model

def solve_problem(model, sampler):
    """Run the provided NL object on the designated sampler"""

    # Initialize the NL solver
    sampler = set_sampler()

    # Solve the problem using the NL solver
    sampleset = sampler.sample(model, label='Knapsack using NL solver')

    return sampleset

## ------- Main program -------
if __name__ == "__main__":
	
    # Add constants 
    values = [34, 25, 78, 21, 64]
    weights = [3, 5, 9, 4, 2]
    W = 10
    max_items_allowed = 2

    ## Construct the model
    model = build_nl(values, weights, W, max_items_allowed)
	
    ## ------- Run on the QPU -------
    sampler = set_sampler()

    sampleset = solve_problem(model, sampler)

    # Obtain results 
    with model.lock():
        current_state = 0
        print(f"For state {current_state}, {list(sym.state(current_state) for sym in model.iter_decisions())} results in objective {model.objective.state(current_state)}")
