import pickle
from gimmick import mapping
from gimmick.image_op import functions as image_functions
from sklearn.model_selection import train_test_split

''' 
This function create and fit model based on passed arguments 
Paramters:

images :                     Images to be passed to learning functions, has shape [N, (2D or 3D)], 
                             where N is number of samples and 2D and 3D denotes image size
algo :                       Algorithm to be used to learn image representation, Eg Autoencode_dense, 
code_length:                 Default 8, Length of intermediate representation or condense space generated 
                             by model. In order to generate a random image sample having dimention equal 
                             to code_length must be passed.
epochs:                      Default 10, number of epoch to be used while training model
batch_size:                  Default 16, batch size of each training/eval/generation step
optimizer:                   Default 'adam', optimizer used to train the model
learning_rate:               Default 0.001, learning rate for training model
loss_function:               Default 'mse', loss function for training model
metrics:                     Default ['mse'], list of metrics to be printed while training
num_encoder_layer:           Default 'auto', number of layers to be used in encoder
num_decoder_layers:          Default 'auto', number of layers to be used in decoder
samples_for_code_statistics: Default 64, samples to be used to generate code statistics
'''
def learn(images, algo, code_length=8, num_encoder_layer='auto', num_decoder_layers='auto', epochs=10, 
          batch_size=16, optimizer='adam', learning_rate=0.001, loss_function='mse', metrics=['mse'],
          samples_for_code_statistics=64):

    print("Number sample:", images.shape[0], "Image shape:", images[0].shape)

    model = mapping.algo_mapping.get(algo, None)
    if not model:
        raise Exception("Algo not implement/present possible values for also are %s" % (mapping.algo_mapping.keys()))

    optimizer_keys = optimizer
    optimizer = mapping.optimizer_mapping.get(optimizer, None)
    if not optimizer:
        raise Exception("Optimizer not implement/present possible values for also are %s" % (mapping.optimizer_mapping.keys()))

    loss_function_keys = loss_function
    loss_function = mapping.loss_function_mapping.get(loss_function, None)
    if not optimizer:
        raise Exception("loss_function not implement/present possible values for also are %s" % (mapping.loss_function_mapping.keys()))

    metrics_keys = metrics
    metrics = [mapping.metrics_mapping.get(x, None) for x in metrics]
    if list(filter(lambda x: x == None, metrics)):
        raise Exception("One or more of the metrics passed is not a valid metrics, possible values are %s" % (mapping.metrics_mapping.keys()))
        
    print("===================================================================")
    print("Algo:\t\t", model)
    print("optimizer:\t", optimizer)
    print("loss_function:\t", loss_function)
    print("metrics:\t", metrics)
    print("Epochs:\t\t", epochs)
    print("batch_size:\t", batch_size)
    print("learning_rate:\t", learning_rate)

    print("===================================================================")

    ## Write code to normalize image to nearest 2 power
    images = image_functions.convert_2dto3d(images)

    model.__init__(learning_rate=learning_rate, optimizer=optimizer, optimizer_keys=optimizer_keys, 
                   loss_function=loss_function, loss_function_keys=loss_function_keys, 
                   metrics=metrics, metrics_keys=metrics_keys,code_length=code_length, 
                   num_encoder_layer=num_encoder_layer, num_decoder_layers=num_decoder_layers)
    model.build_model_graph(images[0].shape)
    
    images_train, images_test = train_test_split(images, test_size=0.3, shuffle=True)

    print("Train:", len(images_train.shape))
    print("Test:", len(images_test.shape))

    model.train(images_train, images_test, epochs=epochs, batch_size=batch_size, validation_split=0.2)
    model.prepare_code_statistics(images_train, batch_size=batch_size, sample_size=samples_for_code_statistics)
    return model