import flask
from inginious.frontend.pages.api._api_page import  APIAuthenticatedPage

class service_courses_member(APIAuthenticatedPage):
    def API_GET(self,courseid):
        try:
            course = self.course_factory.get_course(courseid)
        except:
            return {"status":"error", "message":"Course not found"}

        res = {}
        for member in self.user_manager.get_course_registered_users(course):
            res[member] = {
                'realname':self.user_manager.get_user_realname(member),
                'email':self.user_manager.get_user_email(member),
            }

        return res, 200
        

    def API_POST(self,courseid):
        try:
            course = self.course_factory.get_course(courseid)
        except:
            return {"status":"error", "message":"Course not found"},500

        if self.user_manager.has_admin_rights_on_course(course):
            user_input = flask.request.get_json(force=True)
            email = user_input['email']
            find_user = self.database.users.find_one({'email':email})
            if find_user is not None:
                username = find_user['username']
                self.user_manager.course_register_user(course,username,force=True)
                return {"status":"success","username":username,"realname":self.user_manager.get_user_realname(username)},200
            return {"status":"error","message":"This Email not found"},200
        else:
            return {'status':'Forbidden'},403
        

    def API_DELETE(self,courseid,username):
        try:
            course = self.course_factory.get_course(courseid)
        except:
            return {"status":"error", "message":"Course not found"}

        if self.user_manager.has_admin_rights_on_course(course):
            self.user_manager.course_unregister_user(course,username)
        else:
            username = self.user_manager.session_username()
            self.user_manager.course_unregister_user(course,username)
        
        return {"status":"success"},200

            

        
 