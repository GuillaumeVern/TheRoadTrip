import json
import math
import numpy as np
import os
import shutil
import fnmatch
from os.path import isdir, join


offsetX = 1024
offsetY = -2049.4
offsetZ = -21.200

def rotate90(x, y):
    transformedX = (x * math.cos(math.pi/2)) + (y * math.sin(math.pi/2)) + offsetX
    transformedY = (-x * math.sin(math.pi/2)) + (y * math.cos(math.pi/2)) + offsetY
    return transformedX, transformedY

def move(path, file):
    jsonFile = open(path + "\\" + file)
    jsonString = jsonFile.read()

    decoder = json.JSONDecoder()
    encoder = json.JSONEncoder()

    parsed_values = []
    calculated_values = []

    rot = np.array([[math.cos(90 * math.pi / 180), -math.sin(90 * math.pi / 180), 0],
                    [math.sin(90 * math.pi / 180), math.cos(90 * math.pi / 180), 0],
                    [0, 0, 1]])

    while jsonString:
        data, new_start = decoder.raw_decode(jsonString)
        jsonString = jsonString[new_start:].strip()
        parsed_values.append(data)



    for row in parsed_values:
        if 'pos' in row:
            x, y = row['pos'][0], row['pos'][1]
            row['pos'][0], row['pos'][1] = rotate90(x, y)
            row['pos'][2] += offsetZ
            
        if 'position' in row:
            x, y = row['position'][0], row['position'][1]
            row['position'][0], row['position'][1] = rotate90(x, y)
            row['position'][2] += offsetZ
        
        i = 0
        if 'nodes' in row:
            for node in row['nodes']:
                x, y = node[0], node[1]
                row['nodes'][i][0], row['nodes'][i][1] = rotate90(x, y)
                i += 1
                
        if 'rotationMatrix' in row:
            object_matrix = np.array(row['rotationMatrix'])
            object_matrix = np.array([[object_matrix[0], object_matrix[1], object_matrix[2]], [object_matrix[3], object_matrix[4], object_matrix[5]], [object_matrix[6], object_matrix[7], object_matrix[8]]])
            object_matrix = object_matrix.dot(rot)
            row['rotationMatrix'] = [object_matrix[0][0], object_matrix[0][1], object_matrix[0][2], object_matrix[1][0], object_matrix[1][1], object_matrix[1][2], object_matrix[2][0], object_matrix[2][1], object_matrix[2][2]]
        elif 'pos' in row or 'position' in row:
            row['rotationMatrix'] = [rot[0][0], rot[0][1], rot[0][2], rot[1][0], rot[1][1], rot[1][2], rot[2][0], rot[2][1], rot[2][2], ]
            
        
        
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




sourceFolder = "C:\\Users\\Administrator\\Desktop\\Utah\\forest"
targetFolder = "C:\\Users\\Administrator\\AppData\\Local\\BeamNG.drive\\0.29\\mods\\unpacked\\TheRoadTrip\\levels\\road_trip\\forest"
# directories = [os.path.abspath(x[0]) for x in os.walk(sourceFolder)]
# directories.remove(os.path.abspath(sourceFolder))

# if os.path.exists(targetFolder) and os.path.isdir(targetFolder):
#         print('removing existing directory "{}"'.format(targetFolder))
#         shutil.rmtree(targetFolder, ignore_errors=False)


# shutil.copytree(sourceFolder, targetFolder, ignore=include_patterns('*.json', '.png', '.PNG'))

for root, dirs, files in os.walk(sourceFolder): 
    for f in files:
        shutil.copyfile(root + "\\" + f, targetFolder + root[53:] + "\\" + f)
        move(targetFolder + root[53:], f)
        
    
print("done!")