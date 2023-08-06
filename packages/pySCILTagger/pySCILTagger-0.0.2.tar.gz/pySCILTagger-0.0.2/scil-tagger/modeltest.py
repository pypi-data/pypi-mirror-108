'''
FOR TESTING
'''

#from utilities import *
from pandm import *
import torch
import pandas
import json
import numpy as np
from transformers import BertForSequenceClassification
from sklearn.metrics import matthews_corrcoef, f1_score, precision_recall_fscore_support
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler

#Test takes a .pt Model path and then either a JSON or a CSV as the filepath.
def test(modelpath, path):
    filetype = ''
    if path.endswith('.csv'):
        filetype = 'csv'
    elif path.endswith('.json'):
        filetype = 'json'
    else:
        print("Invalid File Type, please examine your typing.")
        exit()
    print("Running GPU Check")
    #Check if Cuda is running, and set the device accordingly
    cudacheck = torch.cuda.is_available()
    if cudacheck:
        # Tell PyTorch to use the GPU.
        device = torch.device("cuda")
        print('There are %d GPU(s) available.' % torch.cuda.device_count())
        print('We will use the GPU:', torch.cuda.get_device_name(0))  # If not...
    else:
        print('No GPU available, using the CPU instead.')
        device = torch.device("cpu")
    PATH = modelpath
    #Check if cuda is Running, and load the weights accordingly.
    if(cudacheck):
        model_state_dict = torch.load(PATH)
    else:
        model_state_dict = torch.load(PATH, map_location=torch.device('cpu'))
    model = BertForSequenceClassification.from_pretrained(
        "bert-base-uncased",  # Use the 12-layer BERT model, with an uncased vocab.
        num_labels=14,  # The number of output labels--2 for binary classification.
        # You can increase this for multi-class tasks.
        output_attentions=False,  # Whether the model returns attentions weights.
        output_hidden_states=False,  # Whether the model returns all hidden-states.
        state_dict=model_state_dict
    )
    model.save_pretrained("pretrained")
    #Last Cuda check, check if the GPU is available and set up the stream.
    if(cudacheck):
        model.to("gpu")
    else:
        model.to("cpu")
    #Load File into Dataframe.
    if filetype == 'csv':
        testdata = pandas.read_csv(path)
        test_labels_str = testdata['DamslActTag']
        test_labels = list(map(JsonTagtoNumber, test_labels_str))
    if filetype == 'json':
        with open(path) as f:
            data = json.load(f)
        # print(data)
        allturns = data['turns']
        df = pandas.DataFrame(columns=['DamslActTag', 'Text'])
        for i in allturns:
            df = df.append({'Text': i['text'], 'DamslActTag':i['dialog_act']}, ignore_index=True)
        testdata = df
        test_labels_str = testdata['DamslActTag']
        test_labels = list(map(JsonTagtoNumber, test_labels_str))
    testing = padandmask(testdata, 2)
    test_inputs = testing[0]
    test_masks = testing[1]
    test_inputs = torch.tensor(test_inputs)
    test_labels = torch.tensor(test_labels)
    test_masks = torch.tensor(test_masks)
    batch_size = 32
    testing_data = TensorDataset(test_inputs, test_masks, test_labels)
    testing_sampler = SequentialSampler(testing_data)
    testing_loader = DataLoader(testing_data, sampler=testing_sampler, batch_size=batch_size)
    print('Number of testing utterances: {:,}'.format(testdata.shape[0]))
    print('Beginning Predictions')
    tests, true_labels = [], []
    # Predict
    model.eval()
    for batch in testing_loader:
        # Add batch to GPU
        batch = tuple(t.to(device) for t in batch)
        # Unpack the inputs from our dataloader
        b_input_ids, b_input_mask, b_labels = batch
        # Telling the model not to compute or store gradients, saving memory and speeding up prediction
        with torch.no_grad():
            # Forward pass, calculate logit predictions
            outputs = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask)
        # Move logits and labels to CPU
        logits = outputs[0]
        logits = logits.detach().cpu().numpy()
        label_ids = b_labels.to('cpu').numpy()
        # Store predictions and true labels
        tests.append(logits)
        true_labels.append(label_ids)
    print("Predictions Complete")
    matthews_set = []
    for i in range(len(true_labels)):
        matthews = matthews_corrcoef(true_labels[i],
            np.argmax(tests[i], axis=1).flatten())
        matthews_set.append(matthews)
    # Remember, the predictions are held in batches.
    # Flatten the predictions and true values for aggregate Matthew's evaluation on the whole dataset
    flat_predictions = [item for sublist in tests for item in sublist]
    flat_predictions = np.argmax(flat_predictions, axis=1).flatten()
    flat_true_labels = [item for sublist in true_labels for item in sublist]
    print('Classification accuracy using BERT Fine Tuning: {0:0.2%}'.format(
        matthews_corrcoef(flat_true_labels, flat_predictions)))
    fscore = precision_recall_fscore_support(flat_true_labels, flat_predictions, average=None)
    print("These are our true labels", flat_true_labels)
    print("These are our predictions", flat_predictions)
    k = 0
    #for i in fscore:
    #    print(k,":",i)
    #    k += 1
    #print("This is fscore", fscore)
    print("Returning predictions")
    return flat_predictions

def testonall(modelname):
    test(modelname, 'GT/YMCA_gt.json')
    test(modelname, 'GT/Cheney_gt.json')
    test(modelname, 'GT/Feb13_GroupA_gt.json')
    test(modelname, 'GT/Feb13_GroupB_gt.json')
    test(modelname, 'GT/Feb19_GroupB_gt.json')
    test(modelname, 'GT/Mar11_GroupB_gt.json')
    test(modelname, 'GT/Training_gt.json')

if __name__ == '__main__':
    testonall('selected.pt')
