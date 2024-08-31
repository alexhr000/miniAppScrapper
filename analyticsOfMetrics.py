import json
import time
import glob
import os



list_of_files = glob.glob('json/metrics/*') 
latest_file = max(list_of_files, key=os.path.getctime) 
latest_file = latest_file.replace('/','\\') # путь к последнему файлу метрики


def get_metrics(previous_metric, name_of_the_period):

    last_week_res = []
    last_week_counter = 0
    this_week_res = []
    this_week_counter = 0
    departed_miniapps_list = []
    appeared_miniapps_list = []

    with open(previous_metric, 'r', encoding='utf-8') as file:
        last_week_json_data = json.load(file)
        last_week_sorted_obj = dict(last_week_json_data) 
        last_week_sorted_obj = sorted(last_week_json_data, key=lambda x : x['bot_monthly_users'], reverse=True)
        for item in last_week_sorted_obj:  
            last_week_counter = last_week_counter + 1
            last_week_res.append(
                {
                'bot_name': item['bot_name'],
                'bot_monthly_users': item["bot_monthly_users"],
                'place_in_the_top': last_week_counter
                }
            )

    with open(latest_file, 'r', encoding='utf-8') as file:
        this_week_json_data = json.load(file)
        this_week_sorted_obj = dict(this_week_json_data) 
        this_week_sorted_obj = sorted(this_week_json_data, key=lambda x : x['bot_monthly_users'], reverse=True)
        for item in this_week_sorted_obj:  
            this_week_counter = this_week_counter + 1
            this_week_res.append(
                {
                'bot_name': item['bot_name'],
                'bot_monthly_users': item["bot_monthly_users"],
                'place_in_the_top': this_week_counter
                }
            )


    print(f'\n Изменение в рейтинге miniApp за {name_of_the_period}:', end='\n\n')


    break_out_flag = False

    for last_week_item in last_week_res: 
        for this_week_item in this_week_res:    
            if this_week_item['bot_name'] == last_week_item['bot_name']:
                print(f'miniApp: {this_week_item["bot_name"]} | прирост числа пользовтаелй: {this_week_item["bot_monthly_users"]-last_week_item["bot_monthly_users"]} | изменение места в топе: {last_week_item["place_in_the_top"] - this_week_item["place_in_the_top"]}  [{last_week_item["place_in_the_top"]} >> {this_week_item["place_in_the_top"]}] ')



    for last_week_item in last_week_res: 
        break_out_flag = True
        for this_week_item in this_week_res:  
        
            if this_week_item['bot_name'] == last_week_item['bot_name']:          
                break_out_flag = False
                break
        if break_out_flag:
            departed_miniapps_list.append(last_week_item)
        
    for this_week_item in this_week_res:  
        break_out_flag = True
        for last_week_item in last_week_res:   
        
            if last_week_item['bot_name'] == this_week_item['bot_name']:           
                break_out_flag = False
                break
        if break_out_flag:
            appeared_miniapps_list.append(this_week_item)


    if(departed_miniapps_list):
        print('\n Пропали из топа: \n')
        for departed_miniapp in departed_miniapps_list:
            print(f'{departed_miniapp["bot_name"]} - {departed_miniapp["bot_monthly_users"]} пользователей в месяц, до этого {departed_miniapp["place_in_the_top"]} место в топе ')

    if(appeared_miniapps_list):
        print('\n Новые в топе: \n')
        for appeared_miniapp in appeared_miniapps_list:
            print(f'{appeared_miniapp["bot_name"]} - {appeared_miniapp["bot_monthly_users"]} пользователей в месяц, {appeared_miniapp["place_in_the_top"]} место в топе ')
    
    
    print('==========================================')



get_metrics("json\metrics\metrics 20.03_22.07.24.json", 'месяц')
get_metrics("json\metrics\metrics 18.15_17.08.24.json", 'неделю')  
get_metrics("json\metrics\metrics 18.15_24.08.24.json", 'день')  