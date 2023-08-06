import pandas as pd
import numpy as np
from zkyhaxpy import np_tools, dict_tools


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



def get_loss_type_class_numpy(in_df, in_dict_master_config):
    '''
    Get loss class for given plant info data    
    '''
    dict_loss_type_class = in_dict_master_config['dict_loss_type_class']
    out_df = in_df.copy()
    out_df['loss_type_class'] = dict_tools.map_dict(out_df['DANGER_TYPE_NAME'].values, dict_loss_type_class, 0)
    out_df['loss_type_class'] = np.where(
        (out_df['loss_type_class'].values==0) & (out_df['TOTAL_DANGER_AREA_IN_WA'].values>0),
        3,
        out_df['loss_type_class'].values
    )
    
    return out_df


def get_loss_info(
    in_df,
    in_dict_master_config,
    danger_area_col = 'total_danger_area_in_wa',
    plant_area_col='total_actual_plant_area_in_wa',
    target_info=['loss_type_class', 'loss_ratio_class', 'target_f'],
    near_real_time=False, seperate_loss_type=True
):

    '''
    Get loss info for model training    
    '''

    out_df = in_df.copy()
    if 'loss_type_class' in target_info:
        #get loss ratio    
        out_df = get_loss_type_class_numpy(out_df, in_dict_master_config)

    if 'loss_ratio_class' in target_info:
        #get loss ratio    
        out_df = get_loss_ratio_and_class(out_df, in_dict_master_config, danger_area_col, plant_area_col)
    
    if 'target_f' in target_info:
        #target_f
        out_df = get_target_f(out_df, near_real_time, seperate_loss_type)
   
    return out_df


def get_last_digit_ext_act_id(in_df, last_n_digits=1, out_col_nm='last_digit_ext_act_id'):
    '''
    Get last N digits of ext_act_id

    Output
    ----------------------------
    A pandas dataframe
    '''
    out_df = in_df.copy()
    out_df[out_col_nm] = np_tools.get_last_n_digit(out_df['ext_act_id'], last_n_digits)
    return out_df



def get_target_f(in_df, near_real_time=False, seperate_loss_type=True):
    '''
    Get target flag for each loss_type_class. 
    If near real time is true, target_f will consider image date.    
    '''

    assert('loss_ratio_class' in in_df.columns)
    assert('loss_type_class' in in_df.columns)    
    assert('START_DATE' in in_df.columns)
    if near_real_time==True:
        assert('img_date' in in_df.columns)
    
    out_df = in_df.copy()

    if seperate_loss_type==True:
        for loss_type_class in [1, 2, 3]:
            if loss_type_class == 1:
                out_target_f_col_nm = 'target_f_drought'
            elif loss_type_class == 2:
                out_target_f_col_nm = 'target_f_flood'
            elif loss_type_class == 3:
                out_target_f_col_nm = 'target_f_other'
            
            if near_real_time==True:        
                out_df[out_target_f_col_nm] = np.where(
                    (out_df['loss_type_class'].values == loss_type_class) 
                    & (out_df['START_DATE'].values <= out_df['img_date'].values),
                    out_df['loss_ratio_class'].values,
                    0
                )
            else:
                out_df[out_target_f_col_nm] = np.where(
                    out_df['loss_type_class'].values == loss_type_class,
                    out_df['loss_ratio_class'].values,
                    0
                )
    else:
        if near_real_time==True:        
                out_df['target_f'] = np.where(                    
                    out_df['START_DATE'].values <= out_df['img_date'].values,
                    out_df['loss_ratio_class'].values,
                    0
                )
        else:
            out_df['target_f'] = out_df['loss_ratio_class'].values                            
    return out_df


def get_tambon_pcode(    
    in_df,
    prov_cd_col='plant_province_code',
    amphur_cd_col='plant_amphur_code',
    tambon_cd_col='plant_tambon_code',
    ):
    '''
    Get Tambon P Code for given data frame
    '''

    out_df = in_df.copy()
    assert(out_df[prov_cd_col].dtype == int)
    assert(out_df[amphur_cd_col].dtype == int)
    assert(out_df[tambon_cd_col].dtype == int)

    out_df['tambon_pcode'] = (out_df[prov_cd_col] * 10000) + (out_df[amphur_cd_col] * 100) + + (out_df[tambon_cd_col])
    return out_df


