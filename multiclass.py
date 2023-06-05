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
        # bin = np.frombuffer(eval.binary, dtype=np.uint8)
        # bin = np.unpackbits(bin, axis=0).astype(np.single)
        bin = fen_to_vec(eval.fen).astype(np.single)
        eval.eval = np.sign(eval.eval) + 1 # good for black, even, good for white
        ev = np.array([eval.eval]).astype(np.single)
        return {'binary': bin, 'eval': ev}

class LinearModel(pl.LightningModule):
    def __init__(self, learning_rate=1e-4, batch_size=1024):
        super().__init__()
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.model = nn.Linear(773, 3)
    
    def forward(self, x):
        return self.model(x)

    def training_step(self, batch):
        x, y = batch['binary'], batch['eval']
        y = torch.flatten(y).long()
        # print(y)
        logits = self(x)
        # print(logits)
        loss = F.cross_entropy(logits, y)
        self.log("loss", loss, prog_bar=True)
        # print(loss)
        return loss
    
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.learning_rate)
    
    def train_dataloader(self):
        dataset = EvaluationDataset(count=LABEL_COUNT)
        return DataLoader(dataset, batch_size=self.batch_size, num_workers=8, pin_memory=True)
        # return DataLoader(dataset, batch_size=self.batch_size, num_workers=8)

def main():
    db.connect()
    pl.seed_everything(42, workers=True)
    trainer = pl.Trainer(devices="auto", accelerator="auto", precision="16-mixed", max_epochs=1, log_every_n_steps=200)
    # trainer = pl.Trainer(max_epochs=1)
    model = LinearModel()
    trainer.fit(model)

if __name__ == "__main__":
    main()
