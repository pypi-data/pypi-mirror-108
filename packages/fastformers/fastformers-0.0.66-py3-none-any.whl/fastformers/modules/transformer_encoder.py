import torch
from torch.nn import Module, ModuleList, LayerNorm

from .attention import MultiHeadAttention
from .modules import TransformerFFN


class TransformerEncoderLayer(Module):
    def __init__(self, n_heads: int, embedding_size: int, ffn_size: int, blender_norm: bool):
        super().__init__()
        self.attention = MultiHeadAttention(n_heads, embedding_size)
        self.norm1 = LayerNorm(embedding_size)

        self.ffn = TransformerFFN(embedding_size, ffn_size)
        self.norm2 = LayerNorm(embedding_size)

        self.blender_norm = blender_norm

    def forward(self, tensor: torch.Tensor, mask: torch.Tensor):
        residual = tensor
        if self.blender_norm:
            tensor = self.norm1(tensor)
        tensor = self.attention(tensor, mask=mask)[0]
        tensor = tensor + residual
        if not self.blender_norm:
            tensor = self.norm1(tensor)
        residual = tensor
        if self.blender_norm:
            tensor = self.norm2(tensor)
        tensor = self.ffn(tensor)
        tensor = tensor + residual
        if not self.blender_norm:
            tensor = self.norm2(tensor)
        return tensor


class TransformerEncoder(Module):
    def __init__(self, n_heads: int, n_layers: int, embedding_size: int, ffn_size: int, blender_norm: bool = False):
        super(TransformerEncoder, self).__init__()

        self.layers = ModuleList(
            TransformerEncoderLayer(n_heads, embedding_size, ffn_size, blender_norm) for _ in range(n_layers))
        self.n_heads = n_heads

    def forward(self, tensor: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        bsz, seq_len = mask.shape
        attn_mask = ~mask.view(bsz, 1, -1, seq_len).repeat(1, self.n_heads, 1, 1).expand(
            -1, -1, seq_len, -1).view(bsz * self.n_heads, seq_len, seq_len)

        for layer in self.layers:
            tensor = layer.forward(tensor, attn_mask)

        return tensor * mask.unsqueeze(-1)
