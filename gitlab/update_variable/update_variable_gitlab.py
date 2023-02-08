import os
import gitlab
import json 
import logging
from modules.dictionary_grouping import processDict
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, filename ="logs/update_variable_gitlab.log", format="%(asctime)s - %(levelname)s - %(message)s")
logging.info(f"{20*'*'}RODANDO{20*'*'}")

#Definindo variáveis

load_dotenv()

access_token_personal=os.environ.get('access_token_personal')
access_token_rd=os.environ.get('access_token_rd')
id_group_personal=os.environ.get('id_group_personal')
id_group_rd=os.environ.get('id_group_rd')
count=int(os.environ.get('count'))
variable=os.environ.get('variable')
new_value_variable=os.environ.get('new_value_variable')
run_all=os.environ.get('run_all')
max_run=int(os.environ.get('max_run'))
url_gitlab=(os.environ.get('url_gitlab'))

# Dados (GitLab.com)

gl = gitlab.Gitlab()
gl = gitlab.Gitlab(url=url_gitlab, private_token=access_token_personal)
group = gl.groups.get(id_group_personal)
values_found={}

for iterator in group.subgroups.list(iterator=True):
            
    #Obtem nome e id de cada subgrupo        
     
    obj = json.loads(iterator.to_json(sort_keys=True, indent=4))
    id_subgroup = obj['id']
    name_subgroup = obj['name']
    
    #logging.info(name_subgroup, id_subgroup)
    
    #Verificando se existe a variável
       
    try:  
        subgroup = gl.groups.get(id_subgroup) 
        g_var = subgroup.variables.get(variable)
        g_var = g_var.to_json(sort_keys=True, indent=4)
        variable_aws = json.loads(g_var)
        name_variable = variable_aws['key']
        value_variable = variable_aws['value']  
        values_found.setdefault(name_subgroup,value_variable) #Adiciona o par Chave:Valor no dicionário values_found
        #logging.info(f"{name_subgroup} - {name_variable} - {value_variable}")  # Listar os subgrupos, com o valor da variável desejada
        
        #Fazendo a alteração do valor da variável
        
        if value_variable != new_value_variable and "grupo_teste__" in name_subgroup:
            subgroup.variables.update(variable, {"value": new_value_variable}) #Atualiza o valor da variável
            logging.info(f"A variável {variable} do subgrupo {name_subgroup} foi alterada! Antigo Valor: {value_variable}; Novo valor: {new_value_variable}")
            count += 1 
            if count >= max_run and run_all == None:
                break
        else:
            logging.info(f"A variável {variable} do subgrupo {name_subgroup} não precisa ser alterada!") 
            
    except:
        logging.info(f"O subgrupo {name_subgroup} não possui a variável {variable}!")  
        continue      
    
# logging.info(values_found)

result = processDict(values_found)
logging.info(f"{10*'*'}AGRUPAMENTO DOS SUBGRUPOS, COM SUAS RESPECTIVAS VARIÁVEIS{10*'*'}")
logging.info(f"{result}")
    

