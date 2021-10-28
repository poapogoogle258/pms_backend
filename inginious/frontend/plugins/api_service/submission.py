import json
import bson
import flask

from inginious.frontend.pages.api._api_page import  APIAuthenticatedPage

class service_submission(APIAuthenticatedPage):

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
            member = self.user_manager.get_course_registered_users(course)


        for task_id in tasksid:
            tasks = course.get_task(task_id)
            problems = [ problem_id for problem_id in tasks.get_problems_dict()] if problemid is None else [problemid]
            res[task_id] = {
                'problems':{}
            }
            for problem_id in problems:
                res[task_id]['problems'][problem_id] = {}
                data = list(self.database.user_tasks.find({"courseid": coursesid, "taskid": task_id,'problemid':problem_id,'username':{'$in':member}}))
                caches = {username: None for username in member}
                for result in data:
                    username = result["username"]
                    caches[username] = result

                for username,cache in caches.items():
                    if cache != None:
                        if cache['submissionid']!= None:
                            submission = self.database.submissions.find({'_id':cache['submissionid']})
                            submission = list(submission) if not submission is None else []
                            input_user = bson.BSON.decode(self.submission_manager.get_gridfs().get(submission[0]["input"]).read()) if len(submission) > 0 else None
                        else:
                            submission = None
                            input_user = None
                                            
                        student_submisstion = {
                            "problemid" : problem_id,
                            "courseid": coursesid,
                            "taskid":task_id,
                            'username' : username,
                            "grade": cache.get('grade',0),
                            'succeeded' : cache.get('succeeded',None),
                            'attempts' : cache.get('tried',0),
                            'realname': self.user_manager.get_user_realname(username),
                            'submitted_on' : json.dumps(submission[0]['submitted_on'], default=str) if submission is not None else None,
                            'feedback' : submission[0].get("text", "") if submission is not None else "",
                            'status' : cache.get('status_work',None),
                            'extrapoint':cache.get('extrapoint',0),
                            'code' : input_user.get('student_code',"") if submission is not None else None,
                            'memory': submission[0].get('memory',None) if submission is not None else None,
                            'timed': submission[0].get('runtime',None) if submission is not None else None,
                        }

                        res[task_id]['problems'][problem_id][username] = student_submisstion
                        
        return res, 200

    def API_POST(self, courseid, taskid, problemid):  # pylint: disable=arguments-differ
        """
            Creates a new submissions. Takes as (POST) input the key of the subproblems, with the value assigned each time.

            Returns

            - an error 400 Bad Request if all the input is not (correctly) given,
            - an error 403 Forbidden if you are not allowed to create a new submission for this task
            - an error 404 Not found if the course/task id not found
            - an error 500 Internal server error if the grader is not available,
            - 200 Ok, with {"submissionid": "the submission id"} as output.
        """
        username = self.user_manager.session_username()
        user_input =  flask.request.get_json(force=True)
        user_input['problemid'] = problemid

        try:
            course = self.course_factory.get_course(courseid)
        except:
            return {"message":"Course not found"} ,500


        if not self.user_manager.course_is_open_to_user(course, username, False):
            return {"message":" You are not registered to this course"} ,403

        try:
            task = course.get_task(taskid)
        except:
            return {"message":"Task not found"} ,500

        # Verify rights
        if not self.user_manager.task_can_user_submit(task, username, False):
            return {"message":"You are not allowed to submit for this task"} ,403


        #PMS15-10
        problems = task.get_problems_dict()
        if not problemid in problems:
            return {"message":"problem not found"},500

        # self.user_manager.user_saw_task(username, courseid, taskid)
        self.user_manager.user_saw_problem(username, courseid, taskid, problemid)

        
        # PMS17-10 set value for check resluts
        user_input['fixanswer'] = problems[problemid]['fixAnswer']
        user_input['testcase'] = problems[problemid]['testcase']
        user_input['deadline'] = problems[problemid].get('deadline',None)
        user_input['score'] = problems[problemid]['score']
        user_input['score_late'] = problems[problemid]['score_late']

        # Start the submission
        submissionid, _ = self.submission_manager.add_job(task, user_input, debug = False)
        return {"submissionid": str(submissionid)},200

