# Description
Memory Wrap is an extension to image classification models that improves both data-efficiency and model interpretability, adopting a sparse content-attention mechanism between the input and some memories of past training samples.

# Installation
This is a PyTorch implementation of Memory Wrap. To install Memory Wrap run the following command:
```
pip install memorywrap
```

The library contains two main classes:
- *MemoryWrapLayer*: it is the Memory Wrap variant described in the paper that uses both the input encoding and the memory encoding to compute the output;
- *BaselineMemory*: it is the baseline that uses only the memory encoding to compute the output.

# Usage
## Instantiate the layer
```python
memorywrap = MemoryWrapLayer(encoder_dim,output_dim,return_weights=False)
```
or
```python
memorywrap = BaselineMemory(encoder_dim,output_dim)
```
where:
- *encoder_dim* is the output dimension of the last layer of the encoder 
- *output_dim* is the desired output dimensione. In the case of the paper *output_dim* is equal to the **number of classes**;
- *return_weights* is a flag telling to the layer if it has to return the sparse content weights.

## Forward call
Add the forward call to your forward function.
```python
output_memorywrap = memorywrap(input_encoding,memory_encoding)
```
where *input_encoding* and *memory_encoding* are the outputs of the the encoder of rispectively the current input and the memory set. <br>
If you have set the flag *return_weights* to True, then *output_memorywrap* is a Tuple where the first element is the output and the second one are the content weights associated to each element in the memory_encoding.

# Additional information
Here you can find link to additional source of information about Memory Wrap:
- <a href="https://arxiv.org/abs/2106.01440">Paper</a>
- <a href="">GitHub repo</a>
- <a href="https://colab.research.google.com/drive/1OPjcpTH7X8EV1ev361iuhVzd2Jfp9kFA">Jupyter notebook</a>