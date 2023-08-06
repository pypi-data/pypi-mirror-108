import torch
import torch.nn as nn

from .base import Attack

class FGSM(Attack):
    
    def __init__(self, model, eps=0.05):
        super(FGSM,self).__init__(model, "FGSM")
        self.eps = eps
    
    def forward(self, images,labels):
        
        images = images.clone().detach().to(self.device)
        labels = labels.clone().detach().to(self.device)
        labels = self._transform_label(images, labels)
        
        loss = nn.CrossEntropyLoss()
        
        images.requires_grad = True
        outputs = self.model(images)
        cost = self._targeted*loss(outputs,labels)
        
        grads = torch.autograd.grad(cost,images,retain_graph=False,create_graph=False)[0]
        if self._attack_mode == "targeted" :
            adv_imgs = images - self.eps*grads.sign()
        else :
            adv_imgs = images + self.eps*grads.sign()
        
        adv_clamp_imgs = torch.clamp(adv_imgs,min=0,max=1).detach()
        return adv_clamp_imgs