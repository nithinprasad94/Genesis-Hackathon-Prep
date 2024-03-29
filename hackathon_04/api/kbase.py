from HTTPRequest import HTTPRequest
from suffix_keys import url_suff as suff
import suffix_keys
import json


# 3) KNOWLEDGE BASES
# 3.1 Create a knowledge base
# 3.2 view a knowledge base
# 3.3 view a list of knowledge bases
# 3.4 update a knowledge base
# 3.5 delete a knowledge base

# POST Request
def create_kbase(server_name, url_suff, payload_info, org_id, token,kbase_responses={}):

    # Check if # of databases exceeds limit (5)
    if len(kbase_responses.items()) == 5:
        return {},

    full_addr = server_name + url_suff["create_kbase"]

    req = HTTPRequest(full_addr, "POST")

    for key in payload_info.keys():
        req.payload_append(key, payload_info[key])

    #'Content-Type': "application/json",
    #'organizationid': "3ae6bd8b-23b6-47c7-a9a0-8dc56833ca18",
    #'token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcmdJZCI6IjNhZTZiZDhiLTIzYjYtNDdjNy1hOWEwLThkYzU2ODMzY2ExOCIsImV4cCI6MTU3MTUxNjYyOCwiaWF0IjoxNTcxNTEzMDI4fQ.S1mQ4sdeSaPhTCwUodVOb6QW3yOzTnQKOunSU732SSI",
    #'cache-control': "no-cache",
    req.add_header("Content-Type","application/json")
    req.add_header("organizationid",org_id)
    req.add_header("token", token)
    req.add_header("cache-control","no-cache")

    response = req.post()
    print(response)
    print("response: ",response.json())

    # resp_id = response.json().get("id")
    # kbase_responses['status_code'] = response.status_code
    # if resp_id:
    #     kbase_responses[resp_id] = (response["dateCreated"],
    #                                 response["dateModified"],
    #                                 response["selfUri"])
    # else:
    #     return kbase_responses
    #
    # return kbase_responses


# GET Request
def view_kbase(server_name, url_suff, org_id, token, limit=1, kbase_id=None):

    full_addr = server_name + url_suff["view_kbase"]
    response_list = []
    print('kbase_id in view_kbase', kbase_id)
    if kbase_id:
        full_addr += '/' + kbase_id
        req = HTTPRequest(full_addr, "GET")
        req.add_header("Content-Type", "application/json")
        req.add_header("organizationid", org_id)
        req.add_header("token", token)
        req.add_header("cache-control", "no-cache")
        response = req.get()
        response_dict = response.json()
        if response_dict.status_code == 200:
            response_list.append(response_dict)
    else:
        full_addr += '?limit={0}'.format(limit)
        req = HTTPRequest(full_addr, "GET")
        req.add_header("Content-Type", "application/json")
        req.add_header("organizationid", org_id)
        req.add_header("token", token)
        req.add_header("cache-control", "no-cache")
        response = req.get()
        print("Response:", response)
        response_dict = response.json()
        if response.status_code == 200:

            response_list = response_dict["entities"]
            print("Resp List", response_list)

            # while response_dict.get("nextUri") != None:
            #     print("in loop")
            #     full_addr = server_name + url_suff["view_kbase"]
            #     full_addr += '?limit={0}'.format(limit)
            #     full_addr += response_dict.get("nextUri")
            #     req = HTTPRequest(full_addr, "GET")
            #     response = req.get()
            #     response_dict = response.json()
            #     if response.status_code == 200:
            #         response_list.append(response_dict)
            ret_list = []
            for elem in response_list:
                ret_list.append(elem['id'])
            return ret_list

    return response_list


# PUT Request
def update_kbase(server_name, url_suff, payload_info, kbase_id):
    full_addr = server_name + url_suff["update_kbase"]
    full_addr += kbase_id
    req = HTTPRequest(full_addr, "PUT")
    for key in payload_info.keys():
        req.payload_append(key, payload_info[key])
    response = req.put()
    response_result = response.json()
    response_result['status_code'] = response.status_code
    return response_result

def garbles():
    print("YOU GARBAGE BOIIII")

# DELETE Request
def delete_kbase(org_id, token, server_name, url_suff, kbase_id):
    print("IN DELETE!!!!")
    full_addr = server_name + url_suff["delete_kbase"]
    full_addr += kbase_id
    req = HTTPRequest(full_addr, "DELETE")
    req.add_header("Content-Type", "application/json")
    req.add_header("organizationid", org_id)
    req.add_header("token", token)
    req.add_header("cache-control", "no-cache")
    response = req.delete()
    print("Response: ",response,", Response Code:", response.status_code)
    return response.status_code

