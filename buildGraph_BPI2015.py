'''
Created on 29/mag/2019

@author: nino
'''


from lxml import etree
# import datetime
# import numpy as np 

def buildGraph(filename):
    
    graph = open('graph_BPI_2015.txt','w')
    
    tree = etree.parse(filename)
    root = tree.getroot()
    
    c_name = -1

    for element in root.iter():
        
        if(element.tag.endswith('trace')):
            
            vector_events = []
            
#            cluster = ''#nominal (label: 1,2,3,4,5)           
#             delta_df = ''#sequence of delta timestamps
#             previous_dateFinished = 'null'
# #             delta_dd = ''#sequence of delta timestamps
# #             previous_dueDate = 'null'
#             delta_p = ''#sequence of delta timestamps
#             previous_planned = 'null'
#             delta = ''#sequence of delta timestamps
#             previous_timestamp = 'null'
#             
#             min_date_df = datetime.date(2030, 1, 1)
#             max_date_df = datetime.date(2000, 1, 1)
#             min_date_p = datetime.date(2030, 1, 1)
#             max_date_p = datetime.date(2000, 1, 1)
#             min_date = datetime.date(2030, 1, 1)
#             max_date = datetime.date(2000, 1, 1)
            
            c_name += 1
            
            avg_SUMleges = 0
            counter_avg_SUMleges = 0
            
            for childelement in element.iterchildren():
                               
                key = childelement.attrib.get('key')
                value = childelement.attrib.get('value')
                is_term_name = False
                is_SUMleges = False
#                 is_planned = False
                is_parts = False
                is_action_code = False
                is_responsible_actor = False
                is_last_phase = False
                is_artificial = False
                
                if(key == 'cluster:label'):
                    cluster = value
                    
#                 if(key == 'concept:name'):
#                     c_name = value
                                
                elif (childelement.tag.endswith('event')):
                    
                    for grandchildelement in childelement.iterchildren():

                        key = grandchildelement.attrib.get('key')
                        value = grandchildelement.attrib.get('value')
                                                
                        if value == 'artificial':
                            is_term_name = True
                            is_SUMleges = True
#                             is_planned = True
                            is_parts = True
                            is_action_code = True
                            is_responsible_actor = True
                            is_last_phase = True
                            is_artificial = True
                            break
                        
                        elif key == '(case)_SUMleges':
                            case_SUMleges = value
                            is_SUMleges = True
                            avg_SUMleges += float(value)
                            counter_avg_SUMleges += 1
                            
#                         elif key == 'dateFinished':
#                             dateFinished = datetime.datetime.strptime(value[:10], '%Y-%m-%d').date()
#                             min_date_df = min(min_date_df,dateFinished)
#                             max_date_df = max(max_date_df,dateFinished)
#                             
#                             if(previous_dateFinished == 'null'):
#                                 difference_df = '0'
#                             else:
#                                 difference_df = str((dateFinished - previous_dateFinished).days)
#                             
#                             delta_df += difference_df+'/'
#                             
#                             previous_dateFinished = dateFinished
                            
                        elif key == 'action_code':
                            is_action_code = True
                            action_code = value.replace('_','')
                            
                        elif key == 'activityNameEN':
                            activityNameEN = value.replace('-','').replace(' ','').replace(':','').replace('.','').replace(',','')
                            
