import eel
import utils
# import file exist and validating function
from utils.check_file import is_file_valid
# import process parameters to int or str function
from utils.process_parameters import process_parameters
# import data pre-processing functions
from utils.data_preprocess_regression import regression_dataset
from utils.data_preprocess_classification import classification_dataset
from utils.data_preprocess_clustering import clustering_dataset
from utils.data_preprocess_anomaly import anomaly_dataset
from utils.data_preprocess_dimension import dimension_dataset
# import model build classes
from ml_models.regression_models import Build_Regression_Model
from ml_models.classification_models import Build_Classification_Model
from ml_models.clustering_models import Build_Clustering_Model
from ml_models.anomaly_models import Build_Anomaly_Model
from ml_models.dimension_models import Build_Dimension_Model
# import evaluation metrics
from utils.evaluate_performance import regression_metrics, classification_metrics
from utils.evaluate_performance import base64_regression_metrics, base64_classification_metrics
from utils.evaluate_performance import base64_confusion_matrix

eel.init('web')

@eel.expose
def check_file_exists(file_name):
	return is_file_valid(file_name)

@eel.expose
def get_parameters(model_type, model_name, dataset_files,
				   para = None):
	'''
	Param:
	------
		model_type (str) : ML model classification
		model_name (str) : ML model name
		dataset_files (dict) : path to train and test dataset files
		para (dict) : parameters for model
					  keys and values are type str where
					  values may separate by ','
	'''

	# convert str parameter values to int
	if para != None: 
		para = process_parameters(para, model_type)

	# build model
	if model_type == 'regression':
		data_dict_regression = regression_dataset(dataset_files)
		if data_dict_regression == None:
			return 'fail'
		train_data_dict, test_data_dict = data_dict_regression

		# apply model on data files
		model = Build_Regression_Model(train_data_dict['X_train'], train_data_dict['Y_train'],
										model_name, para)
		# fit model
		try:
			model.fit()
			# prdict dataset
			Y_train_pred = model.predict(train_data_dict['X_train'])
			Y_eval_pred = model.predict(train_data_dict['X_eval'])
			Y_test_pred = model.predict(test_data_dict['X'])

			# get evaluation metrics
			n, p = len(train_data_dict['X_train']), len(train_data_dict['X_train'][0])
			train_data_metrics = regression_metrics(train_data_dict['Y_train'], Y_train_pred, n, p)
			n, p = len(train_data_dict['X_eval']), len(train_data_dict['X_eval'][0])
			eval_data_metrics = regression_metrics(train_data_dict['Y_eval'], Y_eval_pred, n, p)

			# get base64 plots
			train_data_metrics_plot  = base64_regression_metrics(train_data_metrics) 
			eval_data_metrics_plot = base64_regression_metrics(eval_data_metrics)

			evaluation_metrics = [train_data_metrics_plot, eval_data_metrics_plot]
			return evaluation_metrics
		except:
			return 'fail'

	if model_type == 'classification':
		data_dict_classification = classification_dataset(dataset_files)
		if data_dict_classification == None:
			return 'fail'
		train_data_dict, test_data_dict = data_dict_classification

		# apply model on data files
		model = Build_Classification_Model(train_data_dict['X_train'], train_data_dict['Y_train'],
										model_name, para)
		# fit model
		try:
			model.fit()
			# prdict dataset
			Y_train_pred = model.predict(train_data_dict['X_train'])
			Y_eval_pred = model.predict(train_data_dict['X_eval'])
			Y_test_pred = model.predict(test_data_dict['X'])

			# get evaluation metrics
			train_data_metrics = classification_metrics(train_data_dict['Y_train'], Y_train_pred)
			eval_data_metrics = classification_metrics(train_data_dict['Y_eval'], Y_eval_pred)

			# get base64 plots
			train_data_metrics_plot = base64_classification_metrics(train_data_metrics)
			eval_data_metrics_plot = base64_classification_metrics(eval_data_metrics)
			train_data_confusion_matrix_plot = base64_confusion_matrix(train_data_metrics)
			eval_data_confusion_matrix_plot = base64_confusion_matrix(eval_data_metrics)

			evaluation_metrics = [train_data_metrics_plot, eval_data_metrics_plot]
			confusion_matrix = [train_data_confusion_matrix_plot, eval_data_confusion_matrix_plot]
			return [evaluation_metrics, confusion_matrix]

		except:
			return 'fail'

	if model_type == 'clustering':
		data_dict_clustering = clustering_dataset(dataset_files)
		if data_dict_clustering == None:
			return 'fail'
		train_data_dict = data_dict_clustering

		# apply model on data file
		try:
			model = Build_Clustering_Model(train_data_dict['X'], model_name, para)
			model.fit()
			print(model.clustered_model.labels_)
		except:
			print('Improper parameters')


	if model_type == 'anomaly':
		data_dict_anomaly = anomaly_dataset(dataset_files, model_name)
		if data_dict_anomaly == None:
			return 'fail'
		train_data_dict = data_dict_anomaly

		labels = None
		label_convert = lambda x : -1 if x == -1 else 0
		# apply model on data file
		try:
			model = Build_Anomaly_Model(train_data_dict['X'], model_name, para, 
										train_data_dict.get('Y', None))
			model.fit()
			# dbscan
			if model_name == 'dbscan':
				labels = model.anomaly_model.labels_
			# for rest all models
			else:
				labels = model.predict(train_data_dict['X'])

			print(list(map(label_convert, labels)))
		except:
			print('Improper parameters')


	if model_type == 'dimension':
		data_dict_clustering = dimension_dataset(dataset_files)
		if data_dict_clustering == None:
			return 'fail'
		train_data_dict = data_dict_clustering

		# apply model on data file
		try:
			model = Build_Dimension_Model(train_data_dict['X'], model_name, para)
			model.fit()
			print(model.predict(train_data_dict['X']))
		except:
			print('Improper parameters')


eel.start('index.html', size = (600, 500))