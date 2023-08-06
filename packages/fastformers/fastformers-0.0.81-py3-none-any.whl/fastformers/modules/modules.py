import torch
from torch.nn import Module, Linear
from torch.nn.functional import gelu


class TransformerFFN(Module):
    def __init__(self, dim: int, dim_hidden: int):
        super(TransformerFFN, self).__init__()
        self.lin1 = Linear(dim, dim_hidden)
        self.lin2 = Linear(dim_hidden, dim)

    def forward(self, tensor: torch.Tensor) -> torch.Tensor:
        tensor = self.lin1(tensor)
        tensor = gelu(tensor)
        tensor = self.lin2(tensor)
        return tensor


class TanhHead(Module):
    """Head for sentence-level classification tasks."""

    def __init__(self, input_dim: int, inner_dim: int, num_classes: int):
        super().__init__()
        self.dense = Linear(input_dim, inner_dim)
        self.out_proj = Linear(inner_dim, num_classes)

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        hidden_states = self.dense(hidden_states)
        hidden_states = torch.tanh(hidden_states)
        return self.out_proj(hidden_states)
