from inginious_container_api import feedback
from inginious_container_api import run_student
from inginious_container_api import input


try:
    inputfile = input._load_input()['input']

    testcase = inputfile['testcase']

    fixanswer = inputfile['fixanswer']


    input.parse_template(r"template.py",r"student/student_code.py")


    error = False

    for i in range(len(testcase['output'])):

        if testcase['input'][i].strip() != '':
            student_input = testcase['input'][i].strip()
            stdout, stderr, retval = run_student.run_student_simple(r'python3 student/student_code.py', cmd_input=student_input+'\n')
            
        else :
            stdout, stderr, retval = run_student.run_student_simple(r'python3 student/student_code.py')
        
        if stderr :
            feedback.set_global_result('error')
            feedback.set_global_feedback(str(stderr))
            error = True
              
        elif fixanswer and stdout.strip() != testcase['output'][i].strip():
            feedback.set_global_result('failed')
            feedback.set_global_feedback('ไม่ผ่านชุดแบบทดสอบที่ {} ,answer : {} ,output: {} '.format(i+1,testcase['output'][i].strip(),stdout.strip()))
            error = True
            break;

        elif not fixanswer:
            output = stdout.lower().strip().replace(" ","").replace("\t","")
            testcase_output = testcase['output'][i].lower().strip().replace(" ","").replace("\t","")
            if output != testcase_output:
                feedback.set_global_result('failed')
                feedback.set_global_feedback('ไม่ผ่านชุดแบบทดสอบที่ {} ,answer : {} ,output: {} '.format(i+1,testcase['output'][i].strip(),stdout.strip()))
                error = True
                break;

    if  not error:
        feedback.set_global_result('complete')
        feedback.set_global_feedback('ผ่านทุกแบบทดสอบ')

except Exception as ex:
    feedback.set_global_result('crash')
    feedback.set_global_feedback(str(ex))



    


        


