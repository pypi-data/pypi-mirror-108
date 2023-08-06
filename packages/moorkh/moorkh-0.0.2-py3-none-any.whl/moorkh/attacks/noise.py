import torch
import torch.nn as nn

from .base import Attack

class Noise(Attack):
    
    def __init__(self, model, sigma=0.1):
        super(GN, self).__init__(model,"GN")
        self.sigma = sigma
        self._attack_mode = 'only_default'

    def forward(self, images, labels=None):
        images = images.clone().detach().to(self.device)
        adv_images = images + self.sigma*torch.randn_like(images)
        adv_clamp_images = torch.clamp(adv_images, min=0, max=1).detach()

        return adv_clamp_images