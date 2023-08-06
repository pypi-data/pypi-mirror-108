import pickle
import tensorflow as tf
from gimmick.distributer import *
from gimmick import mapping

def load(modelfile):
    modelfile_tf = "tf_" + modelfile.split('.')[0] + ".h5"

    modelobj = pickle.load(open(modelfile, 'rb'))
    modelobj.model = tf.keras.models.load_model(modelfile_tf)
    modelobj.metrics = [mapping.metrics_mapping.get(x) for x in modelobj.metrics_keys]
    modelobj.optimizer = mapping.optimizer_mapping.get(modelobj.optimizer_keys)
    modelobj.loss_function = mapping.loss_function_mapping.get(modelobj.loss_function_keys)
    return modelobj