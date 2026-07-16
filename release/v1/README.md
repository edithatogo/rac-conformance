# v1.0 Release Candidate Packet

This directory is a release-candidate evidence packet, not a published v1.0
release. `gates.json` is the machine-readable source of truth for the current
qualification boundary and `tools/v1_release_audit.py` evaluates it without
promoting candidate fixtures or human/external gates.

The packet must be regenerated from the exact reviewed commit before any human
release authorization. Publication, signing, DOI deposition, and announcements
remain separate human actions.
