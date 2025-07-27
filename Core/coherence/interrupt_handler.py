def reconcile_interrupts(log):
    if "INTERRUPT" in log:
        return "[InterruptLayer]  Interruption detected  Patch pending."
    return "[InterruptLayer] Clean thread."

if __name__ == "__main__":
    print(reconcile_interrupts("LOG: task OK  INTERRUPT  resume"))
