# Capstone monitoring decision

| input | value |
|---|---|
| drift | DRIFT DETECTED (strong: attendance_rate, missed_assessments, assignment_rate) |
| labels + degradation | no / labels absent |

## Decision: **MONITOR**

Drift alone never authorises a retrain - keep watching until labels agree.

_A script recommends; a human decides (Module 14's rule, restated here)._
