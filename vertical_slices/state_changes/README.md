# State Changes

This directory contains state-change packages.

A state-change package is a command-oriented vertical slice. Its job is to take
an incoming command, load the events needed for one decision boundary, enforce
the business rules for that decision, and emit durable events.

The pattern is:

`command -> decision logic over selected events -> event`

Each package under `vertical_slices/state_changes/` should own one command slice
and register the public command names it handles.
