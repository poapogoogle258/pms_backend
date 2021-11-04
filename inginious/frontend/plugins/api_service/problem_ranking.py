import flask
import json
import pymongo

from inginious.frontend.pages.api._api_page import  APIAuthenticatedPage

class service_ranking(APIAuthenticatedPage):

    def API_GET(self,coursesid,taskid,problemid):
        try :
            course = self.course_factory.get_course(coursesid)
        except:
            return {"status":"error", "message":"Course not found"},500
        try:
            tasks = {taskid: course.get_task(taskid)}
        except:
            return {"status":"error","message":"Task not found"},500
                

        member = self.user_manager.get_course_registered_users(course,with_admins=False)
        
        data = list(self.database.user_tasks.find({"courseid": coursesid, "taskid": taskid,'problemid':problemid,'username':{'$in':member}}))

        submisstions = [cache['submissionid'] for cache in data]
        raw_submission =  self.database.submissions.find({'_id':{'$in': submisstions}})
        sorted_submission = list(raw_submission.sort([("grade",pymongo.DESCENDING),("runtime", pymongo.ASCENDING),("memory", pymongo.ASCENDING),("submitted_on", pymongo.DESCENDING)]))

        res = []
        for index in range(len(sorted_submission)):
            res.append({
                'number' : index+1,
                'realname' : self.user_manager.get_user_realname(sorted_submission[index]['username'][0]),
                'runtime' : sorted_submission[index]['runtime'],
                'memory' : sorted_submission[index]['memory'],
                'submitted_on' : json.dumps(sorted_submission[index]['submitted_on'], default=str)
            })   

        return flask.jsonify(res), 200


