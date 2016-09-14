import pl as spotify
import pandas as pd
import numpy as np
import scipy.stats

def dict_to_frame(playlist):
    pl_frame = pd.DataFrame(playlist)
    raw_data = pl_frame[['energy', 'speechiness', 'acousticness',
                        'danceability', 'loudness', 'valence', 'release_date',
                        'instrumentalness']]
    return raw_data

def simple_stats(playlist):
    ''' outputs basic statitics for given playlist
        such as average value for each feature
    '''
    pl_frame = dict_to_frame(playlist)
    means = pl_frame.mean().to_dict()
    means_list = []
    for key, value in means.iteritems():
        means_list.append([key, round(value, 1)])
    return means_list

def confidence_interval(songs, confidence=.9999):
    ''' experimental bound generator for sifter
    '''
    pl_frame = dict_to_frame(songs)
    n = len(pl_frame)
    m, se = np.mean(pl_frame), scipy.stats.sem(pl_frame)
    h = se * scipy.stats.t._ppf((1+confidence)/2., n-1)
    uppers = (m+h).to_dict()
    lowers = (m-h).to_dict()
    keys = ['energy', 'speechiness', 'acousticness',
            'danceability', 'loudness', 'valence', 'release_date',
            'instrumentalness']
    set = []
    for key in keys:
        if key == 'popularity':
            set.append([0, 100])
            continue
        if key == 'release_date':
            set.append([1900, 2016])
            continue
        set.append([round(lowers[key], 0),round(uppers[key], 0)])
    return set

def pca(playlist):
    ''' Principle Component Analysis
    '''
    pl_frame = pd.DataFrame(playlist)
    features = ['energy', 'speechiness', 'acousticness',
                'danceability', 'loudness', 'valence', 'release_date',
                'instrumentalness']
    raw_data = pl_frame[features]
    data = raw_data
    data_clean = data.as_matrix()
    data = data.transpose()
    data = data.as_matrix()

    ## computing d-dimensional mean vector
    mean = []
    for row in data:
        mean.append(np.mean(row))
    mean_vector = np.array([mean]).T
    # print "Mean Vector:\n", mean_vector
    size = len(mean_vector)

    ## computing the scatter matrix
    scatter_matrix = np.zeros((size,size))
    for i in range(data.shape[1]):
        scatter_matrix += (data[:,i].reshape(size,1) - mean_vector).dot((data[:,i].reshape(size,1) - mean_vector).T)
    # print 'Scatter Matrix:\n', scatter_matrix

    ## computing eigenvectors and coor. eigenvalues with scatter ..
    eig_val_sc, eig_vec_sc = np.linalg.eig(scatter_matrix) 
    for i in range(len(eig_val_sc)):
        eigvec_sc = eig_vec_sc[:,i].reshape(1,size).T

    ## check if eigenvector-eigenvalue calculation are correct
    for i in range(len(eig_val_sc)):
        eigv = eig_vec_sc[:,i].reshape(1,size).T
        np.testing.assert_array_almost_equal(scatter_matrix.dot(eigv), eig_val_sc[i] * eigv,
                                            decimal=6, err_msg='', verbose=True)

    ## Sorting Eignevectors by Decreasing eigenvalues
    for ev in eig_vec_sc: #vertify they're of equal length, 1
        np.testing.assert_array_almost_equal(1.0, np.linalg.norm(ev))
    eig_pairs = [(np.abs(eig_val_sc[i]), eig_vec_sc[:,i]) for i in range(len(eig_val_sc))]
    eig_pairs.sort(key = lambda x: x[0], reverse=True)

    ## store two largest eigenvectors for display
    vector1 = [round(n, 2) for n in eig_pairs[0][1].tolist()]
    vector2 = [round(n, 2) for n in eig_pairs[1][1].tolist()]
    weights = zip(features, vector1, vector2)
    print weights.insert(0, ('Weights', 'X', 'Y'))


    ## Choosing k eigenvectors with the largest eigenvalues
    matrix_w = np.hstack((eig_pairs[0][1].reshape(size,1), eig_pairs[1][1].reshape(size,1)))

    ## Transforming the samples onto the new subspace
    transformed = matrix_w.T.dot(data)
    coords = pd.DataFrame(transformed.T)
    return {"coords": coords, "weights": weights,}

def merge_pca(songs, pca):
    for index, row in pca.iterrows():
        songs[index]['pcax'] = round(row[0], 3)
        songs[index]['pcay'] = round(row[1], 3)
    return songs

if __name__ == '__main__':
    playlist = spotify.pl_data('Sleepwalk', 'rino21111')['songs']
    print confidence_interval(playlist)
    #print spotify.pl_data('Starred', 'rino21111')['songs']



















