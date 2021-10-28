import hashlib
import random
import re
import flask
from  flask import jsonify

from inginious.frontend.pages.api._api_page import  APIPage
"""
     Query Endpoint /api/v0/service_user?$Query
"""


class service_user(APIPage):
    def API_GET(self, username=None):
        """
            Query Endpoint /api/v0/service_user/{username}
        """
        try:
            data_query = []
            if username == None:
                users = self.database.users.find({"username" : {'$ne': 'superadmin'}})
            else:
                users = self.database.users.find({"username": username})
            for user in users:
                data_query.append({
                "username": user["username"],
                "realname": user["realname"],
                "email": user["email"]
                })
            return jsonify(data_query), 200
        except Exception as e:
            return {"status": f"failed : {e}"}, 500

    def API_POST(self): 
        """
            register
        """
        msg1 = ""
        msg2 = ""
        data = flask.request.form
        error = False
        # email_re = re.compile(
        #     r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
        #     r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'  # quoted-string
        #     r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain

        # Check input format
        # if re.match(r"^[-_|~0-9A-Z]{4,}$", data["username"], re.IGNORECASE) is None:
        #     error = True
        #     msg = "Invalid username format."
        # elif email_re.match(data["email"]) is None:
        #     error = True
        #     msg = "Invalid email format."
        # elif len(data["passwd"]) < 6:
        #     error = True
        #     msg = "Password too short."
        # elif data["passwd"] != data["passwd2"]:
        #     error = True
        #     msg = "Passwords don't match !"

        if not error:
            existing_user = self.database.users.find_one(
                {"$or": [{"username": data["username"]}, {"email": data["email"]}]})
            if existing_user is not None:
                error = True
                if existing_user["username"] == data["username"]:
                    msg1 = "ชื่อผู้ใช้งานซ้ำ กรุณาเปลี่ยนชื่อผู้ใช้งานใหม่"
                elif existing_user["email"] == data["email"]:
                    msg2 = "อีเมลซ้ำ กรุณาเปลี่ยนอีเมลใหม่"
            else:
                passwd_hash = hashlib.sha512(data["passwd"].encode("utf-8")).hexdigest()
                activate_hash = hashlib.sha512(str(random.getrandbits(256)).encode("utf-8")).hexdigest()
                self.database.users.insert({"username": data["username"],
                                            "realname": data["realname"],
                                            "email": data["email"],
                                            "password": passwd_hash,
                                            "bindings": {},
                                            "language": self.user_manager._session.get("language", "en"),
                                            "tos_accepted": True
                                            })#"activate": activate_hash,
                # try:
                #     message = Message(recipients=[(data["realname"], data["email"])],
                #                       subject=subject,
                #                       body=body,)
                #     mail.send(message)
                #     msg = "You are succesfully registered. An email has been sent to you for activation."
                # except Exception as ex:
                #     # Remove newly inserted user (do not add after to prevent email sending in case of failure)
                #     # self.database.users.remove({"username": data["username"]})
                #     error = True
                #     msg = "Something went wrong while sending you activation email. Please contact the administrator."
        return {"message1" : msg1,"message2" : msg2,'status': 'error' if error else 'success'}, 200
        #edit PMS 15.8.64 redirect


    def API_DELETE(self,username):
        try:
            self.database.users.remove({"username": username})
            return {"status" : "sucess"}, 200
        except Exception as e:
            return {"status" : f"failed : {e}"}, 500


    def API_PATCH(self,username):
        users_data = flask.request.form
        try:
            self.database.users.update_one({"username":username},
                {"$set" :users_data}
            )
            return {"status" : "success"},200
        except Exception as ex:
            return {"status": "error" , 'message':str(ex)},500 









        
                    

    