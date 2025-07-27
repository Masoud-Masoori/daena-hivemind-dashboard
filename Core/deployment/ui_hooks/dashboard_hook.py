def bind_ui_to_deployment(dashboard):
    if "launchButton" not in dashboard:
        raise Exception(" UI launch button missing.")
    dashboard["launchButton"].onClick = lambda: print(" Launch initiated via UI.")
    print(" UI hook bound to launch system.")
