def create_channel(name:str):
    if name=='email':
        return 
    if name=='sms':
        return 
    if name == 'console':
        return 
    else:
        raise ValueError(f"Channel {name} is not supported")