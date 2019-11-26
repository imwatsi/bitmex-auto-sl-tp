import os

def stop_bot(reason=None):
    print('Shutting down bot...')
    if reason:
        print(f'REASON: {reason}')
    os._exit(0)