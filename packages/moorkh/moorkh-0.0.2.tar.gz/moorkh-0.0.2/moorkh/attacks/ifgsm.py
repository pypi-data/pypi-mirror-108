import torch
import torch.nn as nn

from .base import Attack

class IFGSM(Attack):
    """
    Implementaion of the Iterative-Fast Gradient Sign Method
    
    Paper : "Adversarial Examples in the Physical World"
    """
    
    def __init__(self, model, eps=10/255,alpha=1/255,itr=0):
        super(IFGSM,self).__init__(model, "IFGSM")
        self.eps = eps
        self.alpha =alpha
        self.itr = itr if itr else int(min(eps*255 + 4, 1.25*eps*255)) # as mentioned in paper
        
    def forward(self, images,labels):
        
        images = images.clone().detach().to(self.device)
        labels = labels.clone().detach().to(self.device)
        labels = self._transform_label(images, labels)
        ori_imgs = images.clone().detach()
        loss = nn.CrossEntropyLoss()
        
        for i in range(self.itr):
            images.requires_grad = True
            outputs = self.model(images)
            cost = loss(outputs,labels)
            
            grads = torch.autograd.grad(cost,images,retain_graph=False,create_graph=False)[0]
            if self._attack_mode == "targeted" :
                adv_imgs = images - self.eps*grads.sign()
            else :
                adv_imgs = images + self.eps*grads.sign()
        
            a = torch.clamp(ori_imgs - self.eps, min=0)
            # b = max(adv_images, a) = max(adv_images, ori_images-eps, 0)
            b = (adv_imgs >= a).float()*adv_imgs + (adv_imgs < a).float()*a 
            # c = min(ori_images+eps, b) = min(ori_images+eps, max(adv_images, ori_images-eps, 0))
            c = (b > ori_imgs+self.eps).float()*(ori_imgs+self.eps) + (b <= ori_imgs + self.eps).float()*b 
            # images = max(1, c) = min(1, ori_images+eps, max(adv_images, ori_images-eps, 0))
            images = torch.clamp(c, max=1).detach()
        return images