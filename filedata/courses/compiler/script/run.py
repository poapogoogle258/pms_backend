from inginious_container_api import feedback
from inginious_container_api import run_student
from inginious_container_api import input

import time
import datetime
import tracemalloc

try:
    results_memory = []
    results_rumtime = []

    inputfile = input._load_input()['input']
    testcase = inputfile['testcase']
    deadline = datetime.datetime.strptime(inputfile['deadline'], '%Y-%m-%dT%H:%M:%S.%fZ') if inputfile['deadline']!=None else None

    if not inputfile['fixanswer']:
        testcase['output'] = [output.lower().strip() for output in testcase['output']]

    input.parse_template(r"template.py",r"student/student_code.py")
    error = False
 
    for i in range(len(testcase['output'])):
        if testcase['input'][i] != '':
            time_start = time.time()
            tracemalloc.start()
            stdout, stderr, retval = run_student.run_student_simple(r'python3 student/student_code.py', cmd_input=testcase['input'][i].strip()+'\n')
            time_usege = time.time() - time_start;
            memory_usege = tracemalloc.get_tracemalloc_memory()
            tracemalloc.stop()
            results_memory.append(memory_usege)
            results_rumtime.append(time_usege)    

        else:
            time_start = time.time()
            tracemalloc.start()
            stdout, stderr, retval = run_student.run_student_simple(r'python3 student/student_code.py')
            time_usege = time.time() - time_start;
            memory_usege = tracemalloc.get_tracemalloc_memory()
            tracemalloc.stop()
            results_memory.append(memory_usege)
            results_rumtime.append(time_usege)

        if stderr:
            feedback.set_global_feedback(str(stderr))
            error = True
            break
            
        if not inputfile['fixanswer']:
            stdout = stdout.lower()

        if stdout.strip() != testcase['output'][i].strip():
            feedback.set_global_feedback("data set {}: your answer:{} ,real answer: {}".format(i+1,stdout,testcase['output'][i]))
            error = True
            break

    if not error:
        feedback.set_global_result("success")
        feedback.set_custom_value('memory', sum(results_memory)/len(results_memory))
        feedback.set_custom_value('runtime', sum(results_rumtime)/len(results_rumtime))
        if deadline==None or input.get_submission_time() < deadline:
            feedback.set_custom_value("status_work",'success')
            feedback.set_grade(inputfile['score'])
        else:
            feedback.set_custom_value("status_work",'late')
            feedback.set_grade(inputfile['score_late'])
            
    else:
        feedback.set_global_result("failed")
        feedback.set_custom_value("status_work",'failed')
        feedback.set_grade(0)

except Exception as ex:
    feedback.set_global_result("failed")
    feedback.set_global_feedback("server not available now {}".format(ex))        

