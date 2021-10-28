
import flask

from fuzzywuzzy import fuzz

from inginious.frontend.pages.api._api_page import APIAuthenticatedPage

class service_search(APIAuthenticatedPage):

    def API_GET(self,search_methon,query=''):
        results = []
        course_all = self.course_factory.get_all_courses()
        language = self.user_manager.session_language()
        cutoff = 70

 
        for courseid, course in course_all.items():
            if course.is_open_to_non_staff():
                if  search_methon=='allcourse' or self.user_manager.course_is_user_registered(course) or self.user_manager.has_admin_rights_on_course(course):
                    course_name = str(course.get_name(language))

                    results.append({
                        'id' : course.get_id(),
                        'title' : course_name,
                        'teacher' : None if len(course.get_admins()) == 0 else self.user_manager.get_user_realname(course.get_admins()[0]),
                        'score_partial_ratio': fuzz.partial_ratio(course_name, query),
                        'score_ratio' : fuzz.ratio(course_name, query)
                        
                    })
        
        results = list(filter(lambda course : course['score_partial_ratio'] >= cutoff ,results))

        res =  sorted(results, key=lambda course_item : (course_item['score_partial_ratio'] ,course_item['score_ratio'] ),reverse=True )

        return flask.jsonify(res) ,200
        

