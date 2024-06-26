# https://github.com/lucidrains/linformer
# MIT License

# Copyright (c) 2020 Phil Wang

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import torch
import torch.nn as nn
import math

class LinformerAttention(nn.Module):
    projection_matrix = None

    def __init__(self, config):
        super().__init__()

        self.num_head = config["num_head"]
        self.head_dim = config["head_dim"]
        self.linformer_k = config["linformer_k"]
        self.seq_len = config["max_seq_len"]
        self.device = config['device'] if 'device' in config else 'cuda'

        # TODO modified into the upper two lines for run_norm
        self.E = nn.Parameter(torch.Tensor(self.num_head, self.linformer_k, self.seq_len)).to(self.device)
        torch.nn.init.normal_(self.E, std = 0.02)


        # if LinformerAttention.projection_matrix is not None:
        #     self.E = LinformerAttention.projection_matrix
        # else:
        #     LinformerAttention.projection_matrix = nn.Parameter(torch.Tensor(self.num_head, self.linformer_k, self.seq_len))
        #     torch.nn.init.normal_(LinformerAttention.projection_matrix, std = 0.02)
        #     self.E = LinformerAttention.projection_matrix

    def forward(self, Q, K, V, mask):
        K = torch.matmul(self.E, K * mask[:, None, :, None])
        V = torch.matmul(self.E, V * mask[:, None, :, None])

        dot = torch.matmul(Q, torch.transpose(K, -2, -1))
        dot = dot / math.sqrt(self.head_dim)

        attn = nn.functional.softmax(dot, dim = -1)

        X = torch.matmul(attn, V)

        return X

    def extra_repr(self):
        return f'linformer_k={self.linformer_k}'
