from torch.utils.data import Dataset
from tqdm import tqdm

class CryptoDataset(Dataset):
    """Onchain dataset."""

    def __init__(self, csv_file, seq_length, features, target):
        """
        Args:
        """
        self.csv_file = csv_file
        self.target = target
        self.features = features
        self.seq_length = seq_length
        self.data_length = len(csv_file)
        self.indexes = self.create_start_end_pairs()


    def create_start_end_pairs(self):
        pairs = []
        print('loading dataset...')
        for idx in tqdm(range(self.data_length - self.seq_length)):
            x = [idx, idx + self.seq_length]
            y = [idx + self.seq_length, idx + self.seq_length + 1]
            pairs.append((x, y))
        return pairs


    def create_features_label_pairs(self, index):
        x, y = self.indexes[index]
        start_x, end_x = x
        start_y, end_y = y
        features = self.csv_file[start_x:end_x][self.features].values
        label = self.csv_file[start_y:end_y][self.target].values
        return features, label

    def __len__(self):
        return len(self.indexes)

    def __getitem__(self, idx):
        return self.create_features_label_pairs(idx)
        
