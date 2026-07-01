# State Views

This directory contains state-view packages.

A state-view package is a query-oriented vertical slice. Its job is to consume
events, project the state needed for one question, and return a read model or
query result without making domain decisions.

The pattern is:

`event -> projection/read model -> query result`

Each package under `vertical_slices/state-views/` should own one query or read
model slice and register the public query names it answers.
