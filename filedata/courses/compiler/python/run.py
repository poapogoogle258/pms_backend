from inginious_container_api import feedback
from inginious_container_api import run_student
from inginious_container_api import input


try:
    inputfile = input.get_input('student_code')

    inputfile = input._load_input()['input']

    input.parse_template(r"template.py",r"student/student_code.py")

    if 'input' in inputfile:
        student_input = inputfile['input']
        stdout, stderr, retval = run_student.run_student_simple(r'python3 student/student_code.py', cmd_input=student_input.strip() + '\n')
        
    else :
        stdout, stderr, retval = run_student.run_student_simple(r'python3 student/student_code.py')
    
    if stderr:
        feedback.set_global_result('error')
        feedback.set_global_feedback(str(stderr))
    else:
        feedback.set_global_result('complete')
        feedback.set_global_feedback(str(stdout))

except Exception as ex:
    # feedback.set_global_result('server not available now')
    feedback.set_global_feedback(str(ex))
