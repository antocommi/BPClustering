'''
Created on 13/mar/2019

@author: nino
'''

from lxml import etree
import datetime
import numpy as np 

def build(filename):
    
    data = []

    tree = etree.parse(filename)
    root = tree.getroot()

    for element in root.iter():
        
        if(element.tag.endswith('trace')):
            
            cluster = ''#nominal (label: 1,2,3,4,5)
            case_SUMleges_seq = ''#sequence of float
            action_code_seq = ''#sequence of nominal
            activityNameEN_seq = ''#sequence of nominal
            case_caseStatus_seq = ''#sequence of nominal
            case_Responsible_actor_seq = ''#sequence of nominal
            concept_name_seq = ''#sequence of nominal
            case_last_phase_seq = ''#sequence of nominal
            case_requestComplete_seq = ''#sequence of boolean
            case_parts_seq = ''#sequence of nominal
            question_seq = ''#sequence of nominal
            case_termName_seq = ''#sequence of nominal
            monitoringResource_seq = ''#sequence of nominal
            org_resource_seq = ''#sequence of nominal
#             case_IDofConceptCase_seq = ''#sequence of nominal
           
            delta_df = ''#sequence of delta timestamps
            previous_dateFinished = 'null'
#             delta_dd = ''#sequence of delta timestamps
#             previous_dueDate = 'null'
            delta_p = ''#sequence of delta timestamps
            previous_planned = 'null'
            delta = ''#sequence of delta timestamps
            previous_timestamp = 'null'
            
            min_date_df = datetime.date(2030, 1, 1)
            max_date_df = datetime.date(2000, 1, 1)
            min_date_p = datetime.date(2030, 1, 1)
            max_date_p = datetime.date(2000, 1, 1)
            min_date = datetime.date(2030, 1, 1)
            max_date = datetime.date(2000, 1, 1)
            
            c_name = ''
            
            avg_SUMleges = 0
            counter_avg_SUMleges = 0
            
            for childelement in element.iterchildren():
                               
                key = childelement.attrib.get('key')
                value = childelement.attrib.get('value')
                is_term_name = False
                is_SUMleges = False
                is_planned = False
                is_parts = False
                is_action_code = False
                is_responsible_actor = False
                is_last_phase = False
                if(key == 'cluster:label'):
                    cluster = value
                    
                if(key == 'concept:name'):
                    c_name = value
                                
                elif (childelement.tag.endswith('event')):
                    
                    for grandchildelement in childelement.iterchildren():
#                         is_IDofConceptCase = False
                        key = grandchildelement.attrib.get('key')
                        value = grandchildelement.attrib.get('value')
                                                
                        if value == 'artificial':
                            is_term_name = True
                            is_SUMleges = True
                            is_planned = True
                            is_parts = True
                            is_action_code = True
                            is_responsible_actor = True
                            is_last_phase = True
                            break
                        #agguinto
                        elif key == '(case)_cluster:label':
                            cluster=value
                        
                        elif key == '(case)_SUMleges':
                            case_SUMleges_seq += value + '/'
                            is_SUMleges = True
                            avg_SUMleges += float(value)
                            counter_avg_SUMleges += 1
                            
                        elif key == 'dateFinished':
                            dateFinished = datetime.datetime.strptime(value[:10], '%Y-%m-%d').date()
                            min_date_df = min(min_date_df,dateFinished)
                            max_date_df = max(max_date_df,dateFinished)
                            
                            if(previous_dateFinished == 'null'):
                                difference_df = '0'
                            else:
                                difference_df = str((dateFinished - previous_dateFinished).days)
                            
                            delta_df += difference_df+'/'
                            
                            previous_dateFinished = dateFinished
                        
