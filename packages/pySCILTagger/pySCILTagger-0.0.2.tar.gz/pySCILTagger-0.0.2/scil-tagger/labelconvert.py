#This file contains all of the conversions used between different tagsets.
#Lots of different utility functions here.



#A utiity function, it converts the SWDA strings into a number to be able to be used as a label for bert.
#If any strings are not found, they are printed with an example.
def SwDaConvert(stringinput):
    tagMap = {
        'sd':1,
        'b':2,
        'sv':3,
        'aa':4,
        '%':5,
        'ba':6,
        'qy':7,
        'ny':8,
        'fc':9,
        'qw':10,
        'nn':11,
        'bk':12,
        'h':13,
        'qy^d':14,
        'fo_o_fw_"_by_bc':15,
        'bh':16,
        '^q':17,
        'bf':18,
        'na':19,
        'ad':20,
        'b^m':21,
        'qo':22,
        'qh':23,
        '^h':24,
        'ar':25,
        'ng':26,
        'br':27,
        'no':28,
        'fp':29,
        'qrr':30,
        'arp_nd':31,
        'oo_co_cc':32,
        'bd':33,
        'aap_am':34,
        '^g':35,
        'qw^d':36,
        'fa':37,
        'ft':38,
        'x': 39,
        '^2':40,
        't3':41,
        't1':42,
        '+':43
    }
    if stringinput in tagMap.keys():
        stringoutput = tagMap[stringinput]
    else:
        #We Don't Want This.
        print("Stringinput not found", stringinput)
        #Default to Assertion-Opinion in case of emergency.
        stringoutput = 1
    return stringoutput - 1

def NumtoSwDa(intinput):
    intinput += 1
    tagMap = {
        1: 'sd',
        2: 'b',
        3: 'sv',
        4: 'aa',
        5: '%',
        6: 'ba',
        7: 'qy',
        8: 'ny',
        9: 'fc',
        10: 'qw',
        11: 'nn',
        12: 'bk',
        13: 'h',
        14: 'qy^d',
        15: 'fo_o_fw_"_by_bc',
        16: 'bh',
        17: '^q',
        18: 'bf',
        19: 'na',
        20: 'ad',
        21: 'b^m',
        22: 'qo',
        23:'qh',
        24:'^h',
        25:'ar',
        26:'ng',
        27:'br',
        28:'no',
        29:'fp',
        30:'qrr',
        31:'arp_nd',
        32:'oo_co_cc',
        33:'bd',
        34:'aap_am',
        35:'^g',
        36:'qw^d',
        37:'fa',
        38:'ft',
        39:'x',
        40:'^2',
        41:'t3',
        42:'t1',
        43:'+'
    }
    if intinput in tagMap.keys():
        stringoutput = tagMap[intinput]
    else:
        #We Don't Want This.
        print("Intinput not found", intinput)
        #Default to Assertion-Opinion in case of emergency.
        stringoutput = "sd"
    return stringoutput

def SwDatoDSARMD(stringinput):
    tagMap = {'sd': 'Assertion-Opinion', 'b': 'Acknowledge', 'sv': 'Assertion-Opinion',
              'aa': 'Agree-Accept', '%': 'Other-Conventional-Phrase', 'ba': 'Acknowledge',
              'qy': 'Confirmation-Request', 'ny': 'Response-Answer', 'fc': 'Conventional-Closing',
              'qw': 'Information-Request', 'nn': 'Response-Answer', 'bk': 'Acknowledge',
              'h': 'Response-Non-Answer', 'qy^d': 'Confirmation-Request',
              'fo_o_fw_"_by_bc': 'Other-Conventional-Phrase', 'bh': 'Confirmation-Request', '^q': 'Assertion-Opinion',
              'bf': 'Confirmation-Request', 'na': 'Response-Answer', 'ad': 'Action-Directive',
              'b^m': 'Assertion-Opinion', 'qo': 'Information-Request',
              'qh': 'Information-Request', '^h': 'Response-Non-Answer', 'ar': 'Disagree-Reject',
              'ng': 'Response-Answer', 'br': 'Signal-Non-Understanding',
              'no': 'Response-Non-Answer', 'fp': 'Conventional-Opening', 'qrr': 'Assertion-Opinion',
              'arp_nd': 'Response-Answer', 'oo_co_cc': 'Offer-Commit', 'bd': 'Other-Conventional-Phrase',
              'aap_am': 'Agree-Accept',
              '^g': 'Confirmation-Request', 'qw^d': 'Information-Request',
              'fa': 'Other-Conventional-Phrase', 'ft': 'Other-Conventional-Phrase'
    }
    if stringinput in tagMap.keys():
        stringoutput = tagMap[stringinput]
    else:
        #We Don't Want This.
        print("Stringinput not found SwDA2", stringinput)
        #Default to Assertion-Opinion in case of emergency.
        stringoutput = "Assertion-Opinion"
    return stringoutput


