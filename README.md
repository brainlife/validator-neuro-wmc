For detailed definition of what WMC datatype is, please see

> https://brainlife.io/datatype/5cc1d64c44947d8aea6b2d8b

# Checks performed by this validator

This validator currently checks for the following conditions.

* `names` and `index` fields exists inside classification.mat
* No whitespaces inside the each name
* All names are unique
* Names array should be as big or bigger than the number of unique elements

# Examples of valid WMC structure

```
names: ['tractA', 'tractB', 'tractC']
index: [0, 0, 1, 0, 2, 0, 0, 3, 3]
```

```
names: ['tractA', 'tractB', 'tractC']
index: [0, 0, 1]
```

* index 2(tractB), 3(tractC) has no streamline segmented (but it probably has attempted). This is OK, but validator will give warnings that there are 0 streamlines for those tracts.

# Examples of invalid WMC structure

```
names: ['tractA', 'tractB', 'tractC']
index: [0, 0, 1, 0, 2, 0, 0, 3, 3, 4]
```

* The last item in index(4) exceeds the length of names array. names should have all the names for all index values.

```
names: ['tract A', 'tract B', 'tract B']
index: [0, 0, 1, 0, 2, 0, 0, 3, 3]
```

* names should not contain space, and there are duplicate names (`tract B`)
