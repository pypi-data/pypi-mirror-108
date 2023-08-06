# MIT License
#
# Copyright (c) 2021 Soohwan Kim and Sangchun Ha and Soyoung Cho
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from dataclasses import dataclass, field

from openspeech.dataclass.configurations import OpenspeechDataclass


@dataclass
class TransformerWithCTCConfigs(OpenspeechDataclass):
    r"""
    This is the configuration class to store the configuration of
    a :class:`~openspeech.models.TransformerWithCTC`.

    It is used to initiated an `TransformerWithCTC` model.

    Configuration objects inherit from :class: `~openspeech.dataclass.configs.OpenspeechDataclass`.

    Configurations:
        model_name (str): Model name (default: transformer_with_ctc)
        extractor (str): The CNN feature extractor. (default: vgg)
        d_model (int): Dimension of model. (default: 512)
        d_ff (int): Dimenstion of feed forward network. (default: 2048)
        num_attention_heads (int): The number of attention heads. (default: 8)
        num_encoder_layers (int): The number of encoder layers. (default: 12)
        encoder_dropout_p (float): The dropout probability of encoder. (default: 0.3)
        ffnet_style (str): Style of feed forward network. (ff, conv) (default: ff)
        optimizer (str): Optimizer for training. (default: adam)
    """
    model_name: str = field(
        default="transformer_with_ctc", metadata={"help": "Model name"}
    )
    d_model: int = field(
        default=512, metadata={"help": "Dimension of model."}
    )
    d_ff: int = field(
        default=2048, metadata={"help": "Dimenstion of feed forward network."}
    )
    num_attention_heads: int = field(
        default=8, metadata={"help": "The number of attention heads."}
    )
    num_encoder_layers: int = field(
        default=12, metadata={"help": "The number of encoder layers."}
    )
    encoder_dropout_p: float = field(
        default=0.3, metadata={"help": "The dropout probability of encoder."}
    )
    ffnet_style: str = field(
        default="ff", metadata={"help": "Style of feed forward network. (ff, conv)"}
    )
    optimizer: str = field(
        default="adam", metadata={"help": "Optimizer for training."}
    )
