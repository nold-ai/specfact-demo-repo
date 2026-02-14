# backlog-labeler

Official demo plugin that labels blocked backlog items during `post_sync`.

## Why it exists

It demonstrates a safe extension that does not bypass enforcement gates:

- reads sync output from context
- adds `specfact:blocker` label to blocked items
- does not mutate gate decisions

## Local test

```bash
./specfact plugin test plugins/official/backlog_labeler/plugin.py --fixture fixtures
```
