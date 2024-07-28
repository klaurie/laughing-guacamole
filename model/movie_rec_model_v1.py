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
import gurobipy as gp
from gurobipy import GRB


# Function to find the index of a subgenre
def find_index_by_subgenre(genre, genre_df, subgenre=False):

    if subgenre:
        result = genre_df.index[genre_df['Subgenre'] == genre].tolist()
    else:
        result = genre_df.index[genre_df['Genre'] == genre].tolist()

    if len(result) > 0:
        return result
    else:
        return None



def read_data():
    movie_df = pd.read_csv('../categorized_movies.csv')
    output_file_path = 'modified_categorized_movies.csv'
    movie_df.to_csv(output_file_path, index=False)
    user_df = {
        'Genre': ['pop'],
        'Subgenre 1': ['indie pop'],
        'Subgenre 2': ['uk pop'],
        'Subgenre 3': ['j-poprock']
    }
    genre_df = pd.read_excel('Music Genres_Subgenres.xlsx', sheet_name='Data')
    genre_ref_df = pd.read_excel('Music Genres_Subgenres.xlsx', sheet_name='Reference')

    rows_to_remove = []
    # Map genres to their indices
    genre = user_df['Genre'][0]  # Get the genre string
    index = find_index_by_subgenre(genre, genre_ref_df)
    if index is not None:
        user_df['Genre'][0] = index
    else:
        print(f"The genre '{genre}' was not found in the DataFrame.")
        rows_to_remove.append(i)

    for i in range(movie_df.shape[0]):
        # movies mapping
        genre = movie_df.loc[i, 'Genre']  # Get the genre string
        index = find_index_by_subgenre(genre, genre_ref_df)
        if index is not None:
            movie_df.loc[i, 'Genre'] = index
        else:
            print(f"The genre '{genre}' was not found in the DataFrame.")
            rows_to_remove.append(i)

    # Map subgenres to their indices
    for subgenre_col in ['Subgenre 1', 'Subgenre 2', 'Subgenre 3']:
        subgenre = user_df[subgenre_col][0]  # Get the subgenre string
        index = find_index_by_subgenre(subgenre, genre_df, True)
        if index is not None:
            user_df[subgenre_col][0] = index[0]
        else:
            print(f"The subgenre '{subgenre}' was not found in the DataFrame.")
            rows_to_remove.append(i)

        # now for movie data
        subgenre = movie_df[subgenre_col][0]  # Get the subgenre string
        index = find_index_by_subgenre(subgenre, genre_df, 'subgenre')
        if index is not None:
            movie_df[subgenre_col][0] = index[0]
        else:
            print(f"The subgenre '{subgenre}' was not found in the DataFrame.")
            rows_to_remove.append(i)

    # Remove rows that have subgenres not found in the genre DataFrame
    movie_df = movie_df.drop(rows_to_remove).reset_index(drop=True)

    return movie_df, user_df, genre_df


