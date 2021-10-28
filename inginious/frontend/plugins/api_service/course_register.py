from inginious.frontend.pages.api._api_page import  APIAuthenticatedPage

class service_courses_register(APIAuthenticatedPage):

    def API_GET(self,courseid):
        try:
            course = self.course_factory.get_course(courseid)
        except Exception as ex:
            return {"status":"error", "message ": "Course not found"}, 500

        username = self.user_manager.session_username()
        user_info = self.user_manager.get_user_info(username)
        language = self.user_manager.session_language()
        output = {}

        if course.is_registration_possible(user_info):  
            output['id'] = courseid
            output['name'] = course.get_name(language)
            output['description'] = course.get_description(language)
            output['registed'] = self.user_manager.course_is_user_registered(course,username)
            output['teacher'] =  None if len(course.get_admins()) == 0 else self.user_manager.get_user_realname(course.get_admins()[0])
            output['tasks'] = [task.get_name(language) for taskid, task in course.get_tasks().items()]
            
        return output ,200

    def API_POST(self,courseid,password=None):
        try:
            course = self.course_factory.get_course(courseid)
        except Exception as ex:
            return {'status':'error','message':f"course not found Error : {str(ex)}"}

        username = self.user_manager.session_username()
        
        if self.user_manager.course_register_user(course,username,password,False):
            return {"status":"success"}, 200
        else:
            return {"status":"failed"}, 200



        
