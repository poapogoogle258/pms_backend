import flask
import yaml
import time
import bson
import pymongo 
import re
 

import datetime

from inginious.common.base import id_checker
from inginious.frontend.pages.api._api_page import APIAuthenticatedPage


class service_problem(APIAuthenticatedPage):

    def API_GET(self, courseid, taskid, problemid=None) :
        try:
            username = self.user_manager.session_username()
            course = self.course_factory.get_course(courseid)
            task = self.task_factory.get_task(course, taskid)
            problems = task.get_problems_dict()

            output = {
                "courseid":courseid,
                "course_name":course.get_name(self.user_manager.session_language()),
                "taskid" : taskid,
                "task_name" : task.get_name(self.user_manager.session_language()),
                "problems" : [],
                'is_admin' : self.user_manager.has_admin_rights_on_course(course,username),
            }

            for problmeid1,problem in problems.items():
                last_submisstion = self.database.submissions.find({"username": username, "courseid": courseid, "taskid": taskid,"problemid":problmeid1}).sort([("submitted_on", pymongo.DESCENDING)]).limit(1)

                last_submisstion = list(last_submisstion) if not last_submisstion is None else []
                

                input_user = bson.BSON.decode(self.submission_manager.get_gridfs().get(last_submisstion[0]["input"]).read()) if len(last_submisstion) > 0 else None


                caches = self.user_manager.get_problem_caches([username],courseid,taskid,problmeid1)
                print(caches)
                
                if problemid == None or problmeid1 == problemid:
                    output['problems'].append({
                        'id':problmeid1,
                        'name':problem['name'],
                        'header':problem['header'],
                        'testcase':problem.get('testcase',None ) ,
                        'examplecase':problem.get('examplecase',None ) ,
                        'deadline':problem.get('deadline',None),
                        'tried' : caches[username]['tried'] if caches[username]!=None else 0,
                        'status' : caches[username]['status_work'] if caches[username]!=None and caches[username]['tried'] > 0 else 'notting',
                        'submitted_on' : last_submisstion[0]['submitted_on'] if len(last_submisstion) > 0 else None,
                        'code': input_user.get('student_code',"") if len(last_submisstion) > 0 else "",
                        'score': problem.get('score',''),
                        'accept':problem.get('accept',[]),
                        'notaccept':problem.get('notaccept',[]),
                        'score_late': problem.get('score_late',''),
                        'statement': problem.get('statement',''),
                        'fixanswer': problem.get('fixanswer',True),
                        'noinput': problem.get('noinput',''),
                    })

            return output, 200
        except Exception as ex:
            return {'status':'error' ,"message":f"Problem not found Error: {str(ex)}"}, 500


    def API_POST(self, courseid, taskid):
        problem_input = flask.request.get_json(force=True)

        problemid =  'problem{0}{1}'.format( time.time(),self.user_manager.session_username() )
        problemid = re.sub(r'[^A-Za-z0-9]+','',problemid)

        default_problem = {
            'type': 'code',
            'language': 'python',
            'default': '',
            'fixAnswer' : False,
            'testcase':{
                'input':[],
                'output':[]
            },
            'examplecase':{
                'input':[],
                'output':[]
            }
        }
        default_problem.update(problem_input)

        try:
            course = self.course_factory.get_course(courseid)
        except:
            return {'status':'error', "message":"Course not found"}, 500


        if self.user_manager.has_admin_rights_on_course(course):
            try:    
                task = self.task_factory.get_task(course, taskid)
            except:
                return {'status':'error',"mssage" : "Task not found"}, 500

            task_path = task.get_fs().get('task.yaml').decode('utf-8')
            task_file =yaml.safe_load(task_path)
            
            if problemid in task_file['problems']:
                return {'status':"error","message":"coursesid same in this courses"},400

            try:
                task_file['problems'][problemid] = default_problem
                task.get_fs().put('task.yaml',yaml.dump(task_file))
                return {"status":"success","problemid":problemid}, 201
            except:
                return {"status":"error", "message":"server dont can save problem"}, 500
        
        return {"status" :"Forbidden"}, 403
        
        
    def API_PATCH(self, courseid, taskid ,problemid):
        problem_input = flask.request.get_json(force=True)

        try:
            course = self.course_factory.get_course(courseid)
        except:
            return {'status':'error', "message":"Course not found"}, 500

        try:    
            task = self.task_factory.get_task(course, taskid)
        except:
            return {'status':'error',"mssage" : "Task not found"}, 500
        
        if self.user_manager.has_admin_rights_on_course(course):

            task_file = task.get_fs().get('task.yaml').decode('utf-8')
            task_dict = yaml.safe_load(task_file)
            task_dict["problems"][problemid].update(problem_input)
            try:
                task.get_fs().put('task.yaml',yaml.dump(task_dict))

                chachs = self.database.user_tasks.find({
                    'courseid':courseid,
                    'taskid':taskid,
                    'problemid':problemid,
                    'status_work': {'$in':['success','late']}})
                
                
                for chach in list(chachs):
                    print(chach)
                    islate = chach['submitted_on'] >= datetime.datetime.strptime(problem_input['deadline'], '%Y-%m-%dT%H:%M:%S.%fZ') if problem_input['deadline'] != None else False

                    self.database.user_tasks.update_one({ 
                        '_id': chach['_id']
                    },{
                        '$set': {
                            'grade' : problem_input['score_late'] if islate else problem_input['score'],
                            'status_work': 'late' if islate else 'success'
                        } 
                       
                    })


                return {"status":"success"}, 200
            except Exception as ex:
                return {"status":"error", "message":"server dont can update problem"+str(ex) }, 500

        else:
            return {"status" :"Forbidden"}, 403

    def API_DELETE(self, courseid, taskid, problemid ):
        try:
            course = self.course_factory.get_course(courseid)
            task = self.task_factory.get_task(course, taskid)
            if self.user_manager.has_admin_rights_on_course(course):

                task_file = task.get_fs().get("task.yaml").decode("utf-8")
                task_dict = yaml.safe_load(task_file)

                del task_dict['problems'][problemid]
                task.get_fs().put('task.yaml',yaml.dump(task_dict))
                self.database.submissions.remove({"courseid":courseid,"taskid":taskid,"problemid":problemid})
                return {"status": "success"},200
            else:
                return {"status" :"Forbidden"}, 403
        except Exception as ex :
            return {"error": str(ex)}, 500