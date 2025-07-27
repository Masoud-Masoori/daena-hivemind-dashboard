# truth_bias_calibrator.py

def calibrate_bias(response_set, external_facts):
    for res in response_set:
        topic = res.get('topic')
        if topic in external_facts:
            res['confidence'] = min(1.0, res['confidence'] + 0.1)
    print(f"[TruthBias]  Calibrated {len(response_set)} responses using external facts.")
    return response_set
