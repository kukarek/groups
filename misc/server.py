from database import sql
from helper_bot.group import Group

    
groups = []

def groups_init():
    """
    Инициализация обьектов груп из данных бд
    """

    sql.clean_invalid_groups()

    for group_id in sql.get_group_ids():

        groups.append(Group(group_id))

def groups_start():

    for group in groups:
        group.start()

def add_group(group: Group):

    groups.append(group)
    
def get_group(group_id):

    for group in groups:
        if group.GROUP_ID == group_id:
            return group
    
    return None
        
def remove_group(group_name) -> bool:

    for group in groups:
        if group.GROUP_NAME == group_name:
            
            sql.remove_group(group.GROUP_ID)
            group.stop_chat_bot()
            groups.remove(group)
            return True
        
    return False

def get_group(group_id):

    for group in groups:
        if group.GROUP_ID == int(group_id):
            return group
    
    return None


