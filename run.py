import nltk
import json
import repositories.tastingNotes as TastingNotesRepo

count = 0
maxImportCount = 20
TastingNotesRepo.deleteAll()
with open('resources/winemag-data-130k-v2.json') as json_file:  
    data = json.load(json_file)
    for note in data:
        if(count  > maxImportCount):
            break
        else:
            count= count +1
            TastingNotesRepo.add(note)