def run_model(user_data, movie_data, genre_reference):
    # Priority (Lower the value, higher the priority). Penalty is 10^(6-x)
    weights = {
        'Objective Component': ['Soundtrack Subgenre 1', 'Soundtrack Subgenre 2', 'Soundtrack Subgenre 3'],
        'Priority': [0, 4, 6, 9]
    }

    # Pre-Processing
    # Identify all counts of inputs
    unique_genres = pd.unique(genre_reference['Genre'])
    num_genres = len(unique_genres)
    unique_movies = pd.unique(movie_data['name'])
    num_movies = len(unique_movies)
    #unique_movie_genres = pd.unique(movie_data['Genre'])
    #num_movie_genres = len(unique_movie_genres)
    num_subgenres = genre_reference.shape[0]

    genre_association = {
        'Action': [5, 1, 2],
        'Adventure': [5, 1, 2],
        'Animation': [0, 1, 9],
        "Biography": [0,5, 10, 9],
        "Drama": [0, 5, 10, 9],
        "Comedy": [0, 10],
        "Crime": [5, 2, 10],
        "Family": [0, 9, 7],
        "Fantasy": [0, 7, 9],
        "Film-Noir": [10, 11, 1],
        "History": [8, 14],
        "Horror": [1, 5, 9, 6],
        "Music": [0, 10, 3, 2],
        "Musical": [0, 10, 3, 2],
        "Mystery": [10, 11, 3],
        "Romance": [0, 10, 3, 4, 12],
        "Sci-Fi": [1, 5, 0, 2],
        "Sport": [0, 1, 2, 5],
        "Thriller": [5, 1, 6],
        "War": [5, 10, 9, 14],
        "Western": [7, 8, 11]
    }

    """
    genre_association_binary = pd.DataFrame(np.zeros((num_movie_genres, num_genres)))
    for i in range(num_movie_genres):
        for j in range(num_genres):
            genre_association_binary.iloc[i, j] = 1

    movie_genres_binary2 = pd.DataFrame(np.zeros(num_movies, num_movie_genres))
    for i in range(num_movies):
        for j in range(num_movie_genres):
            movie_genres_binary2.iloc[i, j] = 1
"""

    # Binary indicator of a movies soundtrack genre
    print(movie_data['Genre'])
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
    user_genres_binary = pd.DataFrame(np.zeros((num_genres)))
    user_genres_binary.iloc[user_data.loc[0, 'Genre']] = 1

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

        # these indicate if user subgenre matches movie subgenre
        z_subgenre1 = m.addVars([a for a in list(range(num_movies))],
                                [a for a in list(range(num_subgenres))], ub=1, vtype=GRB.BINARY, name='z_subgenre1')
        z_subgenre2 = m.addVars([a for a in list(range(num_movies))],
                                [a for a in list(range(num_subgenres))], ub=1, vtype=GRB.BINARY, name='z_subgenre2')
        z_subgenre3 = m.addVars([a for a in list(range(num_movies))],
                                [a for a in list(range(num_subgenres))], ub=1, vtype=GRB.BINARY, name='z_subgenre3')

    """
            # indicate if user genre does not match movie genre
            w = m.addVars([a for a in list(range(num_movie_genres))],
                          [a for a in list(range(num_genres))],
                          ub=1, vtype=GRB.BINARY, name='w')
    """
    # ------------------- Objective Definition ------------------------------------
    if True:
        m.setObjective(gp.quicksum((10**(int(6-weights['Priority'][0])*z_subgenre1[m])) +
                                   (10**(int(6-weights['Priority'][1])*z_subgenre2[m])) +
                                   (10**(int(6-weights['Priority'][2])*z_subgenre3[m])) for m in range(num_movies)
                                   for s in range(num_subgenres)), sense=GRB.MAXIMIZE)

        """
                gp.quicksum((10 ** (int(6 - weights['Priority'][3]) * w[i, j]) for i in range(num_movie_genres)
                             for j in range(num_genres)))
        """
        # End timing for variable and objective creation
        end_var_obj = time.time()

    # ----------------------- Constraint Definition --------------------------------
    if True:
        # Start timing for constraint creation
        start_constraints = time.time()

        # Ensure each user is recommended only one movie
        m.addConstrs(
            (gp.quicksum(x[u, i] for i in range(num_movies)) == 1)
            for u in range(len(user_data))
        )

        # Ensure user is recommended movie with matching overarching genre
        m.addConstr(y_genre[i] >= x[i] * (user_genres_binary.values[0].dot(movie_genres_binary.values[i]))
                    for i in range(num_genres))

        # Prioritize movies with matching subgenres
        m.addConstr(z_subgenre1[i, j] <= (1 - (x[i] * user_subgenres1_binary[i, j] * movie_subgenres_binary[i, j]) for i in range(num_movies) for j in range(num_subgenres)))
        m.addConstr(z_subgenre2[i, j] <= (1 - (x[i] * user_subgenres1_binary[i, j] * movie_subgenres_binary[i, j]) for i in range(num_movies) for j in range(num_subgenres)))
        m.addConstr(z_subgenre3[i, j] <= (1 - (x[i] * user_subgenres1_binary[i, j] * movie_subgenres_binary[i, j]) for i in range(num_movies) for j in range(num_subgenres)))

        # Add constraint to maximize the number of matching subgenres
        m.addConstr(3 >= gp.quicksum(z_subgenre1[i] + z_subgenre2[i] + z_subgenre3[i]
                                                          for i in range(num_movies)))

        """
        m.addConstrs(x[i] <= (1 - (genre_association_binary.iloc[i, j] + movie_genres_binary2[k, i] * user_genres_binary[j])
                     for i in range(num_movie_genres)
                     for j in range(num_genres)
                     for k in range(num_movies)))
        """
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

if __name__ == "__main__":
    movie_df, user_df, genre_df = read_data()
    run_model(user_df, movie_df, genre_df)
