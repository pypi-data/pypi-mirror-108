from gimmick import constants
from gimmick.models import autoencoder_dense
import tensorflow as tf

algo_mapping = {
    'autoencoder_dense': autoencoder_dense.Model()
}

optimizer_mapping = {
    'adam': tf.keras.optimizers.Adam(learning_rate=constants.DEFAULT_LEARNING_RATE),
    'adamax': tf.keras.optimizers.Adamax(learning_rate=constants.DEFAULT_LEARNING_RATE),
    'nadam': tf.keras.optimizers.Nadam(learning_rate=constants.DEFAULT_LEARNING_RATE),
    'adagrad': tf.keras.optimizers.Adagrad(learning_rate=constants.DEFAULT_LEARNING_RATE),
    'rmsprop': tf.keras.optimizers.RMSprop(learning_rate=constants.DEFAULT_LEARNING_RATE),
    'sgd': tf.keras.optimizers.SGD(learning_rate=constants.DEFAULT_LEARNING_RATE)
}

metrics_mapping = {
    'mse': tf.keras.metrics.MeanSquaredError(),
    'rmse': tf.keras.metrics.RootMeanSquaredError(),
    'mae': tf.keras.metrics.MeanAbsoluteError(),
    'mape': tf.keras.metrics.MeanAbsolutePercentageError(),
    'msle': tf.keras.metrics.MeanSquaredLogarithmicError(),
    'mean': tf.keras.metrics.Mean(),
    'sum': tf.keras.metrics.Sum(),
    'kldiv': tf.keras.metrics.KLDivergence()
}

loss_function_mapping = {
    'mse': tf.keras.losses.MeanSquaredError(),
    'mae': tf.keras.losses.MeanAbsoluteError(),
    'mape': tf.keras.losses.MeanAbsolutePercentageError(),
    'msle': tf.keras.losses.MeanSquaredLogarithmicError(),
    'kldiv': tf.keras.losses.KLDivergence(),
    'cosine': tf.keras.losses.CosineSimilarity()
}