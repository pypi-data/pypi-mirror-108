import pandas as pd
import numpy as np



def filter_only_in_season_rice(in_df):
    '''
    filter only in-season rice
    '''
    out_df = in_df[in_df['in_season_rice_f']==1].copy()
    
    return out_df
   



def filter_only_loss(in_df, danger_area_col = 'TOTAL_DANGER_AREA_IN_WA', plant_area_col='TOTAL_ACTUAL_PLANT_AREA_IN_WA', loss_type_class=None):
    '''
    Filter for only loss rows
    '''    
    in_df = in_df[(in_df[danger_area_col] > 0) & (in_df[plant_area_col] > 0)].copy()
        
    return in_df



def filter_only_no_loss(in_df, danger_area_col = 'TOTAL_DANGER_AREA_IN_WA', plant_area_col='TOTAL_ACTUAL_PLANT_AREA_IN_WA'):
    '''
    Filter for only loss rows
    '''    
    in_df = in_df[(in_df[danger_area_col].fillna(0) == 0) & (in_df[plant_area_col] > 0)].copy()
        
    return in_df       




def get_loss_ratio_and_class(in_df, in_dict_master_config, danger_area_col = 'TOTAL_DANGER_AREA_IN_WA', plant_area_col='TOTAL_ACTUAL_PLANT_AREA_IN_WA'):
    '''
    Get loss ratio and loss ratio class
    '''    
    out_df = in_df.copy()
    dict_loss_ratio_bin = in_dict_master_config['dict_loss_ratio_bin']


    out_df['loss_ratio'] = out_df[danger_area_col].fillna(0) / out_df[plant_area_col]
    out_df['loss_ratio'] = np.where( out_df['loss_ratio'].values > 1, 1, out_df['loss_ratio'].values)
    arr_loss_ratio_bin = np.full_like(out_df['loss_ratio'].values, fill_value=np.nan, dtype=np.float32)
    for bin_class in dict_loss_ratio_bin.keys():
        arr_loss_ratio_bin = np.where(
            (np.isnan(arr_loss_ratio_bin)) & (out_df['loss_ratio'].values <= dict_loss_ratio_bin[bin_class]),
            int(bin_class),
            arr_loss_ratio_bin
        )

    arr_loss_ratio_bin = np.nan_to_num(arr_loss_ratio_bin, nan=0.0)
    
    out_df['loss_ratio_class'] = arr_loss_ratio_bin
    
    return out_df