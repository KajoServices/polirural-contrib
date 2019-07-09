import numpy as np


def cosine_similarity(term_1, term_2):
    def get_magnitude(term):
        mag = 0
        inner_square_sum = 0
        for val in term:
            inner_square_sum += val*val
        mag = math.sqrt(inner_square_sum)
        return 1 if mag == 0 else mag

    all_words = []
    for word in term_1:
        all_words.append(word)
    for word in term_2:
        if word not in all_words:
            all_words.append(word)

    all_words.sort()

    term_1_vec, term_2_vec = [], []
    for word in all_words:
        term_1_vec.append(1) if word in term_1 else term_1_vec.append(0)
        term_2_vec.append(1) if word in term_2 else term_2_vec.append(0)

    termsum = 0
    for x in range(len(term_1_vec)):
        termsum += term_1_vec[x] * term_2_vec[x]

    mag_A = get_magnitude(term_1_vec)
    mag_B = get_magnitude(term_2_vec)
    cosine_sim_val = float(termsum) / float(mag_A * mag_B)

    if not isinstance(cosine_sim_val, float) or cosine_sim_val < 1e-5:
        cosine_sim_val = 0.0

    return cosine_sim_val


def build_adjacency_matrix(terms_list):
    num = len(terms_list)
    adj_matrix = np.empty([num, num])

    for x in range(num):
        for y in range(num):
            adj_matrix[x][y] = cosine_similarity(terms_list[x][1],
                                                 terms_list[y][1])
    return adj_matrix


def calc_stationary_probabilities(adj_matrix):
    """
    Code pulled from Duke University, Stats 663 from Dr. Cliburn Chan
    http://people.duke.edu/~ccc14/sta-663-2016/homework/Homework02_Solutions.html#Part-3:-Option-2:-Using-numpy.linalg-with-transpose-to-get-the-left-eigenvectors
    """
    P = adj_matrix / np.sum(adj_matrix, 1)[:, np.newaxis]
    P5000 = np.linalg.matrix_power(P, 5000)
    P5001 = np.dot(P5000, P)
    # Check that P50 is stationary.
    np.testing.assert_allclose(P5000, P5001)
    return P5001


def output_summary(distribution, map_, num_terms):
    """Report result of calc_stationary_probabilities."""
    indices = distribution.argsort()[-(num_terms):][::-1]
    for index in indices:
        print("Term:    " + str(map_[index][0]))
        print("Probability: " + str(distribution[index]))
        print("---------------")
