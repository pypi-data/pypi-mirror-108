import torch
import torch.nn as nn

from .base import Attack


class PGD(Attack):
    
    def __init__(self, model, eps=0.3, alpha=2/255, itrs=40, rstart=False):
        super(PGD, self).__init__(model,"PGD")
        self.eps = eps
        self.alpha = alpha
        self.itrs = itrs
        self.rstart = rstart

    def forward(self, images, labels):
        images = images.clone().detach().to(self.device)
        labels = labels.clone().detach().to(self.device)
        labels = self._transform_label(images, labels)
        
        loss = nn.CrossEntropyLoss()

        adv_images = images.clone().detach()

        if self.rstart:
            # Starting at a uniformly random point
            adv_images = adv_images + torch.empty_like(adv_images).uniform_(-self.eps, self.eps)
            adv_images = torch.clamp(adv_images, min=0, max=1).detach()

        for i in range(self.itrs):
            adv_images.requires_grad = True
            outputs = self.model(adv_images)

            cost = loss(outputs, labels)

            grads = torch.autograd.grad(cost, adv_images,retain_graph=False, create_graph=False)[0]
            
            if self._attack_mode == "targeted" :
                adv_images = adv_images - self.eps*grads.sign()
            else :
                adv_images = adv_images + self.eps*grads.sign()
        
            adv_images = adv_images.detach() - self.alpha*grads.sign()
            delta = torch.clamp(adv_images - images, min=-self.eps, max=self.eps)
            adv_images = torch.clamp(images + delta, min=0, max=1).detach()

        return adv_images