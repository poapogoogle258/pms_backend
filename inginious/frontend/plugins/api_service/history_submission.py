import json
import bson
import flask
from pymongo import DESCENDING

from inginious.frontend.pages.api._api_page import  APIAuthenticatedPage

class service_history_submission(APIAuthenticatedPage):

    def API_GET(self,coursesid,taskid,problemid):
        """get best answer of student
        
            {
                taskid:{
                    problemid:{
                        username:{
                            caches()
                        }
                    }
                }
            }
        
        """
        res = {}

        try :
            course = self.course_factory.get_course(coursesid)
        except:
            return {"status":"error", "message":"Course not found"},500
        try:
            if taskid is not None:
                tasks = {taskid: course.get_task(taskid)}
                if problemid is not None and not problemid in tasks[taskid].get_problems_dict():
                    return {'status':"error","message":"Problem not found"},500
        except:
            return {"status":"error","message":"Task not found"},500


        tasksid = [task_id for task_id in course.get_tasks()] if taskid is None else [taskid]
        

        if not self.user_manager.has_admin_rights_on_course(course):
            username = self.user_manager.session_username()
            member = [username]
        else:
            member = self.user_manager.get_course_registered_users(course,with_admins=False)


        for task_id in tasksid:
            tasks = course.get_task(task_id)
            problems = [ problem_id for problem_id in tasks.get_problems_dict()] if problemid is None else [problemid]
            res[task_id] = {
                'problems':{}
            }
            for problem_id in problems:
                res[task_id]['problems'][problem_id] = {}

                for username in member:
                        res[task_id]['problems'][problem_id][username] = []
                        all_submission = self.database.submissions.find({'courseid':coursesid,'taskid':task_id,'problemid':problem_id,'username': username}).sort([("submitted_on", DESCENDING)])
                        all_submission = list(all_submission)

                        for submission in all_submission:
                            input_user = bson.BSON.decode(self.submission_manager.get_gridfs().get(submission["input"]).read()) if len(submission) > 0 else None              
                            student_submisstion = {
                                "problemid" : problem_id,
                                "courseid": coursesid,
                                "taskid":task_id,
                                'username' : username,
                                'realname': self.user_manager.get_user_realname(username),
                                'submitted_on' : json.dumps(submission['submitted_on'], default=str),
                                'feedback' : submission.get("text", ""),
                                'status' : submission.get('status_work',None),
                                'code' : input_user.get('student_code',""),
                                'memory': submission.get('memory',None),
                                'timed': submission.get('runtime',None)
                            }
                            res[task_id]['problems'][problem_id][username].append(student_submisstion)
                        
        return res, 200