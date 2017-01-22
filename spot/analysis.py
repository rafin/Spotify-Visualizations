import pl as spotify
import pandas as pd
import numpy as np
import scipy.stats
from sklearn.manifold import TSNE
from sklearn.preprocessing import scale

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
    ''' Principle Component Analysis implementation
    '''
    pl_frame = pd.DataFrame(playlist)
    features = ['energy', 'speechiness', 'acousticness',
                'danceability', 'loudness', 'valence',
                'instrumentalness', 'release_date']
    data = pl_frame[features].T.as_matrix()
    ## computing d-dimensional mean vector
    mean = []
    for row in data:
        mean.append(np.mean(row))
    mean_vector = np.array([mean]).T
    size = len(mean_vector)

    ## computing the scatter matrix
    scatter_matrix = np.zeros((size,size))
    for i in range(data.shape[1]):
        scatter_matrix += (data[:,i].reshape(size,1) - mean_vector).dot((data[:,i].reshape(size,1) - mean_vector).T)

    ## computing eigenvectors and coor. eigenvalues with scatter ..
    eig_val_sc, eig_vec_sc = np.linalg.eig(scatter_matrix) 
    for i in range(len(eig_val_sc)):
        eigvec_sc = eig_vec_sc[:,i].reshape(1,size).T

    ## Sorting Eignevectors by Decreasing eigenvalues
    eig_pairs = [(np.abs(eig_val_sc[i]), eig_vec_sc[:,i]) for i in range(len(eig_val_sc))]
    eig_pairs.sort(key = lambda x: x[0], reverse=True)
    print eig_pairs

    ## store two largest eigenvectors for display
    vector1 = [round(n, 2) for n in eig_pairs[0][1].tolist()]
    vector2 = [round(n, 2) for n in eig_pairs[1][1].tolist()]
    weights = map(list, zip(features, vector1, vector2))


    ## Choosing k eigenvectors with the largest eigenvalues
    matrix_w = np.hstack((eig_pairs[0][1].reshape(size,1), eig_pairs[1][1].reshape(size,1)))

    ## Transforming the samples onto the new subspace
    transformed = matrix_w.T.dot(data)
    trasnformed = scale(transformed)
    coords = pd.DataFrame(transformed.T)
    return {"coords": coords, "weights": weights}

def merge_pca(songs, pca):
    for index, row in pca.iterrows():
        songs[index]['pca1'] = round(row[0], 2)
        songs[index]['pca2'] = round(row[1], 2)
    return songs

def tSNE(playlist):
    ''' t-distributed stochastic neighbor embedding implementation
        (heavier alternate to pca)
    '''
    pl_frame = pd.DataFrame(playlist)
    features = ['energy', 'speechiness', 'acousticness',
                'danceability', 'loudness', 'valence',
                'instrumentalness', 'release_date']
    data = pl_frame[features].T.as_matrix()
    data = scale(data)
    data = data.T
    data_tsne = TSNE(learning_rate=100, init='pca').fit_transform(data)
    data_tsne = scale(data_tsne)

    return pd.DataFrame(data_tsne)

def merge_tsne(songs, tsne):
    for index, row in tsne.iterrows():
        songs[index]['tSNE1'] = round(row[0] * 100, 2)
        songs[index]['tSNE2'] = round(row[1] * 100, 2) 
    return songs








