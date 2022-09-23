# Advent of Code 

## File Structure 
```
aoc  
├── yyyy  
│   ├── day#  
│   └── day#  
├── yyyy 
│   ├── day#  
│   └── day#  
|   ...
├── README.md  
└── utils.py  
```

The `utils.py` at project root is the master utils file. This is copied into each `day#` directory to make imports simpler. 

Then each year has its own directory, and under that are directories holding code for each day. 

Any imports are for packages or other files within a `day#` directory.