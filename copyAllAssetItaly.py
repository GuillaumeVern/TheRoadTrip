import json
import math
import numpy as np
import os
import shutil
import fnmatch
from os.path import isdir, join




def rotate90(x, y):
    transformedX = (x * math.cos(math.pi/2)) + (y * math.sin(math.pi/2))
    transformedY = (-x * math.sin(math.pi/2)) + (y * math.cos(math.pi/2))
    return transformedX, transformedY

def move(path, file):
    
    offsetX = -2048
    offsetY = -2048
    offsetZ = -21
    
    jsonFile = open(path + "\\" + file)
    jsonString = jsonFile.read()

    decoder = json.JSONDecoder()
    encoder = json.JSONEncoder()

    parsed_values = []
    calculated_values = []


    while jsonString:
        data, new_start = decoder.raw_decode(jsonString)
        jsonString = jsonString[new_start:].strip()
        parsed_values.append(data)



    for row in parsed_values:
        if 'pos' in row:
            row['pos'][0] += offsetX
            row['pos'][1] += offsetY
            row['pos'][2] += offsetZ
                
        elif 'position' in row:
            row['position'][0] += offsetX
            row['position'][1] += offsetY
            row['position'][2] += offsetZ
        
        elif row['class'] == 'TSStatic' or row['class'] == 'Prefab':
            row['position'] = [0, 0, 0]
            row['position'][0] = offsetX
            row['position'][1] = offsetY
            row['position'][2] = offsetZ
            
        
        
        i = 0
        if 'nodes' in row:
            for node in row['nodes']:
                row['nodes'][i][0] += offsetX
                row['nodes'][i][1] += offsetY
                i += 1
                

        
        
        calculated_values.append(row)
        

        
    f = open(path + "\\" + file, "w")
    print("writing", path + "\\" + file)
    for row in calculated_values:
        f.write(encoder.encode(row) + "\n")

    f.close()

    jsonFile.close()
    
def include_patterns(*patterns):
    def _ignore_patterns(path, all_names):
        # Determine names which match one or more patterns (that shouldn't be
        # ignored).
        keep = (name for pattern in patterns
                        for name in fnmatch.filter(all_names, pattern))
        # Ignore file names which *didn't* match any of the patterns given that
        # aren't directory names.
        dir_names = (name for name in all_names if isdir(join(path, name)))
        return set(all_names) - set(keep) - set(dir_names)

    return _ignore_patterns




sourceFolder = "C:\\Users\\Administrator\\Desktop\\Italy\\main\\MissionGroup"
targetFolder = "C:\\Users\\Administrator\\AppData\\Local\\BeamNG.drive\\0.29\\mods\\unpacked\\TheRoadTrip\\levels\\road_trip\\main\\MissionGroup\\Italy"
directories = [os.path.abspath(x[0]) for x in os.walk(sourceFolder)]
directories.remove(os.path.abspath(sourceFolder))

if os.path.exists(targetFolder) and os.path.isdir(targetFolder):
        print('removing existing directory "{}"'.format(targetFolder))
        shutil.rmtree(targetFolder, ignore_errors=False)


shutil.copytree(sourceFolder, targetFolder, ignore=include_patterns('*.json', '.png', '.PNG'))

for root, dirs, files in os.walk(sourceFolder): 
    for f in files:
        shutil.copyfile(root + "\\" + f, targetFolder + root[54:] + "\\" + f)
        move(targetFolder + root[54:], f)
        
    
print("done!")