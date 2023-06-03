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
from collections import OrderedDict

db = SqliteDatabase('2021-07-31-lichess-evaluations-37MM.db')
LABEL_COUNT = 37164639

class Evaluations(Model):
    def __init__(self):
        self.id = IntegerField()
        self.fen = TextField()
        self.binary = BlobField()
        self.eval = FloatField()

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
        bin = np.frombuffer(eval.binary, dtype=np.uint8)
        bin = np.unpackbits(bin, axis=0).astype(np.single)
        eval.eval = np.sign(eval) # good for black, even, good for white
        ev = np.array([eval.eval]).astype(np.single)
        return {'binary': bin, 'eval': ev}

class EvaluationModel(pl.LightningModule):
    def __init__(self, learning_rate=1e-3, batch_size=1024):
        super().__init__()
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.model = nn.Linear(808, 3)
    
    def forward(self, x):
        return self.model(x)

    def training_step(self, batch):
        x, y = batch['binary'], batch['eval']
        print(y)
        logits = self(x)
        y_hat = np.argmax(logits) - 1
        print(y_hat)
        loss = F.cross_entropy(y_hat, y)
        print(loss)
        raise("stop for debug")
        return loss
    
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.learning_rate)
    
    def train_dataloader(self):
        dataset = EvaluationDataset(count=LABEL_COUNT)
        return DataLoader(dataset, batch_size=self.batch_size, num_workers=2, pin_memory=True)

def main():
    db.connect()
    trainer = pl.Trainer(gpus=1, precision=16, max_epochs=1, auto_lr_find=True)
    model = EvaluationModel()
    trainer.fit(model)