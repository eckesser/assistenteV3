# import sys
# import os

# root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(root_directory)

# import torch.nn as nn

# class SimpleRNN(nn.Module):
#     def __init__(self, input_size, hidden_size, output_size):
#         super(SimpleRNN, self).__init__()
#         self.hidden_size = hidden_size
#         self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
#         self.fc = nn.Linear(hidden_size, output_size)

#     def forward(self, x):
#         out, _ = self.rnn(x)
#         out = self.fc(out[:, -1, :])  # Saída apenas do último passo de tempo
#         return out