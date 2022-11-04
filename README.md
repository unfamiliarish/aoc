# Advent of Code 

## Unfinished:


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
├── Makefile  
└── utils.py  
```

The `utils.py` at project root is the master version.
It is copied into individual `day#` directories to make imports simpler. 

Each year has its own directory, and under those are directories holding code for each day. 

Imports within a `day#` solution directory are exclusively packages or other files within that directory.