import pandas as pd

pd.options.mode.chained_assignment = None



EPOCHS        = 1000
DROPOUT       = 0.2
DIRECTIONS    = 1
NUM_LAYERS    = 2
BATCH_SIZE    = 5
OUTPUT_SIZE   = 1
SEQ_LENGTH    = 60
NUM_FEATURES  = 6
HIDDEN_SIZE   = 100
LEARNING_RATE = 0.0001
STATE_DIM     = NUM_LAYERS * DIRECTIONS, BATCH_SIZE, HIDDEN_SIZE
TARGET        = "Target"
FEATURES      = ['Close','High', 'Low', 'Open', 'VWAP', 'Volume']

if __name__=='__main__':
    df_train = pd.read_csv('/mnt/data/guest0/train.csv', nrows=10000)
    df_train.dropna(axis = 0, inplace = True)
    print(df_train.shape)
    #training_data, validation_data = train_test_split(df_train, test_size=0.2, shuffle=False)

    #print(f"Training data size: {training_data.shape}", f"Validation data size: {validation_data.shape}")

