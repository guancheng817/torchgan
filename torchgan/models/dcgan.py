import torch.nn as nn
import torch.nn.functional as F
from .model import Generator, Discriminator
from math import ceil, log2

__all__ = ['DCGANGenerator', 'DCGANDiscriminator']

class DCGANGenerator(Generator):
    r"""Deep Convolutional GAN (DCGAN) generator from
    `"Unsupervised Representation Learning With Deep Convolutional Generative Aversarial Networks
    by Radford et. al. " <https://arxiv.org/abs/1511.06434>`_ paper

    Args:
        encoding_dims (int, optional) : Dimension of the encoding vector sampled from the noise prior. Default 100
        out_size      (int, optional) : Height and width of the input image to be generated. Must be at least 16
                                        and should be an exact power of 2. Defaults to 32
        out_channels (int, optional) : Number of channels in the output Tensor.
        step_channels (int, optional) : Number of channels in multiples of which the DCGAN steps up
                                        the convolutional features
                                        The step up is done as dim `z -> d - > 2 * d -> 4 * d - > 8 * d`
                                        where d = step_channels.
        batchnorm (bool, optional) : If True, use batch normalization in the convolutional layers of the generator.
        nonlinearity (torch.nn.Module, optional) : Nonlinearity to be used in the intermediate convolutional layers
                                                  Defaults to LeakyReLU(0.2) when None is passed.
        last_nonlinearity (torch.nn.Module, optional) : Nonlinearity to be used in the final convolutional layer
                                                       Defaults to tanh when None is passed.
    """
    def __init__(self, encoding_dims=100, out_size=32, out_channels=3, step_channels=64,
                 batchnorm=True, nonlinearity=None, last_nonlinearity=None, label_type='none'):
        super(DCGANGenerator, self).__init__(encoding_dims, label_type)
        if out_size < 16 or ceil(log2(out_size)) != log2(out_size):
            raise Exception('Target Image Size must be at least 16*16 and an exact power of 2')
        num_repeats = out_size.bit_length() - 4
        self.ch = out_channels
        self.n = step_channels
        use_bias = not batchnorm
        nl = nn.LeakyReLU(0.2) if nonlinearity is None else nonlinearity
        last_nl = nn.Tanh() if last_nonlinearity is None else last_nonlinearity
        model = []
        d = int(self.n * (2 ** num_repeats))
        if batchnorm is True:
            model.append(nn.Sequential(
                nn.ConvTranspose2d(self.encoding_dims, d, 4, 1, 0, bias=use_bias),
                nn.BatchNorm2d(d), nl))
            for i in range(num_repeats):
                model.append(nn.Sequential(
                    nn.ConvTranspose2d(d, d // 2, 4, 2, 1, bias=use_bias),
                    nn.BatchNorm2d(d // 2), nl))
                d = d // 2
        else:
            model.append(nn.Sequential(
                nn.ConvTranspose2d(self.encoding_dims, d, 4, 1, 0, bias=use_bias), nl))
            for i in range(num_repeats):
                model.append(nn.Sequential(
                    nn.ConvTranspose2d(d, d // 2, 4, 2, 1, bias=use_bias), nl))
                d = d // 2
        model.append(nn.Sequential(
            nn.ConvTranspose2d(d, self.ch, 4, 2, 1, bias=True), last_nl))
        self.model = nn.Sequential(*model)
        self._weight_initializer()

    def forward(self, x):
        x = x.view(-1, x.size(1), 1, 1)
        return self.model(x)


class DCGANDiscriminator(Discriminator):
    r"""Deep Convolutional GAN (DCGAN) discriminator from
    `"Unsupervised Representation Learning With Deep Convolutional Generative Aversarial Networks
    by Radford et. al. " <https://arxiv.org/abs/1511.06434>`_ paper

    Args:
        encoding_dims (int, optional) : Dimension of the encoding vector sampled from the noise prior.
        in_size (int, optional)       : Height and width of the input image. Must be greater than 16 and must be
                                        an exact power of 2. Default 32
        in_channels (int, optional) : Number of channels in the input Image.
        step_channels (int, optional) : Number of channels in multiples of which the DCGAN steps up
                                        the convolutional features
                                        The step up is done as dim `z -> d - > 2 * d -> 4 * d - > 8 * d`
                                        where d = step_channels.
        batchnorm (bool, optional) : If True, use batch normalization in the convolutional layers of the generator.
        nonlinearity (torch.nn.Module, optional) : Nonlinearity to be used in the intermediate convolutional layers
                                                  Defaults to LeakyReLU(0.2) when None is passed.
        last_nonlinearity (toch.nn.Module, optional) : Nonlinearity to be used in the final convolutional layer
                                                      Defaults to sigmoid when None is passed.
    """

    def __init__(self, in_size=32, in_channels=3, step_channels=64, batchnorm=True,
                 nonlinearity=None, last_nonlinearity=None, label_type='none'):
        super(DCGANDiscriminator, self).__init__(in_channels, label_type)
        if in_size < 16 or ceil(log2(in_size)) != log2(in_size):
            raise Exception('Input Image Size must be at least 16*16 and an exact power of 2')
        num_repeats = in_size.bit_length() - 4
        self.n = step_channels
        use_bias = not batchnorm
        nl = nn.LeakyReLU(0.2) if nonlinearity is None else nonlinearity
        last_nl = nn.LeakyReLU(0.2) if last_nonlinearity is None else last_nonlinearity
        d = self.n
        model = [nn.Sequential(
            nn.Conv2d(self.input_dims, d, 4, 2, 1, bias=True), nl)]
        if batchnorm is True:
            for i in range(num_repeats):
                model.append(nn.Sequential(
                    nn.Conv2d(d, d * 2, 4, 2, 1, bias=use_bias),
                    nn.BatchNorm2d(d * 2), nl))
                d *= 2
        else:
            for i in range(num_repeats):
                model.append(nn.Sequential(
                    nn.Conv2d(d, d * 2, 4, 2, 1, bias=use_bias), nl))
                d *= 2
        model.append(nn.Sequential(
            nn.Conv2d(d, 1, 4, 1, 0, bias=use_bias), last_nl))
        self.model = nn.Sequential(*model)
        self._weight_initializer()

    def forward(self, x):
        x = self.model(x)
        return x.view(x.size(0),)
