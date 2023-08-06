'''
For testing,
example of how to use the tagger
'''

from sciltagger import tagger

tag = tagger.Tagger("dialogue/Mar07_GroupB.json", "selected.pt")
tag.getDialogActTags()


