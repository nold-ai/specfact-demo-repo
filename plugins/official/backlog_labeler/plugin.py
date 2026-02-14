from specfact_demo.plugin_sdk import Plugin


class BacklogLabelerPlugin(Plugin):
    name = "backlog-labeler"
    version = "0.1.0"
    api_version = "1.0"
    scope = ["sync-adapter"]
    invariants_touched = ["backlog_sync"]
    side_effects = ["annotate_blocked_items"]
    attestation_hash = "sha256:official-demo-backlog-labeler"

    def post_sync(self, context):
        sync_result = context.get("sync_result", {})
        for item in sync_result.get("updated_items", []):
            labels = item.setdefault("labels", [])
            if "specfact:blocker" not in labels:
                labels.append("specfact:blocker")
