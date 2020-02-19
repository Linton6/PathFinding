# Multi-Agent path planning in python

# Introduction
This repository consists of the implementation of some multi-agent path-planning algorithms in Python. Two methods, namely Safe-Interval Path Planning, and Conflict-Based Search are implemented. Later, 
 
The dimensions of the map, obstacles, and initial and final positions of the agents must be mentioned in input.yaml. 

The output is generated and stored in output.yaml.
# Table of contents
 - [Path-Planning](#planning) 
    - [Safe-Interval Path Planning (SIPP)](#safe-interval-path-planning) 
    - [Conflict-Based Search (CBS)](#conflict-based-search) 
 - [Scheduling](#scheduling)
    - [Post-processing of plan using Temporal Plan Graph](#post-processing-with-tpg)

# Planning
## Safe-Interval Path Planning
SIPP is a local planner, using which, a collision-free plan can be generated, after considering the static and dynamic obstacles in the environment. In the case of multi-agent path planning, the other agents in the environment are considered as dynamic obstacles. 

### Execution

For SIPP multi-agent prioritized planning, run:
```
cd ./sipp
python multi_sipp.py input.yaml output.yaml
```

### Results
To visualize the generated results

```
python visualize_sipp.py input.yaml output.yaml 
```
To record video

```
python visualize_sipp.py input.yaml output.yaml --video 'sipp.avi' --speed 1
```

Test 1 (Success)                        | Test 2 (Failure)


## Conflict Based Search
Conclict-Based Search (CBS), is a multi-agent global path planner. 

### Execution 
Run:
```
cd ./cbs
python cbs.py map_32by32_obst204_agents10_ex10.yaml output.yaml
```

### Results
To visualize the generated results:
```
python ../visualize.py map_32by32_obst204_agents10_ex10.yaml output.yaml
```

# Scheduling cd
## Post-processing with TPG

The plan, which is computed in discrete time, can be postprocessed to generate a plan-execution schedule, that takes care of the kinematic constraints as well as imperfections in plan execution. 

This work is based on: [Multi-Agent Path Finding with Kinematic Constraints](https://www.aaai.org/ocs/index.php/ICAPS/ICAPS16/paper/view/13183/12711)

Once the plan is generated using CBS, please run the following to generate the plan-execution schedule:

```
cd ./scheduling
python minimize.py ../cbs/output.yaml real_schedule.yaml
```




