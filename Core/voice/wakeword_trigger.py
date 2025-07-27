def handle_wakeword(phrase):
    if "launch pitch" in phrase.lower():
        from core.public.campaign_trigger import launch_pitch
        launch_pitch()
