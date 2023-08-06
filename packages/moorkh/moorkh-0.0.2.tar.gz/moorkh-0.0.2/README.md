# moorkh : Adversarial Attacks in Pytorch

**moorkh** is a Pytorch library for generating adversarial examples with full support for batches of images in all attacks.

## About the name

The name moorkh is a Hindi word meaning Fool in English, that's what we are making to Neural networks by generating advesarial examples. Although we also do so for making them more robust.

## Usage

### Installation

- `pip install moorkh` or
- `git clone https://github.com/akshay-gupta123/moorkh`

```python
import moorkh
norm_layer = moorkh.Normalize(mean,std)
model = nn.Sequential(
    norm_layer,
    model
)
model.eval()
attak = moorkh.FGSM(model)
adversarial_images = attack(images, labels)
```
## Implemented Attacks

* **[`EXPLAINING AND HARNESSING ADVERSARIAL EXAMPLES: FGSM`](https://arxiv.org/abs/1412.6572)**
* **[`ADVERSARIAL EXAMPLES IN THE PHYSICAL WORLD: IFGSM`](https://arxiv.org/abs/1607.02533)**
* **[`ON THE LIMITATION OF CONVULATIONSAL NEURAL NETWORK IN RECOGNIZING NEGATIVE IMAGES: Semantic`](https://arxiv.org/abs/1703.06857)**
* **[`ADDING NOISE: Noise`](https://arxiv.org/abs/1802.00420)**
* **[`TOWARDS DEEP LEARNING MODELS RESISTANT TO ADVERSARIAL ATTACKS: PGD\L2`](https://arxiv.org/abs/1706.06083)**
* **[`ESEMBLE ADVERSAIAL TRAINING: ATTACKS and DEFENSE: RFGSM`](https://arxiv.org/abs/1705.07204)**

## To-Do's
  * Adding more Attacks
  * Making Documentation
  * Adding demo notebooks
  * Adding Summaries of Implemented papers(for my own undestanding)

## Contribution

This library is developed as a part of my learning, if you find any **bug** feel free to create a PR. All kind of contributions are always welcome! 

##  References

* [Adversarial=Robustness-Toolbox](https://github.com/IBM/adversarial-robustness-toolbox) by IBM.
* [Foolbox](https://github.com/bethgelab/foolbox) by Bethgelab.
* [Cleverhans](https://github.com/tensorflow/cleverhans) by Google brain
* [Reliable and Interpretable Artificial Intelligence](https://www.sri.inf.ethz.ch/teaching/riai2020) A Eth Zurich course
* [Adversarial Robustness - Theory and Practice](https://adversarial-ml-tutorial.org/) Tutorial by Zico Kolter and Aleksander Madry