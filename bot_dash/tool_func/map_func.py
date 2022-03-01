def set_range(x_move:float,y_move:float,motion_para:dict)->None:
    if x_move>=0:
        motion_para["x_upper_limit"]+=x_move
    else:
        motion_para["x_lower_limit"]-=x_move
    
    if y_move>=0:
        motion_para["y_upper_limit"]+=y_move
    else:
        motion_para["y_lower_limit"]-=y_move