def get_cluster_id(in_df, in_df_tambon_cluster):
    '''
    Add cluster id column.
    '''
    out_df = in_df.copy()
    tmp_df_tambon_cluster = in_df_tambon_cluster.copy()
    if 'tambon_pcode' in out_df.columns:
        pass
    else:
        out_df = get_tambon_pcode(out_df)
    
    if 'tambon_pcode' in tmp_df_tambon_cluster.columns:
        pass
    else:
        tmp_df_tambon_cluster = get_tambon_pcode(tmp_df_tambon_cluster)
    
        
    dict_tambon_cluster = tmp_df_tambon_cluster.set_index('tambon_pcode')['full_cluster_id'].squeeze().to_dict()
    
    #get default cluster for each province
    df_prov_default_cluster = tmp_df_tambon_cluster.groupby(['plant_province_code','full_cluster_id'], as_index=False).agg(count=pd.namedagg(column='tambon_pcode', aggfunc='size'))
    df_prov_default_cluster = df_prov_default_cluster.sort_values('count', ascending=False).drop_duplicates(['plant_province_code'])
    dict_prov_default_cluster =  df_prov_default_cluster.set_index('plant_province_code')['full_cluster_id'].squeeze().to_dict()
    
    arr_default_cluster = dict_tools.map_dict(out_df['plant_province_code'].values, dict_prov_default_cluster)
    out_df['cluster_id'] = dict_tools.map_dict(out_df['tambon_pcode'].values, dict_tambon_cluster, arr_default_cluster)
 
    return out_df
    
    
    
    
    

def get_breed_info(in_df, in_df_breed_info, in_region_cd):
    '''
    Get breed info columns
    '''
    #get photo sensitivity, rice type & breed rice age
    df_breed_info = in_df_breed_info.copy()

    #Get dict of photo sensitive
    dict_breed_photo_sensitive = df_breed_info.set_index('breed_code')['photo_sensitive_f'].squeeze().to_dict()

    #Get breed rice age
    df_breed_rice_age = df_breed_info.iloc[:, [0] + list(range(-4, 0))].melt(id_vars=['breed_code'])
    df_breed_rice_age = df_breed_rice_age.rename(columns={'variable':'region', 'value':'days'})
    df_breed_rice_age['region'] = df_breed_rice_age['region'].str.replace('rice_age_days_', '').map({'central':'c', 'north':'n', 'northeast':'ne', 'south':'s'})
    dict_breed_rice_age = {}
    for region, df_curr in df_breed_rice_age.groupby('region'):
        dict_breed_rice_age[region] = df_curr.set_index('breed_code')['days'].squeeze().to_dict()

    dict_breed_sticky_rice = df_breed_info.set_index('breed_code')['sticky_rice_f'].squeeze().to_dict()
    dict_breed_jasmine_rice = df_breed_info.set_index('breed_code')['jasmine_rice_f'].squeeze().to_dict()

    

    #Get default rice age & photo sensitive from weighted average 
    default_rice_age = int(round(np.sum(df_breed_info['act_count_2015_to_2019'] * df_breed_info.iloc[:, -4:].mean(axis=1)) / np.sum(df_breed_info['act_count_2015_to_2019'])))
    default_photo_sensitive = int(round(np.sum(df_breed_info['act_count_2015_to_2019'] * df_breed_info['photo_sensitive_f']) / np.sum(df_breed_info['act_count_2015_to_2019'])))
    default_sticky_rice = int(round(np.sum(df_breed_info['act_count_2015_to_2019'] * df_breed_info['sticky_rice_f']) / np.sum(df_breed_info['act_count_2015_to_2019'])))
    default_jasmine_rice = int(round(np.sum(df_breed_info['act_count_2015_to_2019'] * df_breed_info['jasmine_rice_f']) / np.sum(df_breed_info['act_count_2015_to_2019'])))

    out_df = in_df.copy()

    out_df['photo_sensitive_f'] = dict_tools.map_dict(out_df['breed_code'].values, dict_breed_photo_sensitive, default_photo_sensitive)
    out_df['sticky_rice_f'] = dict_tools.map_dict(out_df['breed_code'].values, dict_breed_sticky_rice, default_sticky_rice)
    out_df['jasmine_rice_f'] = dict_tools.map_dict(out_df['breed_code'].values, dict_breed_jasmine_rice, default_jasmine_rice)
    out_df['rice_age_days'] = dict_tools.map_dict(out_df['breed_code'].values, dict_breed_rice_age[in_region_cd], default_rice_age)
      

    return out_df


