import flask


from inginious.frontend.pages.api._api_page import  APIAuthenticatedPage

class service_extrapoint(APIAuthenticatedPage):

    def API_POST(self,courseid,taskid):
        """ 
            [
                problemid : {
                    username :
                    extrapoint :
            
            ]
        """

        try :
            course = self.course_factory.get_course(courseid)
        except:
            return {"status":"error", "message":"Course not found"},500
        try:
            tasks = {taskid: course.get_task(taskid)}
        except:
            return {"status":"error","message":"Task not found"},500

        user_input = flask.request.get_json(force=True)

        if self.user_manager.has_admin_rights_on_course(course):
            for problemid, data in user_input.items():
                for username , extrapoint in data.items():
                    query = {"courseid": courseid, "taskid": taskid,'problemid': problemid,'username': username }


                    if len(list(self.database.user_tasks.find(query))) == 0:
                        self.user_manager.user_saw_problem(username,courseid,taskid,problemid)

                    self.database.user_tasks.find_one_and_update(query,{   
                        "$set" : {
                            "extrapoint": int(extrapoint) if extrapoint is not None else 0
                        }
                    })

                    
            return {'status':'done'}, 200

        else:
            return {'status':'err'}, 403

            
                        