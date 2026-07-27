# Task: Raft Write-Ahead Log (WAL) Reconciliation & Canonical State Reconstruction

## Problem Overview
You are tasked with resolving split-brain divergence across a 5-node distributed Raft cluster. During a severe network partition, nodes accepted uncommitted entries across multiple leader terms, leading to divergent Write-Ahead Logs (WALs). Your goal is to apply strict Raft commitment semantics, discard uncommitted divergent tails, replay valid key-value state mutations in order, and output the reconciled cluster state to `/app/reconciled_state.json`.

## Input Specification
The input log file is located at `/app/wals.json` (or relative path `assets/wals.json`). It contains WAL records for 5 cluster nodes (`node_1` to `node_5`).

Each entry in a node's log contains:
- `index` (integer, 1-indexed): Log entry position.
- `term` (integer): Leader term when entry was proposed.
- `command` (object): Key-value state mutation, formatted as `{"op": "SET", "key": "<string>", "val": <string|int>}` or `{"op": "DELETE", "key": "<string>"}`.
- `replications` (array of strings): List of node IDs that acknowledged receiving/persisting this entry.
- `leader_commit_index` (integer): The commit index broadcasted by the leader of that term.

## Reconciliation & Commitment Rules
1. **Raft Commitment Rule (§5.4.2)**: An entry at index `i` with term `t` is considered **committed** if and only if:
   - It is replicated on a strict majority of nodes (at least 3 out of 5 nodes in `replications`).
   - It is covered by a leader commit index from term `>= t` (i.e., `i <= leader_commit_index` of a valid leader entry in term `>= t`).
2. **Truncation Rule**: Any uncommitted entries following a term divergence must be truncated and discarded.
3. **State Machine Execution**:
   - Start with an empty key-value state `{}`.
   - Replay all committed commands in strict ascending log index order starting from index 1.
   - `SET` updates or inserts the key-value pair. `DELETE` removes the key from the state dictionary if present.

## Output Specification
You must write the final result to `/app/reconciled_state.json` matching the following JSON schema:

```json
{
  "last_applied_index": <int>,
  "last_applied_term": <int>,
  "state": {
    "<key>": <value>
  },
  "state_hash": "<sha256_hex_string>"
}
