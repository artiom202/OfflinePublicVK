# OfflinePublicVK
# v 0.4
#
 Python 3.5
 
 OfflinePublicVK uses vk and peewee libraries and also bottle framework
 
 To launch program start views.py via python's command shell, open your browser and type url: localhost:9999/[group_id]
 =================================================
 
 Views.py creates local server with port 9999 and when we connecting to it, program gets an id of group which we want to be saved.
 After that program calls get_content() function with id parameter. 
 Function uses VK API to receive a group's wall and then saves it to content.db (images saving to \static\img\ folder).
 When the process finished all posts of the vk group are showed in the browser.
