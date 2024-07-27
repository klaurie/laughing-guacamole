"""
Updated on Saturday, July 27, 2024

@author: klaurie
"""

# --------------------- Import Packages ------------------------------
# import os # Package to change your working directory
# os.chdir('C:\Users\Kaitlyn\ProgramProjects\laughing-guacamole')
# os.getcwd()
import pandas as pd
import numpy as np
import random
random.seed(10)
import time
import sys
import re
import gurobipy as gp
from gurobipy import GRB

def run_model(user_data, movie_data, genre_reference):
    # Priority (Lower the value, higher the priority). Penalty is 10^(6-x)
    weights = {
        'Objective Component': ['Soundtrack Subgenre 1', 'Soundtrack Subgenre 2', 'Soundtrack Subgenre 3'],
        'Priority': [0, 4, 6]
    }

    # Pre-Processing
    # Identify all counts of inputs
    unique_genres = pd.unique(genre_reference['Genre'])
    num_genres = len(unique_genres)
    unique_movies = pd.unique(movie_data['name'])
    num_movies = len(unique_movies)

    num_subgenres = genre_reference.shape[0]

    # Binary indicator of a movies soundtrack genre
    movie_genres_binary = pd.DataFrame(np.zeros((num_movies, num_genres)))
    for i in range(num_movies):
            movie_genres_binary.iloc[i, movie_data.loc[i, 'Genre']] = 1

    # Binary indicator of a movies soundtrack subgenres
    movie_subgenres_binary = pd.DataFrame(np.zeros((num_movies, num_subgenres)))
    for i in range(num_movies):
            movie_subgenres_binary.iloc[i, movie_data.loc[i, 'Subgenre 1']] = 1
            movie_subgenres_binary.iloc[i, movie_data.loc[i, 'Subgenre 2']] = 1
            movie_subgenres_binary.iloc[i, movie_data.loc[i, 'Subgenre 3']] = 1

    # Binary indicator of a users genre
    user_genres_binary = pd.DataFrame(np.zeros((num_movies, num_subgenres)))
    user_genres_binary.iloc[user_data['Genre']] = 1

    # Binary indicator of a users subgenre 1
    user_subgenres1_binary = pd.DataFrame(np.zeros((num_movies, num_subgenres)))
    user_subgenres1_binary.iloc[user_data['Subgenre 1']] = 1

    # Binary indicator of a users subgenre 2
    user_subgenres2_binary = pd.DataFrame(np.zeros((num_movies, num_subgenres)))
    user_subgenres2_binary.iloc[user_data['Subgenre 2']] = 1

    # Binary indicator of a users subgenre 3
    user_subgenres3_binary = pd.DataFrame(np.zeros((num_movies, num_subgenres)))
    user_subgenres3_binary.iloc[user_data['Subgenre 3']] = 1

    end_preprocess=time.time()
    # -------------------------- Build Gurobi Model ------------------------------------
    if True:
        """
        Variable Order: x, 
        """
        # Define Model
        m = gp.Model("movie_recommendation_model")

        # Start timing for variable and objective creation
        start_var_obj = time.time()

        # Binary variables to indicate if user is recommended a movie
        x = (m.addVars([a for a in list(range(num_movies))], ub=1, vtype=GRB.BINARY, name='x'))

        # Binary variables to indicate if a user is recommended a movie with matching genre
        y_genre = m.addVars([a for a in list(range(num_movies))], ub=1, vtype=GRB.BINARY, name='y_genre')

        # these indicate if each respective subgenre is in matched movie
        z_subgenre1 = m.addVars([a for a in list(range(num_movies))], ub=1, vtype=GRB.BINARY, name='z_subgenre1')
        z_subgenre2 = m.addVars([a for a in list(range(num_movies))], ub=1, vtype=GRB.BINARY, name='z_subgenre2')
        z_subgenre3 = m.addVars([a for a in list(range(num_movies))], ub=1, vtype=GRB.BINARY, name='z_subgenre3')

    # ------------------- Objective Definition ------------------------------------
    if True:
        m.setObjective(gp.quicksum((10**6(int(6-weights.iloc[1, 2]*z_subgenre1[m]))) +
                                   (10**6(int(6-weights.iloc[2, 2]*z_subgenre2[m]))) +
                                   (10**6(int(6-weights.iloc[3, 2]*z_subgenre3[m]))) for m in range(num_movies)),
                       sense=GRB.MAXIMIZE)

        # End timing for variable and objective creation
        end_var_obj = time.time()

    # ----------------------- Constraint Definition --------------------------------
    if True:
        # Start timing for constraint creation
        start_constraints = time.time()

        # Ensure user is recommended movie with matching overarching genre
        m.addConstr(y_genre[i] == x[i] * (user_genres_binary.values[0].dot(movie_genres_binary.values[i]))
                    for i in range(num_genres))

        # Prioritze movies with mathcing subgenres
        for i in range(num_movies):
            m.addConstr(z_subgenre1[i] <= x[i] * (user_subgenres1_binary.values[0].dot(movie_subgenres_binary.values[i])))
            m.addConstr(z_subgenre2[i] <= x[i] * (user_subgenres2_binary.values[0].dot(movie_subgenres_binary.values[i])))
            m.addConstr(z_subgenre3[i] <= x[i] * (user_subgenres3_binary.values[0].dot(movie_subgenres_binary.values[i])))

        # Add constraint to maximize the number of matching subgenres
        total_subgenre_matches = gp.quicksum(z_subgenre1[i] + z_subgenre2[i] + z_subgenre3[i] for i in range(num_movies))
        m.addConstr(3 >= gp.quicksum(z_subgenre1[i] + z_subgenre2[i] + z_subgenre3[i]
                                                          for i in range(num_movies)))

        # End timing for constraint creation
        end_constraints = time.time()


    m.write("movie_rec_model.lp")

    # Solve Model
    start_solve = time.time()
    m.optimize()
    end_solve = time.time()

    # ----------------------- Write Out Solution -----------------------------
    if True:
        if m.Status == GRB.INFEASIBLE:
            m.computeIIS()

            for c in m.getConstrs():
                if c.IISConstr:
                    print(f"{c.ConstrName}: {c}\n")

            for v in m.getVars():
                if v.IISLB: print(f'\t{v.varname} ≥ {v.LB}')
                if v.IISUB: print(f'\t{v.varname} ≤ {v.UB}')

            # Relax the bounds and try to make the model feasible
            print('The model is infeasible; relaxing the bounds')
            orignumvars = m.NumVars
            # relaxing only variable bounds
            m.feasRelaxS(0, False, True, False)
            # for relaxing variable bounds and constraint bounds use
            # m.feasRelaxS(0, False, True, True)

            m.optimize()

            status = m.Status
            if status in (GRB.INF_OR_UNBD, GRB.INFEASIBLE, GRB.UNBOUNDED):
                print('The relaxed model cannot be solved \
                       because it is infeasible or unbounded')
                sys.exit(1)

            # print the values of the artificial variables of the relaxation
            print('\nSlack values:')
            slacks = m.getVars()[orignumvars:]
            for sv in slacks:
                if sv.X > 1e-9:
                    print('%s = %g' % (sv.VarName, sv.X))

    # returns list of recommended movie/movies?
    return [i for i in range(num_movies) if x[i] == 1]
