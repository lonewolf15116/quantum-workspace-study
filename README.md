# Transformer workspace tokens for quantum circuit observables

This study tests whether converting four masked padding slots into learned workspace improves observable prediction at fixed dense sequence capacity (179 positions).

The architecture and workload specifications are in [protocol](protocol/). The resource enumerations, Pilot 01, and both diagnostic packages are in [evidence](evidence/). The ZIP archives preserve the original scripts, data, and results. The D002 archive includes instructions for reproducing its analysis and running the GPU memory check.

Pilot 01 is exploratory. All six final checkpoints had higher training MAE than the zero predictor. GPU fit and confirmatory performance remain unmeasured.
