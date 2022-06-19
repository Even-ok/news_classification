
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import torch.optim as optim

class TextBiLSTMAttention(nn.Module):
    def __init__(self):
         
        self.embedding_pretrained = None                                   
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')   

        self.dropout = 0.5                                              
        self.require_improvement = 1000                                 
        self.num_classes = 2                         
        self.n_vocab = 0                                                                                    
        self.pad_size = 32                                              
        self.learning_rate = 1e-3                                       
        self.embed = self.embedding_pretrained.size(1)\
            if self.embedding_pretrained is not None else 300           
        self.hidden_size = 128                                          
        self.num_layers = 2                                             
        self.hidden_size2 = 64

        if self.embedding_pretrained is not None:
            self.embedding = nn.Embedding.from_pretrained(self.embedding_pretrained, freeze=False)
        else:
            self.embedding = nn.Embedding(self.n_vocab, self.embed, padding_idx=self.n_vocab - 1)
        self.lstm = nn.LSTM(self.embed, self.hidden_size, self.num_layers,
                            bidirectional=True, batch_first=True, dropout=self.dropout)
        self.tanh1 = nn.Tanh()
        
        self.w = nn.Parameter(torch.zeros(self.hidden_size * 2))
        self.tanh2 = nn.Tanh()
        self.fc1 = nn.Linear(self.hidden_size * 2, self.hidden_size2)
        self.fc = nn.Linear(self.hidden_size2, self.num_classes)

    def forward(self, x):
        x, _ = x
        emb = self.embedding(x)  
        H, _ = self.lstm(emb)  
        M = self.tanh1(H)  
        alpha = F.softmax(torch.matmul(M, self.w), dim=1).unsqueeze(-1)  
        out = H * alpha  
        out = torch.sum(out, 1)  
        out = F.relu(out)
        out = self.fc1(out)
        out = self.fc(out)  
        return out

model = TextBiLSTMAttention()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training
for epoch in range(5000):
    optimizer.zero_grad()
    output = model(input_batch)

    # output : [batch_size, num_classes], target_batch : [batch_size] (LongTensor, not one-hot)
    loss = criterion(output, target_batch)
    if (epoch + 1) % 1000 == 0:
        print('Epoch:', '%04d' % (epoch + 1), 'cost =', '{:.6f}'.format(loss))

    loss.backward()
    optimizer.step()

