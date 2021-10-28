import flask
import time
import json
import re

from inginious.common.custom_yaml import load, dump
from inginious.frontend.pages.api._api_page import  APIAuthenticatedPage

class tasks_service(APIAuthenticatedPage):

    def API_GET(self,courseid, taskid=None):
        
        username = self.user_manager.session_username()

        try:
            course = self.course_factory.get_course(courseid)
        except Exception as ex:
            return {"status":"error", "message":"Course not found"},500
            
        
        try:
            tasks = course.get_tasks() if taskid is None else {taskid: course.get_task(taskid)}
        except Exception as ex:
            return {'status':"error","message":"Problem not found"},500
            

        if not self.user_manager.course_is_user_registered(course,username):
            return {"message":"you not member this courses"}, 403

        outputs = {
            "courseid":courseid,
            "course_name":course.get_name(self.user_manager.session_language()),
            'is_admin' : self.user_manager.has_admin_rights_on_course(course,username),
            "tasks" : []
        }

        for taskid, task in tasks.items():
            result = {
                "id": taskid,
                "name": task.get_name(self.user_manager.session_language()),
                "context": task.get_context(self.user_manager.session_language()).original_content(),
                "problems": []
            }

            for problem in task.get_problems():

                macth = {"courseid": courseid, "taskid": taskid,'problemid':problem.get_id(),'username':username}
                user_tasks = self.database.user_tasks.find(macth)
                user_tasks = list(user_tasks) if not user_tasks is None  else []
                haveUser_tasks = len(user_tasks) > 0
                problem_dict = problem.get_original_content()
                
                pcontent = {}
                pcontent["id"] = problem.get_id()
                pcontent["deadline"] = problem_dict.get('deadline',None)
                pcontent["name"] = problem_dict.get('name','')
                pcontent["statement"] = problem_dict.get("statement","")
                pcontent['score'] = problem_dict.get('score')
                pcontent['score_late'] = problem_dict.get('score_late')
                pcontent['succeeded'] = user_tasks[0].get('succeeded') if haveUser_tasks else False
                pcontent['status'] = user_tasks[0].get('status_work') if haveUser_tasks else 'notting'


                result['problems'].append(pcontent)
            
            outputs["tasks"].append(result)

        return outputs, 200
            
    def API_POST(self ,courseid):
        course_input = flask.request.form

        taskid = 'lesson{0}{1}'.format( time.time(),self.user_manager.session_username() )
        taskid =  re.sub(r'[^A-Za-z0-9]+','',taskid)
        
        default_task = {
            'accessible':True,
            'author': self.user_manager.session_username(),
            'categories':[],
            'contact_url':'',
            'context':'',
            'environment_id':'default',
            'environment_parameters':{
                'limits':{'time':1,'hard_time':20,'memory':120},
                'run_cmd': ''
            },
            'environment_type':'docker',
            'evaluate':'best',
            'file': '',
            'groups': False,
            'input_random': '0',
            'network_grading' : False,
            'order' : '0',
            'problems':{},
            'stored_submissions': 0,
            'submission_limit':{
                'amount': -1,
                'period': -1
            },
            'weight': 1.0
        }

        course = self.course_factory.get_course(courseid)
        default_task.update(course_input)

        if self.user_manager.has_admin_rights_on_course(course):
            try:
                self.task_factory.create_task(course, taskid, default_task)
                return {"status":"success",'taskid':taskid}, 201
            except Exception as ex:
                return {"error":str(ex)}, 500

        return {"message":"you are not admin courses"}, 403


    def API_DELETE(self ,courseid, taskid):
        try :
            courses = self.course_factory.get_course(courseid)
            if self.user_manager.has_admin_rights_on_course(courses):
                self.database.submissions.remove({"courseid":courseid,"taskid":taskid})
                self.task_factory.delete_task(courseid, taskid)
                return {"status","success"}, 200
            else:
                return {"status" :"Forbidden"}, 403
        except Exception as ex :
            return {"error",str(ex)}, 500

    def API_PATCH(self ,courseid,taskid):
        courses_input = flask.request.form
        courses = self.course_factory.get_course(courseid)

        if self.user_manager.has_admin_rights_on_course(courses):
            content =  self.task_factory.get_task_descriptor_content(courseid,taskid)
            content.update(courses_input)
            self.task_factory.update_task_descriptor_content(courseid, taskid, content)
            return {"status" : "success"}, 200
        else:
            return {"status" :"Forbidden"}, 403