"""
FILE: multiclass.py
Author: Michelle Fu
Contains a multiclass classifier for chess position evaluation. 
Attributions: tutorial for data handling and training here: https://towardsdatascience.com/train-your-own-chess-ai-66b9ca8d71e4
"""
from peewee import *
import base64
import os
import torch
import numpy as np
from torch import nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, IterableDataset, random_split
import pytorch_lightning as pl
from random import randrange
from process_data import fen_to_vec
from collections import OrderedDict

db = SqliteDatabase('2021-07-31-lichess-evaluations-37MM.db')
LABEL_COUNT = 37164639

class Evaluations(Model):
    id = IntegerField()
    fen = TextField()
    binary = BlobField()
    eval = FloatField()

    class Meta:
        database = db 
    
    def binary_base64(self):
        return base64.b64encode(self.binary)

class EvaluationDataset(IterableDataset):
    def __init__(self, count):
        self.count = count
    
    def __iter__(self):
        return self

    def __next__(self):
        idx = randrange(self.count)
        return self[idx]
    
    def __len__(self):
        return self.count

    def __getitem__(self, idx):
        eval = Evaluations.get(Evaluations.id == idx+1)
        bin = fen_to_vec(eval.fen).astype(np.single)
        eval.eval =  max(eval.eval, -15) # bounding evaluation to be between -15 and 15
        eval.eval = min(eval.eval, 15)
        ev = np.array([eval.eval]).astype(np.single)
        return {'binary': bin, 'eval': ev}

class DeepModel(pl.LightningModule):
    def __init__(self, learning_rate=1e-3, batch_size=1024, layer_count=6):
        super().__init__()
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        layers = []
        for i in range(layer_count - 1):
            layers.append((f"linear-{i}", nn.Linear(773, 773)))
            layers.append((f"relu-{i}", nn.ReLU()))
        layers.append((f"linear-{layer_count-1}", nn.Linear(773, 1)))
        self.seq = nn.Sequential(OrderedDict(layers))
    
    def forward(self, x):
        return self.seq(x)

    def training_step(self, batch):
        x, y = batch['binary'], batch['eval']
        logits = self(x)
        loss = F.l1_loss(logits, y)
        self.log("loss", loss, prog_bar=True)
        return loss
    
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.learning_rate)
    
    def train_dataloader(self):
        dataset = EvaluationDataset(count=LABEL_COUNT)
        return DataLoader(dataset, batch_size=self.batch_size, num_workers=8, pin_memory=True)

def main():
    db.connect()
    torch.set_float32_matmul_precision('medium' | 'high')
    pl.seed_everything(42, workers=True)
    trainer = pl.Trainer(devices="auto", accelerator="auto", precision="16-mixed", max_epochs=1, log_every_n_steps=200)
    model = DeepModel()
    trainer.fit(model)

if __name__ == "__main__":
    main()