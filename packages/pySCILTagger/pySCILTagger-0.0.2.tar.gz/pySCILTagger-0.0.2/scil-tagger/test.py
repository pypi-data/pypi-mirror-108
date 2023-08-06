'''
For testing,
example of how to use the tagger
'''

from scil-tagger import tagger

tag = tagger.Tagger("dialogue/Mar07_GroupB.json", "selected.pt")
tag.getDialogActTags()


