# Custom Deep Learning
* Create a customized Feedforward Neural Network by changing the number of layers, activation functions, loss function and optimizer.
* Refer to the documentation of any class/method by using help(class/method) Eg: help(FNN), help(FNN.compile)
* For intuitive explanations of the underlying theory refer:
   * [Feedforward Neural Network](https://github.com/Taarak9/DL-from-Scratch/blob/master/Feedforward%20Neural%20Network/README.md)
   * [Optimizers](https://github.com/Taarak9/DL-from-Scratch/blob/master/Optimizers/README.md)

## Installation
```bash
$ [sudo] pip3 install customdl
``` 
## Development Installation
```bash
$ git clone https://github.com/Taarak9/Custom-DL.git
```
## Usage
```python3
>>> from customdl import FNN
```
### Creating a Feedforward Neural Network
```python3
# number of input nodes
n_inputs = 27
loss_fn = "ce"
nn = FNN(n_inputs, loss_fn)

# Add a layer with 9 nodes and activation function ReLU
nn.add_layer(9, "relu")
# Add a layer with 3 nodes and activation function sigmoid
nn.add_layer(3, "sigmoid")

# Note the last layer you added will be the output layer of the NN
# Compile the nn
nn.compile(training_data, test_data)
```
* Available options:
    * Weight initialization: Random, Xavier, He 
    * Activation functions: Identity, Sigmoid, Softmax, Tanh, ReLU
    * Loss functions: MSE, Cross Entropy
    * Learning mode: online, mini-batch, batch
    * Optimizers: GD, Momentum based GD, Nesterov accerelated GD  
* Refer to the [Handwritten digit recognizer](https://github.com/Taarak9/Handwritten-Digit-Recognition/blob/main/src/FNN/hdr_fnn.ipynb) built using this package.

### To-do list
* [ ] Use validation data for hyperparameter tuning
* [ ] Plots for monitoring loss and accuracy over epochs
* [ ] Regularization techniques: L1, L2, dropout
* [ ] Add optimizers: Adam, RMSProp
* [ ] RBF NN
