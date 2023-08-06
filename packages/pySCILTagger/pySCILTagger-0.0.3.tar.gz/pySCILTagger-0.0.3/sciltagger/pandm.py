import re
from .labelconvert import *
from keras.preprocessing.sequence import pad_sequences
from transformers import BertTokenizer
import csv

def translator(user_string):
    user_string = user_string.split(" ")
    j = 0
    for _str in user_string:
        # File path which consists of Abbreviations.
        fileName = "slang.txt"
        # File Access mode [Read Mode]
        accessMode = "r"
        with open(fileName, accessMode) as myCSVfile:
            # Reading file as CSV with delimiter as "=", so that abbreviation are stored in row[0] and phrases in row[1]
            dataFromFile = csv.reader(myCSVfile, delimiter="=")
            # Removing Special Characters.
            #_str = re.sub('[^a-zA-Z0-9-_.]', '', _str)
            for row in dataFromFile:
                # Check if selected word matches short forms[LHS] in text file.
                if _str.upper() == row[0]:
                    # If match found replace it with its Abbreviation in text file.
                    user_string[j] = row[1]
            myCSVfile.close()
        j = j + 1
    # Replacing commas with spaces for final output.
    print(' '.join(user_string))
    return user_string


#This is used for context. It creates sequences out of all of listin but the last.
def appendbeginning(listin):
    output = ""
    for i in range(len(listin) - 1):
        if i != 0:
            output += ' '
        output += listin[i]
    return output
'''
def endcheckfor2orless(lis):
    #print("Lis before endcheck")
    if 'END' in lis and 'BEGIN' in lis:
        #print("Both found")
        lis.remove('END')
        lis.remove('BEGIN')
    elif 'END' in lis:
        index = lis.index('END')
        lis = lis[0:index]
    elif 'BEGIN' in lis:
        index = lis.index('BEGIN')
        lis = lis[index:len(lis)-1]
    #print("Lis after endcheck", lis)
    return lis
'''



# This is custom built for SwDa. It removes anything in <> type of brackets.
def remove_tags(input):
    re.sub('<[^>]+>', '', input)
    return input


# This is our regex preprocessor. It remove most special characters.
def preprocess(sen):
    # print("Preprocess input is", sen)
    output = []
    for sentence in sen:
        sentence = remove_tags(sentence)
        # removing
        sentence = re.sub('[^a-zA-Z]', ' ', sentence)
        # Removing single character
        sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)
        # Removing multiple spaces
        sentence = re.sub(r'\s+', ' ', sentence)
        output.append(sentence)
    return output
'''
def contextmask(input, numsent):
    print("Padding and Masking with Context-Pointer model")
    lim = 0
    tokenizer = BertTokenizer.from_pretrained('roberta-base')
    utterances = []
    sentences = list(input['Text'])
    context = list(input['Context'])
    labels = list(input['DamslActTag'])
    k = 0
    for i in range(len(sentences)):
        if(labels[i] == -1 or labels[i] == '-1'):
            print("Sentence", sentences[i], "Labels", labels[i])


        #print("I is", sentences[i])

        # print(sen)
        # print("In loop, at i", i, sentences[i], "length is", numsent)
        # print(sentences[i:(numsent+i+1)])
        print("Sentences:", sentences[i:numsent+i+1], "context",   context[k])
        ourlist = preprocess(sentences[i:(numsent + i + 1)])
        sent1 = context[k]
        sent2 = ourlist[0]
        utterances.append((sent1, sent2))
        k += 1
    # Decently short
    # for i in utterances:
    #    print(i)
    print("Encoding and Truncating, this will take a minute.")
    print("--------------------------------------------------")
    # Tokenize all of the sentences and map the tokens to their word IDs.
    input_ids = []  # For every sentence...
    for sent in utterances:
        # `encode` will:
        #   (1) Tokenize the sentence.
        #   (2) Prepend the `[CLS]` token to the start.
        #   (3) Append the `[SEP]` token to the end. #SEP is especially important for our dialog act tagger.
        #   (4) Map tokens to their IDs.
        encoded_sent = tokenizer.encode(
            sent[0], sent[1],  # Sentence to encode.
            add_special_tokens=True,
            # Add '[CLS]' and '[SEP]'                        # This function also supports truncation and conversion
            # to pytorch tensors, but we need to do padding, so we
            # can't use these features :( .
            # max_length = 128,          # Truncate all sentences.
            # return_tensors = 'pt',     # Return pytorch tensors.
        )
        # Add the encoded sentence to the list.
        input_ids.append(encoded_sent)
    # Determine max length
    print('Max sentence length: ', max([len(k) for k in input_ids]))
    # max sentence length is 82, so our padding goal is 128.
    MAX_LEN = 200
    print('\nPadding/truncating all sentences to %d values...' % MAX_LEN)
    print('\nPadding token: "{:}", ID: {:}'.format(tokenizer.pad_token, tokenizer.pad_token_id))
    input_ids = pad_sequences(input_ids,
                              maxlen=MAX_LEN,
                              dtype="long",
                              value=0,
                              truncating="post",
                              padding="post")
    print('\Done.')
    attention_masks = []  # For each sentence...
    for sent in input_ids:
        # Create the attention mask.
        #   - If a token ID is 0, then it's padding, set the mask to 0.
        #   - If a token ID is > 0, then it's a real token, set the mask to 1.
        att_mask = [int(token_id > 0) for token_id in sent]

        # Store the attention mask for this sentence.
        attention_masks.append(att_mask)

    return (input_ids, attention_masks)

    #translator()
    #cont
    #if contextfile:
    #    print("Grabbing Data from Context")
    #    train_context =
    #    validation_labels =
    '''

