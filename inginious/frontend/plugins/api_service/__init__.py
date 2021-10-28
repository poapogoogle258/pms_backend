# -*- coding: utf-8 -*-
#
# This file is part of INGInious. See the LICENSE and the COPYRIGHTS files for
# more information about the licensing of this file.
# support Inginious version 0.7 use flask in back_end
""" users service api plugin """


from flask_cors import CORS

from inginious.frontend.plugins.api_service.users import service_user
from inginious.frontend.plugins.api_service.courses import service_courses
from inginious.frontend.plugins.api_service.submission import service_submission
from inginious.frontend.plugins.api_service.problems import service_problem
from inginious.frontend.plugins.api_service.task import tasks_service
from inginious.frontend.plugins.api_service.course_member import service_courses_member
from inginious.frontend.plugins.api_service.search_course import service_search
from inginious.frontend.plugins.api_service.course_register import service_courses_register
from inginious.frontend.plugins.api_service.problem_ranking import service_ranking
from inginious.frontend.plugins.api_service.examination import service_examination
from inginious.frontend.plugins.api_service.history_submission import service_history_submission
from inginious.frontend.plugins.api_service.user_tasks_extrapoint import service_extrapoint


def init(plugin_manager, course_factory, client, conf):
    """ Init the plugin """
    print("open new service")
    cors_config = {
        "origins": "http://localhost:3000",
        "supports_credentials": True,
    }
    GET, POST, DELETE, PATCH = "GET","POST","DELETE","PATCH"
    app = plugin_manager._flask_app
    cors = CORS(app,resources={r"/api/*":cors_config})

    # ------------------- search =>  /api/plugin/search/{search_methon}/<query>

    @app.route('/api/plugin/search/<search_methon>/<query>',methods = [GET])
    def search_course(search_methon,query):
        return service_search().API_GET(search_methon,query)

    # ------------------- course =>  /api/plugin/course/<courseid>

    @app.route('/api/plugin/course',defaults= {'courseid': None},methods = [GET])
    @app.route('/api/plugin/course/<courseid>',methods = [GET])
    def get_course(courseid):
        return service_courses().API_GET(courseid)
       
    @app.route('/api/plugin/course',methods = [POST])
    def create_course():
        return service_courses().API_POST()
    
    @app.route('/api/plugin/course/<courseid>',methods = [PATCH])
    def edit_course(courseid):
        return service_courses().API_PATCH(courseid)

    @app.route('/api/plugin/course/<courseid>',methods = [DELETE])
    def delete_course(courseid):
        return service_courses().API_DELETE(courseid)
    
    #---------------------- tasks /api/plugin/<couresid>/<taskid>

    @app.route('/api/plugin/task/<courseid>',defaults ={'taskid': None} ,methods = [GET])
    @app.route('/api/plugin/task/<courseid>/<taskid>', methods = [GET])
    def get_task(courseid, taskid):
        return tasks_service().API_GET(courseid, taskid)
    
    @app.route('/api/plugin/task/<courseid>', methods = [POST])
    def create_task(courseid):
        return tasks_service().API_POST(courseid)
    
    @app.route('/api/plugin/task/<courseid>/<taskid>', methods = [DELETE])
    def delete_task(courseid, taskid):
        return tasks_service().API_DELETE(courseid, taskid)
    
    @app.route('/api/plugin/task/<courseid>/<taskid>', methods = [PATCH])
    def edit_task(courseid, taskid):
        return tasks_service().API_PATCH(courseid, taskid)


    #---------------------- problem /api/plugin/<courseid>/<taskid>/<problemid>
    @app.route('/api/plugin/problem/<courseid>/<taskid>' , defaults={'problemid':None},methods = [GET])
    @app.route('/api/plugin/problem/<courseid>/<taskid>/<problemid>' ,methods = [GET])
    def get_problem(courseid, taskid, problemid):
        return service_problem().API_GET(courseid, taskid, problemid)
    
    @app.route('/api/plugin/problem/<courseid>/<taskid>' ,methods = [POST])
    def create_problem(courseid, taskid):
        return service_problem().API_POST(courseid, taskid)
    
    @app.route('/api/plugin/problem/<courseid>/<taskid>/<problemid>' ,methods = [DELETE])
    def delete_problem(courseid, taskid, problemid):
        return service_problem().API_DELETE(courseid, taskid, problemid)
    
    @app.route('/api/plugin/problem/<courseid>/<taskid>/<problemid>' ,methods = [PATCH])
    def edit_problem(courseid, taskid, problemid):
        return service_problem().API_PATCH(courseid, taskid, problemid)

    # ------------------- course member =>  /api/plugin/coursemember/<courseid>
    
    @app.route('/api/plugin/coursemember',defaults= {'courseid': None},methods = [GET])
    @app.route('/api/plugin/coursemember/<courseid>',methods = [GET])
    def get_course_member(courseid):
        return service_courses_member().API_GET(courseid)
       
    @app.route('/api/plugin/coursemember/<courseid>',methods = [POST])
    def add_course_member(courseid):
        return service_courses_member().API_POST(courseid)

    @app.route('/api/plugin/coursemember/<courseid>',defaults= {'username' : None} ,methods = [DELETE])
    @app.route('/api/plugin/coursemember/<courseid>/<username>',methods = [DELETE])
    def delelt_course_member(courseid,username):
        return service_courses_member().API_DELETE(courseid,username)

    #------------------- register coures => /api/plugin/registercourse/<courseid>/<password>
    @app.route('/api/plugin/registercourse/<courseid>',methods=[GET])
    def get_register_course(courseid):
        return service_courses_register().API_GET(courseid)

    @app.route('/api/plugin/registercourse/<courseid>/<password>',methods=[POST])
    def register_course(courseid,password):
        return service_courses_register().API_POST(courseid,password)

    # ------------------ submissions =>  /api/plugin/subminssion/<courseid>/<taskid>

    @app.route('/api/plugin/submission/<courseid>',defaults={'problemid' :None,'taskid':None} ,methods  = [GET])
    @app.route('/api/plugin/submission/<courseid>/<taskid>',defaults={'problemid' :None} ,methods  = [GET])
    @app.route('/api/plugin/submission/<courseid>/<taskid>/<problemid>',methods  = [GET])
    def get_submission_in_task(courseid,taskid,problemid):
        return service_submission().API_GET(courseid,taskid,problemid)
    
    @app.route('/api/plugin/submission/<courseid>/<taskid>/<problemid>',methods  = [POST])
    def send_submission_in_task(courseid,taskid,problemid):
        return service_submission().API_POST(courseid,taskid,problemid)


    #-------------------- service_history_submission => /api/plugin/history_submission/<courseid>/<taskid>/<problemid>
    @app.route('/api/plugin/history_submission/<courseid>',defaults={'problemid' :None,'taskid':None} ,methods  = [GET])
    @app.route('/api/plugin/history_submission/<courseid>/<taskid>',defaults={'problemid' :None} ,methods  = [GET])
    @app.route('/api/plugin/history_submission/<courseid>/<taskid>/<problemid>',methods  = [GET])
    def get_history_submission(courseid,taskid,problemid):
        return service_history_submission().API_GET(courseid,taskid,problemid)

    #------------------- service_extrapoint => 

    @app.route('/api/plugin/extrapoint/<courseid>/<taskid>',methods = [POST])
    def add_extrapoint(courseid,taskid):
        return service_extrapoint().API_POST(courseid,taskid)

    #------------------- service_ranking => /api/plugin/ranking/<courseid>/<taskid>
    @app.route('/api/plugin/ranking/<courseid>/<taskid>/<problemid>',methods  = [GET])
    def get_ranking_problem(courseid,taskid,problemid):
        return service_ranking().API_GET(courseid,taskid,problemid)

    
    
    #--------------------- examinations /api/plugin/examinations
    @app.route('/api/plugin/examinations',methods  = [GET])
    def get_examinations():
        return service_examination().API_GET()

    #--------------------- user /api/plugin/user/<usernamd>

    @app.route('/api/plugin/user',defaults ={'username': None}, methods = [GET])                                                                                                                                                                                                                                                                                                                                                                                            
    @app.route('/api/plugin/user/<username>', methods = [GET])
    def get_user(username):
        return service_user().API_GET(username)
        
    @app.route('/api/plugin/user', methods = [POST])
    def register_new_user():
        return service_user().API_POST()

    @app.route('/api/plugin/user/<username>', methods = [PATCH])
    def edit_data_user(username):
        return service_user().API_PATCH(username)

    #----------> logout 

    @app.route('/api/plugin/authentication',methods = [DELETE])
    def user_logout():
        try:
            plugin_manager._user_manager.disconnect_user()
            return {"status" : "success"}, 200
        except:
            pass
        return {"status": "error"}, 500



    
    



