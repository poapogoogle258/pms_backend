import flask
import json

import re

from flask_cors import CORS

from inginious.client.client_sync import ClientSync


def keep_only_config_return_values(self, job_return):
    """ Keep only some useful return values """
    return {key: value for key, value in job_return.items() if return_fields.match(key)}

def pre_process(text):
    #remove comment write '#'
    text = text.lower()
    deleted_comment = re.sub(r'(#.*\n?)|(/\*.*?\*/|//[^\r\n]*\n)', '', text)
    deleted_string = re.sub(r"(\".*?\"|\'.*?\')", '', deleted_comment)
    
    return deleted_string

def init(plugin_manager, course_factory, client, config):
    """ Init the plugin """
    print("open new service simple compiler")

    app = plugin_manager._flask_app
    cors = CORS(app,supports_credentials=True)

    @app.route('/api/simple_compiler/python3',methods = ['POST'])
    def runcode_python():
        """
            req = {
                student_code : str
                fixanswer : bool
                accept : list
                notaccept : list
                input : str
                testcase : list
            }
        """
        #fix task for run script been saved in taskfile 
        user_input = flask.request.get_json(force = True)


        #check keywords in test submit mode
        if 'testcase' in user_input:
            code_without_comment = pre_process(user_input['student_code'])
            for keyword in user_input['accept']:
                if not re.findall(r"\b"+keyword+r"\b" ,code_without_comment):
                    return { 'result' : ['failed',f"ในคำตอบไม่พบ keyword :'{keyword}'"] ,'status' :'done'},200
            for keyword in user_input['notaccept']:
                if re.findall(r"\b"+keyword+r"\b",code_without_comment):
                    return { 'result' : ['failed',f"ในคำตอบห้าม keyword :'{keyword}'"] ,'status' :'done'},200

            del user_input['accept']
            del user_input['notaccept']
        
        compiler_nomal = { 
            'courseid':'compiler',
            'taskid':'python',
            'problemid':'python3'}

        compiler_step_by_stet = {
            'courseid':'compiler',
            'taskid':'python_step_by_step',
            'problemid':'python3'}
        
        compiler_testcase = {
            'courseid':'compiler',
            'taskid':'python3_casetast',
            'problemid':'python3'}

        compiler = compiler_testcase if 'testcase' in user_input else compiler_nomal

        client_sync = ClientSync(client)

        course = course_factory.get_course(compiler['courseid'])
        task = course.get_task(compiler['taskid'])
       
        try:
            result, grade, problems, tests, custom, state, archive, stdout, stderr = client_sync.new_job(0, task, user_input, "Plugin - Simple compiler python")
            job_return = {"result": result ,"stdout": stdout, "stderr": stderr}
        except Exception as ex :
            return {"status": "error", "status_message": "An internal error occurred"}, 500

        return {"status": "done","result": result }, 200


        