from .pandm import *
import torch
import pandas
import json
import numpy as np
from transformers import BertForSequenceClassification
from sklearn.metrics import matthews_corrcoef, f1_score, precision_recall_fscore_support
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler

from .config import model_location
from .getmodel import Download
from pathlib import Path
import os
import operator

class Tagger:
    def __init__(self, dialogue_path, model_name):
        self._model_name = model_name
        self._dialogue_path = dialogue_path
        self._lib_path = f"{str(Path.home())}" + model_location["MODEL"]
        self._model_path = os.path.join(self._lib_path, self._model_name)

        # Download model if not stored locally
        path_exists = os.path.exists(self._model_path)
        if (path_exists):
            print(f"Model '{self._model_name}' found in cache. Loading model...")
        else:
            print(f"Model '{self._model_name}' not found in cache. Downloading...") 
            self._model_file = Download(self._model_name)
            self._model_file.download_file()
    
    def getDialogActTags(self):
        predictions = self.__predict_acts()
        DAPreds = list(map(NumbertoJsonTag,predictions))
        
        with open(self._dialogue_path) as f:
            data = json.load(f)
            
            for turn,da in zip(data['turns'], DAPreds):
                turn["dialog_act"] = da
            
            print(predictions)

        filename = os.path.basename(self._dialogue_path).split('.')[0]
        dirname = os.path.dirname(self._dialogue_path)
        
        with open(os.path.join(dirname,filename+"_DAtag.json"), "w") as f:
            json.dump(data, f, indent=4)

    # this method is private
    def __predict_acts(self):
        filetype = ''
        if (self._dialogue_path.endswith('.csv')):
            filetype = 'csv'
            print("ERROR: Only .json is supported at this time")
            quit()
        elif (self._dialogue_path.endswith('.json')):
            filetype = 'json'
        else:
            print("ERROR: Invalid File Type, please examine your typing.")
            exit()
        print("Running GPU Check")
        #Check if CUDA is running, and set the device accordingly
        cudacheck = torch.cuda.is_available()
        if (cudacheck):
            # Tell PyTorch to use the GPU.
            device = torch.device("cuda")
            print('There are %d GPU(s) available.' % torch.cuda.device_count())
            print('We will use the GPU:', torch.cuda.get_device_name(0)) # If not...
        else:
            print('No GPU available, using the CPU instead.')
            device = torch.device("cpu")
        #Check if CUDA is running, and load the weights accordingly.
        if (cudacheck):
            model_state_dict = torch.load(self._model_path)
        else:
            model_state_dict = torch.load(self._model_path, map_location=torch.device('cpu'))
        model = BertForSequenceClassification.from_pretrained(
            "bert-base-uncased", # Use the 12-layer BERT model, with an uncased vocab.
            num_labels=14, # The number of output labels--2 for binary classification.
            # You can increase this for multi-class tasks.
            output_attentions=False, # Whether the model returns attentions weights.
            output_hidden_states=False, #Whether the model returns all hidden-states.
            state_dict=model_state_dict
        )
        # model.save_pretrained("pretrained") #!not needed
        #Last CUDA check, check if the GPU is available and set up the stream.
        if (cudacheck):
            model.to("gpu")
        else:
            model.to("cpu")
        # Load file into Dataframe
        if filetype == 'csv':
            testdata = pandas.read_csv(self._dialogue_path)
        if filetype == 'json':
            with open(self._dialogue_path) as f:
                data = json.load(f)
            # print(data)
            allturns = data['turns']
            df = pandas.DataFrame(columns=['Text'])
            for i in allturns:
                df = df.append({'Text': i['text']}, ignore_index=True)
            testdata = df

        testing = padandmask(testdata, 2)
        test_inputs = testing[0]
        test_masks = testing[1]
        test_inputs = torch.tensor(test_inputs)
        test_masks = torch.tensor(test_masks)
        batch_size = 32
        testing_data = TensorDataset(test_inputs, test_masks)
        testing_sampler = SequentialSampler(testing_data)
        testing_loader = DataLoader(testing_data, sampler=testing_sampler, batch_size=batch_size)
        print('Number of testing utterances: {:,}'.format(testdata.shape[0]))
        print('Beginning Predictions')
        labels = []
        # Predict
        model.eval()
        for batch in testing_loader:
            # Add batch to GPU
            batch = tuple(t.to(device) for t in batch)
            # Unpack the inputs from our dataloader
            b_input_ids, b_input_mask = batch
            # Telling the model not to compute or store gradients, saving memory and speeding up prediction
            with torch.no_grad():
                # Forward pass, calculate logit predictions
                outputs = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask)
            # Move logits and labels to CPU
            logits = outputs[0]
            logits = logits.detach().cpu().numpy()
            # Store predictions
            labels.append(logits)
        print("Predictions Complete")
        # Remember, the predictions are held in batches.
        # Flatten the predictions
        flat_predictions = [item for sublist in labels for item in sublist]
        flat_predictions = np.argmax(flat_predictions, axis=1).flatten()
        return flat_predictions

    
