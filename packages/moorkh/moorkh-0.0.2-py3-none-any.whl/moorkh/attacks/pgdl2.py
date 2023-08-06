import torch
import torch.nn as nn

from .base import Attack


class PGDL2(Attack):
    
    def __init__(self, model, eps=1.0, alpha=0.2, itrs=20, rstart=False):
        super(PGDL2, self).__init__(model,"PGDL2")
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
        batch_size = len(adv_images)
        if self.rstart:
            # Starting at a uniformly random point
            delta = torch.empty_like(adv_images).normal_()
            d_flat = delta.view(adv_images.size(0),-1)
            n = d_flat.norm(p=2,dim=1).view(adv_images.size(0),1,1,1)
            r = torch.zeros_like(n).uniform_(0, 1)
            delta *= r/n*self.eps
            
        for i in range(self.itrs):
            adv_images.requires_grad = True
            outputs = self.model(adv_images)

            cost = loss(outputs, labels)

            grads = torch.autograd.grad(cost, adv_images,
                                       retain_graph=False, create_graph=False)[0]

            grad_norms = torch.norm(grads.view(batch_size, -1), p=2, dim=1) + 1e-10
            grads = grads / grad_norms.view(batch_size, 1, 1, 1)
            
            if self._attack_mode == "targeted" :
                adv_images = adv_images.detach() - self.alpha*grads.sign()
            else :
                adv_images = adv_images.detach() + self.alpha*grads.sign()

            delta = adv_images - images
            delta_norms = torch.norm(delta.view(batch_size, -1), p=2, dim=1)
            factor = self.eps / delta_norms
            factor = torch.min(factor, torch.ones_like(delta_norms))
            delta = delta * factor.view(-1, 1, 1, 1)
            adv_images = torch.clamp(images + delta, min=0, max=1).detach()

        return adv_images