#                         elif key == 'planned':
#                             is_planned = True
#                             planned = datetime.datetime.strptime(value[:10], '%Y-%m-%d').date()
#                             min_date_p = min(min_date_p,planned)
#                             max_date_p = max(max_date_p,planned)
#                             
#                             if(previous_planned == 'null'):
#                                 difference_p = '0'
#                             else:
#                                 difference_p = str((planned - previous_planned).days)
#                             
#                             delta_p += difference_p+'/'
#                             
#                             previous_planned = planned
                            
                        elif key == '(case)_caseStatus':
                            case_caseStatus = value
                           
                        elif key == '(case)_Responsible_actor':
                            is_responsible_actor = True
                            case_Responsible_actor = value
                           
                        elif key == 'concept:name':
                            concept_name = value.replace('_','')
                           
                        elif key == '(case)_last_phase':
                            is_last_phase = True
                            case_last_phase = value.replace(' ','')
                        
                        elif key == '(case)_requestComplete':
                            if(value == 'TRUE'):
                                case_requestComplete = '1'
                            else:
                                case_requestComplete = '0'
                        
                        elif key == '(case)_parts':
                            is_parts = True
                            case_parts = value.replace(',','').replace(' ','').replace('(','').replace(')','').replace('/','').replace('-','').replace(':','').replace('.','')
                        
                        elif key == 'question':
                            if value == 'True' or value == 'False' or value == 'EMPTY':
                                question = value
                            else:
                                question = 'EMPTY'
                        
                        elif key == '(case)_termName':
                            is_term_name = True
                            case_termName = value.replace(' ','')
                           
#                         elif(key == 'time:timestamp'):
#                             timestamp = datetime.datetime.strptime(value[:10], '%Y-%m-%d').date()
#                             min_date = min(min_date,timestamp)
#                             max_date = max(max_date,timestamp)
#                             
#                             if(previous_timestamp == 'null'):
#                                 difference = '0'
#                             else:
#                                 difference = str((timestamp - previous_timestamp).days)
#                             
#                             delta += difference+'/'
#                             
#                             previous_timestamp = timestamp
                           
                        elif key == 'monitoringResource':
                            monitoringResource = value
                           
                        elif key == 'org:resource':
                            org_resource = value
                           
                    if not is_term_name:
                        case_termName = 'EMPTY'
                        
                    if not is_SUMleges:
                        case_SUMleges = 'EMPTY'
                    
#                     if not is_planned:
#                         delta_p += '0/'
                        
                    if not is_parts:
                        case_parts = 'EMPTY'
                        
                    if not is_action_code:
                        action_code = 'EMPTY'
                        
                    if not is_responsible_actor:
                        case_Responsible_actor = 'EMPTY'
                        
                    if not is_last_phase:
                        case_last_phase = 'EMPTY'
                    
                    if not is_artificial:    
                        event = 'e_' + str(c_name) + '_' + concept_name
                        vector_events.append(event)
                        
                        graph.write(event + ' eventName_' + concept_name + '\n')
                        graph.write(event + ' SUMleges_' + case_SUMleges + '\n')
                        graph.write(event + ' action_code_' + action_code + '\n')
                        graph.write(event + ' activityNameEN_' + activityNameEN + '\n')
                        graph.write(event + ' caseStatus_' + case_caseStatus + '\n')
                        graph.write(event + ' Responsible_actor_' + case_Responsible_actor + '\n')
                        graph.write(event + ' last_phase_' + case_last_phase + '\n')
                        graph.write(event + ' requestComplete_' + case_requestComplete + '\n')
                        graph.write(event + ' parts_' + case_parts + '\n')
                        graph.write(event + ' question_' + question + '\n')
                        graph.write(event + ' termName_' + case_termName + '\n')
                        graph.write(event + ' monitoringResource_' + monitoringResource + '\n')
                        graph.write(event + ' org_resource_' + org_resource + '\n')
                       
                    
             
#             duration = 0
#             duration_p = 0
#             duration_df = 0               
#             
#             diff = (max_date - min_date).days
#             
#             if(diff > 0):
#                 duration = str(diff)
#                 
#             diff_df = (max_date_df - min_date_df).days
#             
#             if(diff_df > 0):
#                 duration_df = str(diff_df)
#                 
#             diff_p = (max_date_p - min_date_p).days
#             
#             if(diff_p > 0):
#                 duration_p = str(diff_p)
#                 
#             
#             delta = delta[:len(delta)-1]
#             delta_p = delta_p[:len(delta_p)-1]
#             delta_df = delta_df[:len(delta_df)-1]

            graph.write('trace_' + str(c_name) + ' ' + vector_events[0] + '\n')
            
            for i in range(1,len(vector_events)-1):
                graph.write(vector_events[i] + ' ' + vector_events[i+1] + '\n')
            
    graph.close()
        

buildGraph('progetto/input/BPIC15GroundTruth.xes')