def padandmask(input, numsent):
    lim = 0
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    utterances = []
    sentences = list(input['Text'])
    for i in range(len(sentences)):


        #print("I is", sentences[i])

        # print(sen)
        # print("In loop, at i", i, sentences[i], "length is", numsent)
        # print(sentences[i:(numsent+i+1)])
        ourlist = preprocess(sentences[i:(numsent + i + 1)])
        #print("Uncheckedlist", uncheckedlist)
        #if 'END' in uncheckedlist and 'BEGIN' in uncheckedlist:
        #    print("Both found")
        #    continue


        #if uncheckedlist == ['END', 'BEGIN']:
        #    #print("Endbegin found")
        #    continue
        #ourlist = endcheckfor2orless(uncheckedlist)
        #print("Ourlist", ourlist)
        # print("OURLIST", ourlist)
        # input delete before end.
        if len(ourlist) == 1:
            sent1 = ""
            sent2 = ourlist[0]
        else:
            sent1 = appendbeginning(ourlist)
            sent2 = ourlist[len(ourlist) - 1]
        # print("sent1:", sent1, "sent2", sent2)
        utterances.append((sent1, sent2))
    # Decently short
    # for i in utterances:
    #    print(i)
    print("Encoding and Truncating, this will take a minute.")
    print("--------------------------------------------------")
    # Tokenize all of the sentences and map the tokens to their word IDs.
    input_ids = []  # For every sentence...
    for sent in utterances:
        # `encode` will:
        #   (1) Tokenize the sentence.
        #   (2) Prepend the `[CLS]` token to the start.
        #   (3) Append the `[SEP]` token to the end. #SEP is especially important for our dialog act tagger.
        #   (4) Map tokens to their IDs.
        encoded_sent = tokenizer.encode(
            sent[0], sent[1],  # Sentence to encode.
            add_special_tokens=True,
            # Add '[CLS]' and '[SEP]'                        # This function also supports truncation and conversion
            # to pytorch tensors, but we need to do padding, so we
            # can't use these features :( .
            # max_length = 128,          # Truncate all sentences.
            # return_tensors = 'pt',     # Return pytorch tensors.
        )
        # Add the encoded sentence to the list.
        input_ids.append(encoded_sent)
    # Determine max length
    print('Max sentence length: ', max([len(k) for k in input_ids]))
    # max sentence length is 82, so our padding goal is 128.
    MAX_LEN = 200
    print('\nPadding/truncating all sentences to %d values...' % MAX_LEN)
    print('\nPadding token: "{:}", ID: {:}'.format(tokenizer.pad_token, tokenizer.pad_token_id))
    input_ids = pad_sequences(input_ids,
                              maxlen=MAX_LEN,
                              dtype="long",
                              value=0,
                              truncating="post",
                              padding="post")
    print('\Done.')
    attention_masks = []  # For each sentence...
    for sent in input_ids:
        # Create the attention mask.
        #   - If a token ID is 0, then it's padding, set the mask to 0.
        #   - If a token ID is > 0, then it's a real token, set the mask to 1.
        att_mask = [int(token_id > 0) for token_id in sent]

        # Store the attention mask for this sentence.
        attention_masks.append(att_mask)

    return (input_ids, attention_masks)
