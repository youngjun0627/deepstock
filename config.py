params = dict()
params['EPOCHS'] = 1000
params['DROPOUT'] = 0.2
params['DIRECTIONS'] = 1
params['NUM_LAYERS'] = 2
params['BATCH_SIZE'] = 32
params['OUTPUT_SIZE'] = 1
params['SEQ_LENGTH'] = 60
params['NUM_FEATURES'] =  6
params['HIDDEN_SIZE'] = 100
params['LEARNING_RATE'] =  0.0001
params['TARGET'] = "Target"
params['FEATURES'] = ['Close','High', 'Low', 'Open', 'VWAP', 'Volume']

#params['STATE_DIM'] = (params['NUM_LATERS'] * params['DIRECTIONS'], params['BATCH_SIZE'], params['HIDDEN_SIZE'])