#                         elif key == 'dueDate':
#                             dueDate = datetime.datetime.strptime(value[:10], '%Y-%m-%d').date()
#                             min_date = min(min_date,dueDate)
#                             max_date = max(max_date,dueDate)
#                             
#                             if(previous_dueDate == 'null'):
#                                 difference_dd = '0'
#                             else:
#                                 difference_dd = str((dueDate - previous_dueDate).days)
#                             
#                             delta_dd += difference_dd+'/'
#                             
#                             previous_dueDate = dueDate
                            
                        elif key == 'action_code':
                            is_action_code = True
                            action_code_seq += value.replace('_','') + '/'
                            
                        elif key == 'activityNameEN':
                            activityNameEN_seq += value.replace('-','').replace(' ','').replace(':','').replace('.','').replace(',','') + '/'
                            
                        elif key == 'planned':
                            is_planned = True
                            planned = datetime.datetime.strptime(value[:10], '%Y-%m-%d').date()
                            min_date_p = min(min_date_p,planned)
                            max_date_p = max(max_date_p,planned)
                            
                            if(previous_planned == 'null'):
                                difference_p = '0'
                            else:
                                difference_p = str((planned - previous_planned).days)
                            
                            delta_p += difference_p+'/'
                            
                            previous_planned = planned
                            
                        elif key == '(case)_caseStatus':
                            case_caseStatus_seq += value + '/'
                           
                        elif key == '(case)_Responsible_actor':
                            is_responsible_actor = True
                            case_Responsible_actor_seq += value + '/'
                           
                        elif key == 'concept:name':
                            concept_name_seq += value.replace('_','') + '/'
                           
                        elif key == '(case)_last_phase':
                            is_last_phase = True
                            case_last_phase_seq += value.replace(' ','') + '/'
                        
                        elif key == '(case)_requestComplete':
                            if(value == 'TRUE'):
                                case_requestComplete_seq += '1/'
                            else:
                                case_requestComplete_seq += '0/'
                        
                        elif key == '(case)_parts':
                            is_parts = True
                            case_parts_seq += value.replace(',','').replace(' ','').replace('(','').replace(')','').replace('/','').replace('-','').replace(':','').replace('.','') + '/'
                        
                        elif key == 'question':
                            if value == 'True' or value == 'False' or value == 'EMPTY':
                                question_seq += value + '/'
                            else:
                                question_seq += 'EMPTY/'
                        
                        elif key == '(case)_termName':
                            case_termName_seq += value.replace(' ','') + '/'
                            is_term_name = True
                           
                        elif(key == 'time:timestamp'):
                            timestamp = datetime.datetime.strptime(value[:10], '%Y-%m-%d').date()
                            min_date = min(min_date,timestamp)
                            max_date = max(max_date,timestamp)
                            
                            if(previous_timestamp == 'null'):
                                difference = '0'
                            else:
                                difference = str((timestamp - previous_timestamp).days)
                            
                            delta += difference+'/'
                            
                            previous_timestamp = timestamp
                           
                        elif key == 'monitoringResource':
                            monitoringResource_seq += value + '/'
                           
                        elif key == 'org:resource':
                            org_resource_seq += value + '/'
                           
#                         elif key == '(case)_IDofConceptCase':
#                             case_IDofConceptCase_seq += value + '/'
#                             is_IDofConceptCase = True
                        
                    if not is_term_name:
                        case_termName_seq += 'EMPTY/'
                        
                    if not is_SUMleges:
                        case_SUMleges_seq += 'EMPTY/'
                    
                    if not is_planned:
                        delta_p += '0/'
                        
                    if not is_parts:
                        case_parts_seq += 'EMPTY/'
                        
                    if not is_action_code:
                        action_code_seq += 'EMPTY/'
                        
                    if not is_responsible_actor:
                        case_Responsible_actor_seq += 'EMPTY/'
                        
                    if not is_last_phase:
                        case_last_phase_seq += 'EMPTY/'
                        
                        
                            
