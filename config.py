params = {
        'EPOCHS': 1000,
        'DROPOUT': 0.2,
        'DIRECTIONS': 1,
        'NUM_LAYERS': 2,
        'BATCH_SIZE': 5,
        'OUTPUT_SIZE': 1,
        'SEQ_LENGTH': 60,
        'NUM_FEATURES': 6,
        'HIDDEN_SIZE': 100,
        'LEARNING_RATE' : 0.0001,
        'STATE_DIM' : NUM_LAYERS * DIRECTIONS, BATCH_SIZE, HIDDEN_SIZE
        'TARGET': "Target",
        'FEATURES': ['Close','High', 'Low', 'Open', 'VWAP', 'Volume'],
}
#params['STATE_DIM'] = (params['NUM_LATERS'] * params['DIRECTIONS'], params['BATCH_SIZE'], params['HIDDEN_SIZE'])
