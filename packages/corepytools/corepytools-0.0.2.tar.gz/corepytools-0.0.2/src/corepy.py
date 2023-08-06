import os
import numpy as np
import pandas as pd
import glob
import pickle
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

def sumdum(x,y): # this is only here to test the package upload
    return x*y*y/y


def RootDir(corename, Formation_names):
    root_dir = 'CorePy'
    main_dir = ['CoreData', 'CoreOutput', 'CoreTubes']			# Loading the list of sub-directories
    sub_dir= ['CoreAttributes', 'CoreXRF']    
    
    
    for i in range(0, len(main_dir)):
        dirName = str(root_dir) + '/' + str(main_dir[i])
        if not os.path.exists(dirName):
            os.makedirs(dirName)
    		      
    # builds the necessary subdirectory folders

    for i in range(0, len(sub_dir)):
        dirName = str(root_dir) + '/' + str(main_dir[0]) + '/' + str(sub_dir[i])
        if not os.path.exists(dirName):
		        os.makedirs(dirName)

    # build corename folder    
    
    for i in range(0, len(corename)):
        dirName = str(root_dir) + '/' + str(main_dir[1]) + '/' + str(corename) 
        if not os.path.exists(dirName):
		        os.makedirs(dirName)

    # Build Formation Folder
    for i in range(0, len(Formation_names)):
        dirName = str(root_dir) + '/' + str(main_dir[1]) + '/' + str(corename) + '/' + str(Formation_names) 
        if not os.path.exists(dirName):
		        os.makedirs(dirName)
        return dirName        # this is needed to direct output files
    
def movingaverage(interval, moving_avg):
    window= np.ones(int(moving_avg))/float(moving_avg)
    return np.convolve(interval, window, 'same')
                

def MakeXRFdf(corename,elements,outlier_multiplier,Depth_model,Formation_names):   # bad form here. need to link better but I don't know how to link below RootDir
     
    XRF_file = os.path.join(str('./CorePy/Coredata/CoreXRF/') + corename + '_XRF.csv')
    LODT5 = pd.read_csv(os.path.join(str('./CorePy/Coredata/CoreXRF/') + 'T5iLOD_XRF.csv'))

    files=glob.glob(XRF_file)

    for file in files:
        coredata=pd.read_csv(file)
        coredata[elements]=np.maximum(coredata[elements],LODT5[elements])
        coredata= coredata[   coredata['Formation']==Formation_names]
        Element_outlier=(coredata[elements]).mean()+outlier_multiplier*(coredata[elements]).std()
        coredata['Outliers']=((coredata[elements])>Element_outlier).any(axis='columns')
        coredata = coredata.sort_values([Depth_model])
        return coredata
    
    
def Remove_outliers(coredata):
    coredata_no_outliers=(coredata[coredata['Outliers'] == False]) #excludes outliers from the dataset being evaluated
    return coredata_no_outliers

def Include_outliers(coredata):
    coredata_outliers=(coredata[coredata['Outliers'] == True]) #excludes outliers from the dataset being evaluated
    return coredata_outliers

def PCA_analysis(coredata_no_outliers,elements):
    scaler = StandardScaler() #create a standard scaler object
    pca = PCA() #create a PCA object called pca. could include pca = PCA(n_components=1)
    scaler.fit(coredata_no_outliers[elements].values)
    x_new = pca.fit_transform(scaler.transform(coredata_no_outliers[elements].values)) #
    return x_new

def PCA_explained(coredata_no_outliers,elements):
   
    scaler = StandardScaler() #create a standard scaler object
    pca = PCA() #create a PCA object called pca. could include pca = PCA(n_components=1)
    scaler.fit(coredata_no_outliers[elements].values)
    #x_new = pca.fit_transform(scaler.transform(coredata_no_outliers[elements].values)) #
    #features= np.arange(len(elements))
    pca_explained=pca.explained_variance_ratio_.cumsum()
    return pca_explained

def PCA_matrix_elements(coredata_no_outliers,elements):

    scaler = StandardScaler() #create a standard scaler object
    pca = PCA() #create a PCA object called pca. could include pca = PCA(n_components=1)
    scaler.fit(coredata_no_outliers[elements].values)
    #x_new = pca.fit_transform(scaler.transform(coredata_no_outliers[elements].values)) #
    #features= np.arange(len(elements))
    #cumsum=pca.explained_variance_ratio_.cumsum()
    pca_elements_matrix=pca.components_
    return pca_elements_matrix


def Kmeans_cluster(x_new,coredata_no_outliers,Principal_components, clusters,PC1,PC2):
    x_cluster = x_new[:, np.arange(Principal_components)] #PCs used in clustering
    kmeans = KMeans(n_clusters=clusters) #select the number of clusters
    kmeans.fit(x_cluster) #results from PCA
    Chemofacies_PCA = kmeans.predict(x_cluster)+1 #array of the chemofacies classification for each row
    coredata_no_outliers['Chemofacies_PCA']=Chemofacies_PCA #makes a new column based on above conditional format
    coredata_no_outliers['PCA1']=x_new[:,PC1] #Adds PCA1 to coredata file for reference
    coredata_no_outliers['PCA2']=x_new[:,PC2] #Adds PCA2 to coredata file for reference
    #features= np.arange(len(elements))
    return coredata_no_outliers

def Elbow_method(x_new,Principal_components):
    distortions = []
    X = x_new[:, np.arange(Principal_components)] #PCs used in clustering
    K = range(1,15)
    for k in K:
        kmeanModel = KMeans(n_clusters=k).fit(X)
        kmeanModel.fit(X)
        distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])
    return distortions

def WriteCSV(coredata_no_outliers,coredata_outliers,dirName,corename,Formation_names,Depth_model):
    coredata=pd.concat([coredata_no_outliers, coredata_outliers], ignore_index=True)
    coredata.to_csv  (os.path.join(dirName + '/' + corename + '_' + Formation_names + '.csv'))
    coredata = coredata.sort_values([Depth_model])
    return coredata 

# builds a color dict used in all plots for each chemofacies
def ColorPalette(ColorScheme):
    palette = dict(zip(ColorScheme, sns.color_palette()))
    outfile = open('chemocolor','wb')
    pickle.dump(palette,outfile)
    outfile.close()