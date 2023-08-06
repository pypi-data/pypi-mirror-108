import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import keras


class TransparentAI:
    def __init__(self, model, data, labels):
        self.model = model
        self.data = data
        self.labels = labels

    def preprocess(self):
        pass

    def explain_instance(self, explainer):
        pass
