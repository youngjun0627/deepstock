from dataset import CryptoDataset
from model import LSTM
from activate import load_checkpoint, training
from config import params
import pandas as pd
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import argparse
import asyncio

parser = argparse.ArgumentParser(description='insert saved model name.')
parser.add_argument('--save_name', type=str)

args = parser.parse_args()


def main(csv_file_path):
    #df = pd.read_csv(csv_file_path, nrows=1000)
    print('reading csv file...')
    df = pd.read_csv(csv_file_path)
    print('finish read the file')
    df.dropna(axis = 0, inplace = True)
    print('successfully remove Nan value in dataframe')
    train, val = train_test_split(df)
    print('train: {} \t val:{}'.format(train.shape, val.shape))
    train_dataset = CryptoDataset(train, params['SEQ_LENGTH'], params['FEATURES'], params['TARGET'])
    train_dataloader = DataLoader(train_dataset, batch_size = params['BATCH_SIZE'], shuffle = False, drop_last = True, num_workers = 1)

    val_dataset = CryptoDataset(val, params['SEQ_LENGTH'], params['FEATURES'], params['TARGET'])
    val_dataloader = DataLoader(val_dataset, batch_size = params['BATCH_SIZE'], shuffle = False, drop_last = True, num_workers = 1)

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda:0" if use_cuda else "cpu")
    torch.manual_seed(0)
    torch.cuda.manual_seed(0)
    np.random.seed(0)

    model = LSTM(params['NUM_FEATURES'], params['HIDDEN_SIZE'], params['NUM_LAYERS'], params['OUTPUT_SIZE'], params['DROPOUT']).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.AdamW(model.linear.parameters(), lr=params['LEARNING_RATE'], weight_decay=0.01)

    training(args.save_name, model, 100, train_dataloader, val_dataloader, params['BATCH_SIZE'], optimizer, criterion, device)
if __name__=='__main__':
    main('/mnt/data/guest0/train.csv')

    #use_cuda = torch.cuda.is_available()
    #print(use_cuda)
