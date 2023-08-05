## Introduction
This project implements "Privacy-Preserving Continuous Event Data Publishing". 
## Python package
The implementation has been published as a standard Python package. Use the following command to install the corresponding Python package:

```shell
pip install pp-cedp
```

## Usage
```python
from pp_cedp.CEDP import CEDP

if __name__ == '__main__':
    log_name1 = "./event_logs/EL1_minutes_4_5_1_sequence.xes"
    log_name2 = "./event_logs/EL2_minutes_4_5_1_sequence.xes"
    event_attributes = ['concept:name']
    sensitive = ['Diagnose']
    life_cycle = ['complete', '', 'COMPLETE']
    all_life_cycle = True #True will ignore the transitions specified in life_cycle
    time_accuracy = "original" # original, seconds, minutes, hours, days
    bk_length = 1
    n = 1
    cedp = CEDP()
    R1_KA, R2_KA, FA, CA, BA = cedp.calc_FCB_anonymity(log_name1, log_name2, event_attributes, life_cycle, all_life_cycle, sensitive, time_accuracy, n, bk_length)
```