#                         if not is_IDofConceptCase:
#                             case_IDofConceptCase_seq += 'EMPTY/'
             
            duration = 0
            duration_p = 0
            duration_df = 0               
            
            diff = (max_date - min_date).days
            
            if(diff > 0):
                duration = str(diff)
                
            diff_df = (max_date_df - min_date_df).days
            
            if(diff_df > 0):
                duration_df = str(diff_df)
                
            diff_p = (max_date_p - min_date_p).days
            
            if(diff_p > 0):
                duration_p = str(diff_p)
                
            
            delta = delta[:len(delta)-1]
            delta_p = delta_p[:len(delta_p)-1]
            delta_df = delta_df[:len(delta_df)-1]
            
            if avg_SUMleges > 0 and counter_avg_SUMleges > 0:
                avg_SUMleges = avg_SUMleges/counter_avg_SUMleges
                case_SUMleges_seq = case_SUMleges_seq.replace('EMPTY',str(avg_SUMleges))
            elif avg_SUMleges == 0 and counter_avg_SUMleges == 0:
                case_SUMleges_seq = case_SUMleges_seq.replace('EMPTY','0')
                    
            case_SUMleges_seq = case_SUMleges_seq[:len(case_SUMleges_seq)-1]
            action_code_seq = action_code_seq[:len(action_code_seq)-1]
            activityNameEN_seq = activityNameEN_seq[:len(activityNameEN_seq)-1]
            case_caseStatus_seq = case_caseStatus_seq[:len(case_caseStatus_seq)-1]
            case_Responsible_actor_seq = case_Responsible_actor_seq[:len(case_Responsible_actor_seq)-1]
            concept_name_seq = concept_name_seq[:len(concept_name_seq)-1]
            case_last_phase_seq = case_last_phase_seq[:len(case_last_phase_seq)-1]
            case_requestComplete_seq = case_requestComplete_seq[:len(case_requestComplete_seq)-1]
            case_parts_seq = case_parts_seq[:len(case_parts_seq)-1]
            question_seq = question_seq[:len(question_seq)-1]
            case_termName_seq = case_termName_seq[:len(case_termName_seq)-1]
            monitoringResource_seq = monitoringResource_seq[:len(monitoringResource_seq)-1]
            org_resource_seq = org_resource_seq[:len(org_resource_seq)-1]
            #case_IDofConceptCase_seq = case_IDofConceptCase_seq[:len(case_IDofConceptCase_seq)-1]
            
#             vec1 = case_SUMleges_seq.split('/')
#             vec2 = action_code_seq.split('/')
#             vec3 = activityNameEN_seq.split('/')
#             vec4 = case_caseStatus_seq.split('/')
#             vec5 = case_Responsible_actor_seq.split('/')
#             vec6 = concept_name_seq.split('/')
#             vec7 = case_last_phase_seq.split('/')
#             vec8 = case_requestComplete_seq.split('/')
#             vec9 = case_parts_seq.split('/')
#             vec10 = question_seq.split('/')
#             vec11 = case_termName_seq.split('/')
#             vec12 = monitoringResource_seq.split('/')
#             vec13 = org_resource_seq.split('/')
#             vec14 = delta.split('/')
#             vec15 = delta_p.split('/')
#             vec16 = delta_df.split('/')
#             
#             if not (len(vec1) == len(vec2) and len(vec2) == len(vec3) and len(vec3) == len(vec4) and len(vec4) == len(vec5) and len(vec5) == len(vec6) and len(vec6) == len(vec7) and len(vec7) == len(vec8) and len(vec8) == len(vec9) and len(vec9) == len(vec10) and len(vec10) == len(vec11) and len(vec11) == len(vec12) and len(vec12) == len(vec13) and len(vec13) == len(vec14) and len(vec14) == len(vec15) and len(vec15) == len(vec16)):
#                 print(c_name)
#                 print(len(vec1))
#                 print(len(vec2))
#                 print(len(vec3))
#                 print(len(vec4))
#                 print(len(vec5))
#                 print(len(vec6))
#                 print(len(vec7))
#                 print(len(vec8))
#                 print(len(vec9))
#                 print(len(vec10))
#                 print(len(vec11))
#                 print(len(vec12))
#                 print(len(vec13))
#                 print(len(vec14))
#                 print(len(vec15))
#                 print(len(vec16))
#                 print()
            
            line = case_SUMleges_seq+','+action_code_seq+','+activityNameEN_seq+','+case_caseStatus_seq+','+case_Responsible_actor_seq+','+concept_name_seq+','+case_last_phase_seq+','+case_requestComplete_seq+','+case_parts_seq+','+question_seq+','+case_termName_seq+','+monitoringResource_seq+','+org_resource_seq+','+str(delta)+','+str(delta_p)+','+str(delta_df)+','+str(duration)+','+str(duration_df)+','+str(duration_p)+','+str(cluster)+'\n'
            data.append(line)        
           
    
    data = np.array(data)
    
    attributes_line = 'case_SUMleges_seq,action_code_seq,activityNameEN_seq,case_caseStatus_seq,case_Responsible_actor_seq,concept_name_seq,case_last_phase_seq,case_requestComplete_seq,case_parts_seq,question_seq,case_termName_seq,monitoringResource_seq,org_resource_seq,delta,delta_p,delta_df,duration,duration_df,duration_p,cluster\n'
    
    log2015 = open('BPI_2015.csv','w')
    log2015.write(attributes_line)
    
    for item in data:
        log2015.write(item)

    log2015.close()
        

build('progetto/input/BPIC15GroundTruth_ridotto2.xes')