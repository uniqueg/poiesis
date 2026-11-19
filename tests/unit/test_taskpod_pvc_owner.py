"""The task PVC's ownerReference must not block the Job's deletion."""

from __future__ import annotations

from kubernetes.client import V1ObjectMeta, V1PersistentVolumeClaim

from poiesis.core.taskpod import attach_pvc_owner


def test_pvc_owner_reference_does_not_block_owner_deletion() -> None:
    """The PVC is owned by the Job, without blocking the Job's deletion."""
    pvc = V1PersistentVolumeClaim(metadata=V1ObjectMeta(name="task-pvc"))

    attach_pvc_owner(pvc, job_uid="uid-1", job_name="job-1")

    assert pvc.metadata is not None
    (ref,) = pvc.metadata.owner_references
    assert (ref.api_version, ref.kind, ref.name, ref.uid) == (
        "batch/v1",
        "Job",
        "job-1",
        "uid-1",
    )
    assert ref.controller is True
    assert ref.block_owner_deletion is False
