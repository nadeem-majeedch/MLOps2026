# Lab 01 fixture — nondeterministic training script

Two runs of the same command on the same data must give the same answer.
This one does not. Real output from the authoring machine:

```text
$ python train_nondeterministic.py --label run1
{ "roc_auc": 0.7846, "f1": 0.5532, "n_test_rows": 120 }   # values differ per run

$ python train_nondeterministic.py --label run2
{ ... different numbers ... }
```

Three independent causes hide in the file (each is commented with a `...`
that you should not take at face value — the comments are what a careless
colleague left behind). The data file is byte-identical between runs
(`python ../make_data.py --check` proves it), so **all** variation comes
from the code.

Fix *your copy* until:

```powershell
python train_nondeterministic.py --label a
python train_nondeterministic.py --label b
# metrics_a.json and metrics_b.json must be byte-identical
```

See `../solutions/lab-01/` **after** you have your own answer.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../../docs/about/index.md).*