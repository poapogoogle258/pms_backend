import flask
import time
import re



from inginious.frontend.pages.api._api_page import APIAuthenticatedPage


class service_courses(APIAuthenticatedPage):

    #get course opening public
    def API_GET(self, courses_id=None):
        
        output = []
        username = self.user_manager.session_username()
        user_info = self.user_manager.get_user_info(username)
        language = self.user_manager.session_language()

        if courses_id == None:
            courses = self.course_factory.get_all_courses()
        else:
            try:
                courses = {courses_id: self.course_factory.get_course(courses_id)}
            except Exception as ex:
                return {"status":"error", "message ": "Course not found"}, 500
        
    
        for courseid, course in courses.items():
            if course.is_open_to_non_staff():
                if self.user_manager.user_is_superadmin() or self.user_manager.course_is_user_registered(course,username):
                    course_show = {}
                    course_show['id'] = courseid
                    course_show['name'] = course.get_name(language)
                    course_show['description'] = course.get_description(language)
                    course_show['is_admin'] = self.user_manager.has_admin_rights_on_course(course)

                    if self.user_manager.has_admin_rights_on_course(course):
                        course_show['password'] = course.get_registration_password()

                    output.append(course_show)
        
        return flask.jsonify(output) ,200


    def API_POST(self):
        """ create new coursec hahaha"""
        courses_input = flask.request.form

        courseid = 'course{0}{1}'.format( time.time() ,self.user_manager.session_username() )
        courseid =  re.sub(r'[^A-Za-z0-9]+','',courseid)

        create_course =  {
            "name": courses_input.get('name',courseid),
            "admins": [self.user_manager.session_username()],
            "accessible": True,
            "registration_password":courses_input.get('password'),
            'description' : courses_input.get('description',""),
        }
        try:
            self.course_factory.create_course(courseid, create_course)
            return {"status": "success","courseid":courseid}, 201
        except Exception as ex:
              return {"status": "error",'message':f"server don't can create your course. Error : {str(ex)} "}, 500
      

    def API_PATCH(self, courseid):
        courses_update = flask.request.form
        course = self.course_factory.get_course(courseid)

        if self.user_manager.has_admin_rights_on_course(course):
            content = self.course_factory.get_course_descriptor_content(courseid)

            content.update(courses_update)
            self.course_factory.update_course_descriptor_content(courseid, content)
            return {"status" : "success","courseid":courseid}, 200
        else:
            return {"status" :"Forbidden"}, 403


    def API_DELETE(self, courseid):

        try:
            course = self.course_factory.get_course(courseid)
        except:
            return {'status':'error', "message ":"Course not found"}, 500

        try:
            if self.user_manager.has_admin_rights_on_course(course):
                self.course_factory.delete_course(courseid)
                return {"status": "success"}, 200
            else:
                return {"status" :"Forbidden"}, 403
        except Exception as ex:
            return {'status':'error', 'message': "server don't can delete this course"}, 500

