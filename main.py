import torch.optim as optim
from dataset import CryptoDataset
from model import LSTM
from activate import load_checkpoint, training
from config import param
import pandas as pd
import sklearn.model_selection import train_test_split
from torch.util.data import DataLoader

def main(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df.dropna(axis = 0, inplace = True)
    train, val = train_test_split(df)
    train_dataset = CryptoDataset(train, params['SEQ_LENGTH'], params['FEATURES'], params['TARGET'])
    train_dataloader = DataLoader(train_dataset, batch_size = params['BATCH_SIZE'], shuffle = False, drop_last = True, num_workers = 1)

    val_dataset = CryptoDataset(val, params['SEQ_LENGTH'], params['FEATURES'], params['TARGET'])
    val_dataloader = DataLoader(val_dataset, batch_size = params['BATCH_SIZE'], shuffle = False, drop_last = False, num_workers = 1)

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda:0" if use_cuda else "cpu")
    torch.manual_seed(0)
    torch.cuda.manual_seed(0)
    np.radnom.seed(0)

    model = LSTM(params['NUM_FEATURES'], params['HIDDEN_SIZE'], params['NUM_LAYERS'], params['OUTPUT_SIZE'], params['DROPOUT']).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.AdamW(model.linear.parameters(), lr=params['LEARNING_RATE'], weight_decay=0.01)
    training(100)

if __name__=='__main__':
    main('/mnt/data/guest0/train.csv')
