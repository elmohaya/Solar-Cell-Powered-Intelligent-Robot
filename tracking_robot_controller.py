#!/usr/bin/env python
# coding: utf-8

# In[49]:


left_sensor = 4.85
med_sensor = 0.87
right_sensor = 4.87
#motion(left_sensor, med_sensor, right_sensor)


# In[27]:


# [System]                                   
# Name='signal_robot'
# Type='mamdani'
# Version=2.0
# NumInputs=3
# NumOutputs=2
# NumRules=5
# AndMethod='min'
# OrMethod='max'
# ImpMethod='prod'
# AggMethod='max'
# DefuzzMethod='COS'

# [Input1]
# Name='left_sensor'
# Range=[-2 7]
# NumMFs=2

# [Input2]
# Name='med_sensor'
# Range=[-2 7]
# NumMFs=2

# [Input3]
# Name='right_sensor'
# Range=[-2 7]
# NumMFs=2

Input_Low=[-2 ,-2 ,0 ,3]
Input_High=[1 ,5 ,7 ,7]

# [Output1]
# Name='left_motor'
# Range=[50 100]
# NumMFs=3

# #[Output2]
# Name='right_motor'
# Range=[50 100]
# NumMFs=3

Output_Fast=[50 ,50 ,65]
Output_Med=[55 ,60 ,65]
Output_Slow=[85 ,100 ,100]


# In[28]:


# Implication and Inference

def calc_input_low (x):
    
    # the objective of this function is find
    # the Degree of Fullfillment of input low
    
    if x < -2:
        result = 0.0
    elif x<= 0:
        result = 1.0
    elif x<= 3:
        result = (-1.0/3.0)*x+1
    else:
        result = 0.0
    
    return result 

#####################################

def calc_input_high (x):
    
    # the objective of this function is find
    # the Degree of Fullfillment of input high
    
    if x < 1:
        result = 0.0
    elif x<= 5:
        result = (1.0/4.0)*x-1.0/4.0
    elif x<= 7:
        result = 1.0 
    else:
        result = 0.0
    
    return result


# In[52]:


# Evaluating the rules


# R1: if (left_Sensor is High) & (med_sensor is Low) & (right_sensor is High) then (left_motor is Med)(right_motor is Med):

DOF1 = min(calc_input_high(left_sensor), calc_input_low(med_sensor), calc_input_high(right_sensor))
infer_r1_out1 = list()

# Sampling the area of the inference
for i in range(Output_Med[0], Output_Med[1]+1, 1):
    infer_r1_out1.append([i, DOF1*(1.0/(Output_Med[1]-Output_Med[0]))*(i-Output_Med[0])])
for i in range(Output_Med[1], Output_Med[2]+1, 1):
    infer_r1_out1.append([i, DOF1*(-1.0/(Output_Med[2]-Output_Med[1]))*(i-Output_Med[2])])
infer_r1_out2= infer_r1_out1   
############################################################################

# R2: if (left_Sensor is High) & (med_sensor is High) & (right_sensor is Low) then (left_motor is Fast)(right_motor is Slow):

DOF2 = min(calc_input_high(left_sensor), calc_input_high(med_sensor), calc_input_low(right_sensor))
infer_r2_out1 = list()
infer_r2_out2 = list()

# Sampling the area of the inference
for i in range(Output_Fast[1], Output_Fast[2]+1, 1):
    infer_r2_out1.append([i, DOF2*(-1.0/(Output_Fast[2]-Output_Fast[1]))*(i-Output_Fast[2])])
    
for i in range(Output_Slow[0], Output_Slow[1]+1, 1):
    infer_r2_out2.append([i, DOF2*(1.0/(Output_Slow[1]-Output_Slow[0]))*(i-Output_Slow[0])])

############################################################################

# R3: if (left_Sensor is Low) & (med_sensor is High) & (right_sensor is High) then (left_motor is Slow)(right_motor is Fast):

DOF3 = min(calc_input_low(left_sensor), calc_input_high(med_sensor), calc_input_high(right_sensor))
infer_r3_out1 = list()
infer_r3_out2 = list()

# Sampling the area of the inference
for i in range(Output_Fast[1], Output_Fast[2]+1, 1):
    infer_r3_out2.append([i, DOF3*(-1.0/(Output_Fast[2]-Output_Fast[1]))*(i-Output_Fast[2])])
    
for i in range(Output_Slow[0], Output_Slow[1]+1, 1):
    infer_r3_out1.append([i, DOF3*(1.0/(Output_Slow[1]-Output_Slow[0]))*(i-Output_Slow[0])])
    
############################################################################

# R4: if (left_Sensor is High) & (med_sensor is High) & (right_sensor is High) then (left_motor is Slow)(right_motor is Slow):

DOF4 = min(calc_input_high(left_sensor), calc_input_high(med_sensor), calc_input_high(right_sensor))
infer_r4_out1 = list()
infer_r4_out2 = list()

# Sampling the area of the inference
for i in range(Output_Slow[0], Output_Slow[1]+1, 1):
    infer_r4_out1.append([i, DOF4*(1.0/(Output_Slow[1]-Output_Slow[0]))*(i-Output_Slow[0])])
    infer_r4_out2.append([i, DOF4*(1.0/(Output_Slow[1]-Output_Slow[0]))*(i-Output_Slow[0])])
    
############################################################################

# R5: if (left_Sensor is Low) & (med_sensor is Low) & (right_sensor is Low) then (left_motor is Slow)(right_motor is Slow):

DOF5 = min(calc_input_low(left_sensor), calc_input_low(med_sensor), calc_input_low(right_sensor))
infer_r5_out1=list()
infer_r5_out2=list()

# Sampling the area of the inference
for i in range(Output_Slow[0], Output_Slow[1]+1, 1):
    infer_r5_out1.append([i, DOF5*(1.0/(Output_Slow[1]-Output_Slow[0]))*(i-Output_Slow[0])])
    infer_r5_out2.append([i, DOF5*(1.0/(Output_Slow[1]-Output_Slow[0]))*(i-Output_Slow[0])])
    

    
infer_out1 = infer_r1_out1 + infer_r2_out1 + infer_r3_out1 + infer_r4_out1 + infer_r5_out1
infer_out2 = infer_r1_out2 + infer_r2_out2 + infer_r3_out2 + infer_r4_out2 + infer_r5_out2

#print(infer_out1)
#print('  ')
#print(infer_out2)
#print('  ')
#print(DOF1, DOF2, DOF3, DOF4, DOF5)


# In[53]:


# Defuzzification Code

num1 = 0.0
den1 = 0.0 

num2 = 0.0
den2 = 0.0 

if (DOF1 == 0) and (DOF2 == 0) and (DOF3 == 0) and (DOF4 == 0) and (DOF5 == 0):
    
    left_motor_signal = 100
    right_motor_signal = 100
else:

    for i in range(len(infer_out1)):
        num1 = num1 + infer_out1[i][0]*infer_out1[i][1]
        den1 = den1 + infer_out1[i][1]
    
    for i in range(len(infer_out2)):    
        num2 = num2 + infer_out2[i][0]*infer_out2[i][1]
        den2 = den2 + infer_out2[i][1]

    left_motor_signal = num1/den1
    right_motor_signal = num2/den2

left_motor_signal, right_motor_signal


# In[ ]:




