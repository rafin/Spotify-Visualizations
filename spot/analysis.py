import pl as spotify
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch


def simple_stats(playlist):
    '''outputs basic statitics for given playlist
       such as average value for each feature
    '''
    pl_frame = dict_to_frame(playlist)
    means = pl_frame.mean().to_dict()
    print means
    means_list = []
    for key, value in means.iteritems():
        means_list.append([key, round(value, 1)])
    print means
    return means_list

def dict_to_frame(playlist):
    pl_frame = pd.DataFrame(playlist)
    raw_data = pl_frame[['acousticness','danceability',
                     'energy', 'instrumentalness', 'loudness',
                     'speechiness', 'valence', 'popularity',
                     'tempo', 'duration']]
    return raw_data



# def pca_plot(playlist):
#     '''Principle Component Analysis'''
#     pl_frame = pd.DataFrame(playlist)
#     raw_data = pl_frame[['acousticness','danceability',
#                     'energy', 'instrumentalness', 'loudness',
#                     'speechiness', 'valence', 'popularity']]
#     data = raw_data
#     data_clean = data.as_matrix()
#     data = data.transpose()
#     data = data.as_matrix()

#     ## computing d-dimensional mean vector
#     mean = []
#     for row in data:
#         mean.append(np.mean(row))
#     mean_vector = np.array([mean]).T
#     print 'Mean Vector:\n', mean_vector
#     size = len(mean_vector)

#     ## computing the scatter matrix
#     scatter_matrix = np.zeros((size,size))
#     for i in range(data.shape[1]):
#         scatter_matrix += (data[:,i].reshape(size,1) - mean_vector).dot((data[:,i].reshape(size,1) - mean_vector).T)
#     print 'Scatter Matrix:\n', scatter_matrix

#     ## computing eigenvectors and coor. eigenvalues with scatter ..
#     eig_val_sc, eig_vec_sc = np.linalg.eig(scatter_matrix) 
#     for i in range(len(eig_val_sc)):
#         eigvec_sc = eig_vec_sc[:,i].reshape(1,size).T
#         print 'Eigenvector {}: \n{}'.format(i+1, eigvec_sc)
#         print 'Eigenvalue {} from scatter matrix: {}'.format(i+1, eig_val_sc[i])
#         print 40 * '-'

#     ## check if eigenvector-eigenvalue calculation are correct
#     for i in range(len(eig_val_sc)):
#         eigv = eig_vec_sc[:,i].reshape(1,size).T
#         np.testing.assert_array_almost_equal(scatter_matrix.dot(eigv), eig_val_sc[i] * eigv,
#                                             decimal=6, err_msg='', verbose=True)

#     ## Sorting Eignevectors by Decreasing eigenvalues
#     for ev in eig_vec_sc: #vertify they're of equal length, 1
#         np.testing.assert_array_almost_equal(1.0, np.linalg.norm(ev))
#     eig_pairs = [(np.abs(eig_val_sc[i]), eig_vec_sc[:,i]) for i in range(len(eig_val_sc))]
#     eig_pairs.sort(key = lambda x: x[0], reverse=True)
#     for i in eig_pairs:
#         print(i[0])

#     ## Choosing k eigenvectors with the largest eigenvalues
#     matrix_w = np.hstack((eig_pairs[0][1].reshape(size,1), eig_pairs[1][1].reshape(size,1)))
#     print 'Matrix W:\n', matrix_w

#     ## Transforming the samples onto the new subspace
#     transformed = matrix_w.T.dot(data)
#     fig, ax = plt.subplots()
#     ax.scatter(transformed[0,:], transformed[1,:])
#     names = pl_frame['name']
#     print names
#     for i, txt in enumerate(names):
#             ax.annotate(txt, (transformed[0,:][i], transformed[1,:][i]))
#     plt.show()



if __name__ == '__main__':
    pca_plot(playlist)
    #print spotify.pl_data('Starred', 'rino21111')['songs']



















