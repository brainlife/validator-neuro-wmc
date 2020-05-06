#!/usr/bin/env python3

import os
import json
import scipy.io as sio
import numpy as np
import sys

with open('config.json', encoding='utf8') as config_json:
    config = json.load(config_json)

results = {"errors": [], "warnings": []}

if not os.path.exists("output"):
    os.mkdir("output")
if not os.path.exists("secondary"):
    os.mkdir("secondary")

############## noarmalize output

# for now, we are just going to pass through everything

if os.path.lexists("output/classification"):
    os.remove("output/classification")
os.symlink("../"+config["classification"], "output/classification")

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
        return

    try:
        names = m["classification"]["names"].all()
        print(names)
    except ValueError:
        results["errors"].append("no names field inside classification struct");
        return

    try:
        index = m["classification"]["index"]
        #print(index)
    except ValueError:
        results["errors"].append("no index field inside classification struct");
        return

    #count numbers of values
    np.set_printoptions(threshold=sys.maxsize)
    unique_elements, counts_elements = np.unique(index.all(), return_counts=True)
    print(unique_elements)
    print(counts_elements)

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
    if len(names) != len(np.unique(names)):
        results["errors"].append("names must be all unique")

    #names array should be as big or bigger than the number of unique elements
    max_index = int(np.max(unique_elements))
    if max_index > len(names):
        results["errors"].append("names array has size of "+str(len(names))+" when the max index value is "+str(max_index)+". This means not all names are listed in the names array at the corresponding index value")

    #for index in unique_elements:
    #    index = int(index)
    #    if index == 0:
    #        continue
    #    try:
    #        name = names[index-1]
    #    except IndexError:
    #        results["errors"].append("names array does not contain a name for classification index value of "+str(index))

validate_classification()

with open("product.json", "w") as fp:
    json.dump(results, fp)

if len(results["errors"]) > 0:
    print("error detected")
    print(results["errors"])
if len(results["warnings"]) > 0:
    print("warnings detected")
    print(results["warnings"])
print("done");

