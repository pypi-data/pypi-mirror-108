import torch
import torch.nn as nn

class Normalize(nn.Module) :
    def __init__(self, mean=None, std=None) :
        super(Normalize, self).__init__()
        if mean is None:
            self.mean = [0.485, 0.456, 0.406]
        else:
            self.mean = mean
        
        if std is None:
            self.std = [0.229, 0.224, 0.225]
        else:
            self.std = std
        self.mean = torch.Tensor(self.mean)
        self.std = torch.Tensor(self.std)
        
    def forward(self, input):
        # Broadcasting
        mean = self.mean.reshape(1, 3, 1, 1)
        std = self.std.reshape(1, 3, 1, 1)
        return (input - mean) / std
