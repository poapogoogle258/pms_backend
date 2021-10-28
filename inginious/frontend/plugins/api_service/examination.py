
import flask

from difflib import get_close_matches

from inginious.frontend.pages.api._api_page import APIAuthenticatedPage

class service_examination(APIAuthenticatedPage):

    def API_GET(self):

        course_all = self.course_factory.get_all_courses()
        language = self.user_manager.session_language()
        res = {}
 
        for courseid, course in course_all.items():
            if self.user_manager.has_admin_rights_on_course(course):
                res[courseid] = { 'courseid':courseid ,'name':course.get_name(language),'tasks':{}}
                for taskid,task in course.get_tasks().items():
                    res[courseid]['tasks'][taskid]={'name':task.get_name(language),'problems':[]}
                    for problmeid ,problme in task.get_problems_dict().items():
                        res[courseid]['tasks'][taskid]['problems'].append({'name':problme.get('name',""),'id':problmeid})


        return res,200
        

