# multimodal_affinity_grid.py
class MultimodalAffinityGrid:
    def score_alignment(self, text_tone, audio_tone, visual_cue):
        score = 0
        if text_tone == audio_tone:
            score += 1
        if audio_tone == visual_cue:
            score += 1
        return score / 2.0  # max score is 1.0
