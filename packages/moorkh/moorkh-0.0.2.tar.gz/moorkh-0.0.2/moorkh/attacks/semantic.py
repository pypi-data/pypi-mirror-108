import torch
import torch.nn as nn

from .base import Attack

class Semantic(Attack):
    
    def __init__(self, model,max_val=1.0):
        super(Semantic,self).__init__(model, "Semantic")
        self.max_val = max_val
        self._attack_mode = 'only_default'
        
    def forward(self, images):
        
        images = images.clone().detach().to(self.device)
        adv_clamp_imgs = (self.max_val-images).detach()
        
        return adv_clamp_imgs