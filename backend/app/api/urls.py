API = "/api/"

CREATE = "/create/"
LIST = "/list/"
EDIT = "/edit/"
DELETE = "/delete/"


class UserURLS:
    user = "user"
    base_url = f"{API}{user}"
    # POST
    register = "/register/"
    register_url = f"{base_url}{register}"
    # POST
    login = "/login/"
    login_url = f"{base_url}{login}"
    # GET
    user_data = "/user_data/"
    user_data_url = f"{base_url}{user_data}"


class DeskURLS:
    desk = "desk"
    base_url = f"{API}{desk}"

    # POST
    create = CREATE
    create_url = f"{base_url}{create}"
    # GET
    list = LIST
    list_url = f"{base_url}{list}"
    # PATCH
    edit = EDIT
    edit_url = f"{base_url}{edit}"
    # DELETE
    delete = DELETE
    delete_url = f"{base_url}{delete}"


class TaskTypeURLS:
    task_type = "task_type"
    base_url = f"{API}{task_type}"
    # POST
    create = CREATE
    create_url = f"{base_url}{create}"
    # GET
    list = LIST
    list_url = f"{base_url}{list}"
    # PATCH
    edit = EDIT + "{task_type_id}/"
    edit_url = f"{base_url}{edit}"
    # DELETE
    delete = DELETE + "{task_type_id}/"
    delete_url = f"{base_url}{delete}"


class TaskURLS:
    task = "task"
    base_url = f"{API}{task}"
    # POST
    create = CREATE
    create_url = f"{base_url}{create}"
    # GET
    list = LIST
    list_url = f"{base_url}{list}"
    # PATCH
    edit = EDIT + "{task_id}/"
    edit_url = f"{base_url}{edit}"
    # DELETE
    delete = DELETE + "{task_id}/"
    delete_url = f"{base_url}{delete}"


