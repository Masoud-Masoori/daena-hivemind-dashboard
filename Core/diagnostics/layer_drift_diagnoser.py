def diagnose_layer_drift(layer_outputs_old, layer_outputs_new):
    if len(layer_outputs_old) != len(layer_outputs_new):
        return "Incompatible layer lengths."
    drift_report = []
    for i, (old, new) in enumerate(zip(layer_outputs_old, layer_outputs_new)):
        drift = abs(old - new)
        drift_report.append((i, drift))
    return drift_report
