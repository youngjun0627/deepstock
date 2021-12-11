from torch.utils.data import Dataset

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

        self.metrics = self.create_xy_pairs()

    def create_xy_pairs(self):
        pairs = []
        for idx in range(self.data_length - self.seq_length):
            x = self.csv_file[idx:idx + self.seq_length][self.features].values
            y = self.csv_file[idx + self.seq_length:idx + self.seq_length + 1][self.target].values
            pairs.append((x, y))
        return pairs

    def __len__(self):
        return len(self.metrics)

    def __getitem__(self, idx):
        return self.metrics[idx]
