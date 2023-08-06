import torch

class Attack:
    """
    Base class for all attacks
    """
    def __init__(self,model,attck_name):
        self.attck_name = attck_name
        self.model = model
        self.model_name = str(model).split("(")[0]
        self.device = next(model.parameters()).device
        
        self._transform_label = self._get_label
        self._attack_mode = 'default'
        self._ll = 1
    
    def forward(self,*input):
        """
        Logic for each attacks
        """
        raise NotImplementedError
    
    def set_mode_default(self):
        if self._attack_mode == 'only_default': #Targate attack not possible
           self._attack_mode = 'only_default'
        else:
            self._attack_mode = 'default'
        self._transform_label = self._get_label
    
    def set_mode_targeted(self,target_map_function=None):
        """
         Setting configs for tagetted attack mode.

        Args:
            targeted_map_function (function): Label mapping function. Defaults to None.
        """
        if self._attack_mode == 'only_default':
            raise ValueError(f"Changing attack mode is not supported in {self.attck_name} attack.")
        
        self._attack_mode = "targeted"
        if target_map_function is None:
            self._target_map_function = lambda images, labels:labels
        else:
            self._target_map_function = target_map_function
        self._transform_label = self._get_target_label
    
    def set_mode_least_likely(self,min_class=1):
        """
         Setting configs for least likely attack mode.

        Args:
            min_class (str, optional): smallest probability class for using as target. Defaults to 1.
        """
        self._attack_mode = "targeted"
        self._transform_label = self._get_least_likely_label
        self._ll = min_class
    
    def _get_label(self, images, labels):
        """
        Function for changing the attack mode.
        Return input labels.
        """
        return labels
    
    def _get_target_label(self, images, labels):
        """
        Return input labels.
        """
        return self._target_map_function(images, labels)
    
    def _get_least_likely_label(self, images, labels):
        """
        Return least likely labels.
        """
        outputs = self.model(images)
        if self._ll < 0:
            pos = outputs.shape[1] + self._ll + 1
        else:
            pos = self._ll
        _, labels = torch.kthvalue(outputs.data, pos)
        labels = labels.detach_()
        return labels

    def __call__(self,*input,**kwargs):
        training_mode = self.model.training
        
        self.model.eval()

        adv_imgs = self.forward(*input, **kwargs)
        
        if training_mode:
            self.train.train()
        
        return adv_imgs
        