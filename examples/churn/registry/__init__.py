"""Local model registry (Module 09): versions, stages, promotion history,
and rollback — all implemented with plain files so it runs offline.

    python -m registry list
    python -m registry register --model pipe_out/model.joblib ...
    python -m registry stage v001 staging
    python -m registry stage v001 production
    python -m registry rollback production
    python -m registry get production

This is a *demonstration* registry. Production systems use a remote registry
service (e.g. the MLflow Model Registry behind a tracking server); the concepts
are identical, the transport is not. See docs/modules/09-.../concepts.md.
"""