#Converts from switchboards standard to the DSARMD Standard. Input is a string, output is a string.
def SWfulltoDSARMD(stringinput):
    dict = {
        "Statement-non-opinion" : "Assertion-Opinion",
        "Statement-opinion" : "Assertion-Opinion",
        "Repeat-phrase" : "Assertion-Opinion",
        "Collaborative Completion" : "Assertion-Opinion",
        "Quotation" : "Assertion-Opinion",
        "Or-Clause" : "Assertion-Opinion",
        "Acknowledge (Backchannel)" :"Acknowledge",
        "Appreciation" :"Acknowledge",
        "Response Acknowledgement": "Acknowledge",
        "Maybe/Accept-Part" : "Agree-Accept",
        "Agree/Accept" : "Agree-Accept",
        "Yes Answers" : "Agree-Accept",
        "Dispreferred answers" : "Response-Answer",
        "Affirmative Non-yes Answers" : "Response-Answer",
        "Response" : "Response-Non-Answer",
        "Hold Before Answer/Agreement" : "Response-Non-Answer",
        "Hedge": "Response-Non-Answer",
        "Reject" : "Disagree-Reject",
        "Negative Non-no Answers" : "Disagree-Reject",
        "No Answers": "Disagree-Reject",
        "Conventional-opening":"Conventional-Opening",
        "Signal-non-understanding": "Signal-Non-Understanding",
        "Conventional-closing":"Conventional-Closing",
        "Wh-Question" : "Information-Request",
        "Declarative Yes-No-Question" : "Information-Request",
        "Yes-No-Question" : "Information-Request",
        "Open-Question" : "Information-Request",
        "Rhetorical-Question" : "Information-Request",
        "Tag-Question" : "Information-Request",
        "Summarize/Reformulate"  : "Confirmation-Request",
        "Backchannel in Question Form" : "Confirmation-Request",
        "Offers, Options Commits":"Offer-Commit",
        "Action-directive":"Action-Directive",
        "Abandoned"  : "Other-Conventional-Phrase",
        "Turn-exit"  : "Other-Conventional-Phrase",
        "Other"  : "Other-Conventional-Phrase",
        "Downplayer" : "Other-Conventional-Phrase",
        "Apology"  : "Other-Conventional-Phrase",
        "Other"  : "Other-Conventional-Phrase",
        "Thanking"  : "Other-Conventional-Phrase",
        "Non-Verbal" :"Delete Line",
        "Uninterpretable" : "Delete Line",
        "Self-talk" : "Delete Line" ,
        "3rd-Party Talk" : "Delete Line"
    }
    if stringinput in dict.keys():
        stringoutput = dict[stringinput]
    else:
        print("We shouldn't see this",stringinput)
        stringoutput = ""
#Exception, uncomment for testing.
#    if stringoutput == "":
#        raise Exception("Output not found")
    return stringoutput

