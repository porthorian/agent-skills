from gateway import send


def notify(address, history=[]):
    receipt = send(address, "ready")
    history.append(receipt)
    return history
