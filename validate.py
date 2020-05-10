#!/usr/bin/env python3

import os
import json
import scipy.io as sio
import numpy as np
import sys

with open('config.json', encoding='utf8') as config_json:
    config = json.load(config_json)

results = {"errors": [], "warnings": [], "meta": {}, "brainlife": []}

if not os.path.exists("output"):
    os.mkdir("output")
if not os.path.exists("secondary"):
    os.mkdir("secondary")

############## noarmalize output

# for now, we are just going to pass through everything

if os.path.lexists("output/classification.mat"):
    os.remove("output/classification.mat")
os.symlink("../"+config["classification"], "output/classification.mat")

if os.path.lexists("output/tracts"):
    os.remove("output/tracts")
os.symlink("../"+config["tracts"], "output/tracts")

if os.path.lexists("output/surfaces"):
    os.remove("output/surfaces")
os.symlink("../"+config["surfaces"], "output/surfaces")

############## validate 

def validate_classification():
    m = sio.loadmat(config["classification"], squeeze_me=True)
    if "classification" not in m:
        results["errors"].append("no classification object");
        return False

    try:
        names = m["classification"]["names"].all()
        if not isinstance(names, np.ndarray):
            names = [names]
        names = list(names)
    except ValueError:
        results["errors"].append("no names field inside classification struct");
        return False

    try:
        index = m["classification"]["index"]
    except ValueError:
        results["errors"].append("no index field inside classification struct");
        return False

    #count numbers of values
    np.set_printoptions(threshold=sys.maxsize)
    unique_indicies, counts_indicies = np.unique(index.all(), return_counts=True)
    print(names)
    print(len(names))
    print(unique_indicies)
    print(len(unique_indicies))
    print(counts_indicies)
    print(len(counts_indicies))

    if max(unique_indicies) > len(names):
        results["errors"].append("max index("+str(max(unique_indicies))+") exceeds the number of names("+str(len(names)))
        return False

    #store counts in the meta
    results["meta"]["tracts"] = []
    results["meta"]["tracts"].append({"name": "unclassified", "index": 0, "count": 0})
    for i in range(0, len(names)):
        results["meta"]["tracts"].append({"name": names[i], "index": i+1, "count": 0})
    for i in range(0, len(unique_indicies)):
        index = unique_indicies[i]
        count = counts_indicies[i]
        results["meta"]["tracts"][index]["count"] = int(count)

    #print(results["meta"]["tracts"])

    #name
    # ['forcepsMinor' 'forcepsMajor' 'parietalCC' 'middleFrontalCC'
    # 'anterioFrontalCC' 'leftcingulum' 'rightcingulum' 'leftUncinate'
    # 'rightUncinate' 'leftIFOF' 'leftArc' 'rightArc' 'leftSLF1And2'
    # 'rightSLF1And2' 'leftSLF3' 'rightSLF3' 'leftfrontoThalamic'
    # 'rightfrontoThalamic' 'leftparietoThalamic' 'rightparietoThalamic'
    # 'leftmotorThalamic' 'rightmotorThalamic' 'leftspinoThalamic'
    # 'rightspinoThalamic' 'leftAslant' 'rightAslant' 'leftILF' 'rightILF'
    # 'leftMDLFang' 'rightMDLFang' 'rightMDLFspl' 'leftpArc' 'rightpArc'
    # 'leftTPC' 'leftmeyer' 'leftbaum' 'rightMotorCerebellar'
    # 'right AnterioFrontoCerebellar' 'rightThalamicoCerebellar'
    # 'leftParietoCerebellar' 'leftVOF' 'rightVOF' 'leftCST' 'rightCST']

    #unique_elements
    # [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
    # 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44]

    #counts_elements
    #[4142   14    7   13   58    9    5   19    3    3    5    5    3   27
    #45   12   12    4    1    8    4   13    4    5    6    4    5    7
    #6    3    4    1    4    2    1    2    3    1    2    1    3   11
    #8    2    3]

    #no space in names entries
    for name in names:
        if name == "":
            results["warnings"].append("Empty name is not allowed")
            break

        for c in name:
            if c.isspace():
                results["warnings"].append("The name '"+name+"' should not contain whitespace")
                break

    #names must be unique
    unique_names = np.unique(names)
    if len(names) != len(unique_names):
        check_names = []
        duplicates = []
        for name in names:
            if name in check_names:
                duplicates.append(name)
            check_names.append(name)
        results["errors"].append("All names must be unique. duplicates:"+",".join(duplicates))
            
    #names array should be as big or bigger than the number of unique elements
    max_index = int(np.max(unique_indicies))
    if max_index > len(names):
        results["errors"].append("names array has size of "+str(len(names))+" when the max index value is "+str(max_index)+". This means not all names are listed in the names array at the corresponding index value. Please re-index data in index array so that all indicies will have the corresponding items inside the names array")

    #warn users if some tracts has 0-streamline
    indicies_set = set(unique_indicies)
    for i in range(len(names)):
        if not (i+1) in indicies_set:
            results["warnings"].append(names[i]+"(index:"+str(i+1)+") has no streamline")

    #TODO The number of entries in the .index vector should be EXACTLY EQUAL to the number of streamlines in the associated tractogram.
    # compare it against meta["count"] from config


    return True

def create_plotly():
    left_x= []
    right_x = []
    mid_x = []
    left_y = []
    right_y = []
    mid_y = []

    for i in range(1, len(results["meta"]["tracts"])):
        tract = results["meta"]["tracts"][i]
        #detect if the name is for left/right/mid
        name = tract["name"]
        count = tract["count"]
        left_pos = name.lower().find("left")
        right_pos = name.lower().find("right")
        if left_pos != -1:
            name = name[:left_pos] + name[left_pos+4:].strip()
            left_x.append(name)
            left_y.append(count)
            
        elif right_pos != -1:
            name = name[:right_pos] + name[right_pos+5:].strip()
            right_x.append(name)
            right_y.append(count)

        else:
            #assume middle
            mid_x.append(name)
            mid_y.append(count)

    #for count in results["meta"]["counts"]:
    #    y.append(count)

    graph = {
        "type": "plotly",
        "name": "Fiber counts",
        "data": [
            {
                "type": "bar",
                "name": "Left Tracts",
                "x": left_x,
                "y": left_y,
            },
            {
                "type": "bar",
                "name": "Right Tracts",
                "x": right_x,
                "y": right_y,
            },
            {
                "type": "bar",
                "name": "Mid Tracts",
                "x": mid_x,
                "y": mid_y,
            }
        ],
        "layout": {
            "barmode": "group",
            "xaxis": {
                "tickangle": 45
            },
            "yaxis": {
                "type": "log",
                "title": "Stream Lines"
            },
            "margin": {
                "b": 125,
                "t": 10
            }
        }
    }
    results["brainlife"].append(graph)

if validate_classification():
    create_plotly()

with open("product.json", "w") as fp:
    json.dump(results, fp)

if len(results["errors"]) > 0:
    print("error detected")
    print(results["errors"])
if len(results["warnings"]) > 0:
    print("warnings detected")
    print(results["warnings"])
print("done");