'''
def SwDADSARMDnum(stringput):
    tagdict = {
    "Statement-non-opinion": 0,
    "Statement-opinion": 0,
    "Repeat-phrase": 0,
    "Collaborative Completion": 0,
    "Quotation": 0,
    "Or-Clause": 0,
    "Acknowledge (Backchannel)": 1,
    "Appreciation": 1,
    "Response Acknowledgement": 1,
    "Maybe/Accept-Part": 2,
    "Agree/Accept": 2,
    "Yes Answers": 2,
    "Dispreferred answers": 3,
    "Affirmative Non-yes Answers": 3,
    "Response": 3,
    "Hold Before Answer/Agreement": 3,
    "Hedge": 3,
    "Reject": 4,
    "Negative Non-no Answers": 4,
    "No Answers": 4,
    "Conventional-opening": 5,
    "Signal-non-understanding": 6,
    "Conventional-closing": 7,
    "Wh-Question": 8,
    "Declarative Yes-No-Question": 8,
    "Yes-No-Question": 8,
    "Open-Question": 8,
    "Rhetorical-Question": 8,
    "Tag-Question": 8,
    "Summarize/Reformulate": 9,
    "Backchannel in Question Form": 9,
    "Offers, Options Commits": 10,
    "Action-directive": 11,
    "Abandoned": 12,
    "Turn-exit": 12,
    "Other": 12,
    "Downplayer": 12,
    "Apology": 12,
    "Other": 12,
    "Thanking": 12,
    "Non-Verbal": 13,
    "Uninterpretable": 13,
    "Self-talk": 13,
    "3rd-Party Talk": 13
    }
    if stringput in tagdict.keys():
        intout = dict[stringput]
    else:
        print(stringput)
        intout = 0
    # Exception, uncomment for testing.
    #    if stringoutput == "":
    #        raise Exception("Output not found")
    return intout
'''

# def JsonTagtoNumber(stringput):
#     tagdict = {
#     "Assertion-Opinion": 0,
#     "Acknowledge" :1,
#     "Agree-Accept": 2,
#     "Response-Answer":3,
#     "Response-Non-Answer": 4,
#     "disagree-reject" : 5,
#     "Disagree-Reject" : 5,
#     "Conventional-Opening": 6,
#     "Signal-Non-Understanding": 7,
#     "Conventional-Closing": 8,
#     "information-request":9,
#     "Information-Request": 9,
#     "Confirmation-Request": 10,
#     "Offer-Commit": 11,
#     "Action-Directive": 12,
#     "Other-Conventional-Phrase": 13,
#     "Correct-Misspelling": 14
#     }
#     if stringput in tagdict.keys():
#         intout = tagdict[stringput]
#     else:
#         print("Ourstring is not found", stringput)
#         intout = 0
#     # Exception, uncomment for testing.
#     #    if stringoutput == "":
#     #        raise Exception("Output not found")
#     return intout


def JsonTagtoNumber(stringput):
    tagdict = {
    "Assertion-Opinion": 0,
    "Acknowledge" :1,
    "Agree-Accept": 2,
    "Response-Answer":3,
    "response-answer":4,
    "Response-Non-Answer": 4,
    "disagree-reject" : 5,
    "Disagree-Reject" : 5,
    "Conventional-Opening": 6,
    "conventional-opening": 6,
    "Signal-Non-Understanding": 7,
    "Conventional-Closing": 8,
    "information-request":9,
    "Information-Request": 9,
    "Confirmation-Request": 10,
    "Offer-Commit": 11,
    "Action-Directive": 12,
    "Other-Conventional-Phrase": 13,
    "Correct-Misspelling": 13
    }
    if stringput in tagdict.keys():
        intout = tagdict[stringput]
    else:
        print("Warning! The tag is not found", stringput)
        intout = -1
    # Exception, uncomment for testing.
    #    if stringoutput == "":
    #        raise Exception("Output not found")
    return intout

def NumbertoJsonTag(stringput):
    tagdict = {
    0:"Assertion-Opinion",
    1:"Acknowledge",
    2:"Agree-Accept",
    3:"Response-Answer",
    4:"Response-Non-Answer",
    5:"Disagree-Reject",
    6:"Conventional-Opening",
    7:"Signal-Non-Understanding",
    8:"Conventional-Closing",
    9:"Information-Request",
    10:"Confirmation-Request",
    11:"Offer-Commit",
    12:"Action-Directive",
    13:"Other-Conventional-Phrase"
    }
    if stringput in tagdict.keys():
        intout = tagdict[stringput]
    else:
        print("Warning! The tag is not found", stringput)
        intout = -1
    # Exception, uncomment for testing.
    #    if stringoutput == "":
    #        raise Exception("Output not found")
    return intout

#Takes a number from 0-42 and converts it to 0-14 form

def numconvert(numberin):
    #print("numberin is", numberin)
    outputone = NumtoSwDa(numberin)
    #Outputs SWDA tag
    #print("Output is", outputone)
    outputtwo = SwDatoDSARMD(outputone)
    #Outputs disarmed tag
    finalout = JsonTagtoNumber(outputtwo)
    #Outputs 0-14
    return finalout
