# add the channel conda-forge to the environment my_env in anaconda navigator (run as timperle)
# then run conda install pywin32==225 in the terminal (specifically to work with Python 3.7/3.8)

def send_email(my_subject, my_body, **kwargs):
    
    import win32com.client
    import configparser
    from config.config_defs import CONFIG_PATH

    my_attachment = None

    for key, value in kwargs.items():
        if key == 'my_attachment':
            my_attachment = value

    config = configparser.ConfigParser()		
    config.read(CONFIG_PATH)
    my_email = config['email']
    my_to = my_email["to"]
    
    outlook = win32com.client.Dispatch('outlook.application')
    
    mail = outlook.CreateItem(0)
    
    mail.To = my_to
    # mail.CC = 'somebody@company.com'
    mail.Subject = my_subject
    mail.Body = my_body
    # mail.HTMLBody = '<h3>This is HTML Body</h3>'
    
    if my_attachment != None:
        mail.Attachments.Add(my_attachment)
    
    mail.Send()

def write_to_log(log_path, my_text, **kwargs):
    
    import datetime
    # from gen_mods.misc_fns import send_email
    
    email_update = False
    email_subject = None

    for key, value in kwargs.items():
        if key == 'email_update':
            email_update = value
        if key == 'email_subject':
            email_subject = value
            
    # create output text
    output_text = datetime.datetime.now().strftime("%d/%m/%Y: %H:%M:%S") + ': ' + my_text
    
    # print to screen
    print(output_text)
    
    # write to log
    log_file = open(log_path, 'a')
    log_file.write(output_text + '\n')
    log_file.close()
    
    if email_update == True:
        if email_subject != None:
            send_email(email_subject, my_text, my_attachment = log_path)
        else:
            send_email('automated email update', my_text, my_attachment = log_path)
            
def exec_fn(my_fn, my_log):

    import sys
    
    my_stem = '* function ' + my_fn.__name__ + ' in ' + my_fn.__module__
    write_to_log(my_log, my_stem + ' started *')

    # my_fn()
    
    try:
        my_fn()
    except Exception as e:        
        err_msg = '*** code execution failed -- error below ***'  + '\r' + str(e)    
        if my_log != None and len(my_log) > 0:
            write_to_log(my_log, err_msg)
        sys.exit('code execution failed -- check log file')    
    else:    
        if my_log != None and len(my_log) > 0:
            write_to_log(my_log, my_stem + ' succeeded *')
    
def create_empty_log_file(log_path):
    
    log_file = open(log_path, 'a')
    log_file.seek(0)
    log_file.truncate()
    log_file.close()
    
def run_subprocess(file_path, log_path, **kwargs):
    
    import subprocess
    import sys
    from gen_mods.misc_fns import write_to_log

    failure_email = False

    for key, value in kwargs.items():
        if key == 'failure_email':
            failure_email = value
            
    if log_path != None:
        write_to_log(log_path, 'subprocess started: ' + file_path)
    
    r = subprocess.run([file_path], shell=True)

    if r.returncode != 0:
        err_msg = 'subprocess failed: ' + file_path
        if failure_email == True:
            if log_path != None:
                write_to_log(log_path, err_msg, email_update=True, email_subject='code execution failed -- check log file')
        else:
            if log_path != None:
                write_to_log(log_path, err_msg)               
        sys.exit('code execution failed -- check log file')
    else:
        if log_path != None:
            write_to_log(log_path, 'subprocess succeeded: ' + file_path)
        
def create_empty_text_file(my_path):
    
    log_file = open(my_path, 'a')
    log_file.seek(0)
    log_file.truncate()
    log_file.close()
    
def append_to_text_file(my_path, my_text):
     
    # print to screen
    print(my_text)
    
    # write to log
    log_file = open(my_path, 'a')
    log_file.write(my_text + '\n')
    log_file.close()
    
def write_to_new_text_file(my_path, my_text):
    
    create_empty_text_file(my_path)
    append_to_text_file(my_path, my_text)
    
def current_method_name():
    
    import inspect
    
    # [0] is this method's frame and [1] is its parent's
    return inspect.stack()[1].function

def path_is_in_syspath(path):
    
    import os
    import sys
    
    path = os.path.normcase(path)
    return any(os.path.normcase(sp) == path for sp in sys.path)

def remove_from_syspath(path):

    import os
    import sys
    
    # print('old sys path:',sys.path)
    
    while path_is_in_syspath(path) == True:
        sys.path.remove(path)
    
    # print('new sys path:',sys.path)

def append_to_syspath(path):

    import os
    import sys
    
    print('old sys path:',sys.path)
    
    remove_from_syspath(path)    
    sys.path.append(path)
    
    print('new sys path:',sys.path)
    
def remove_from_python_path(path_to_remove):

    import os
    import sys
         
    python_path = os.environ['PYTHONPATH']
    print('old python path:', python_path)
    
    path_list = python_path.split(os.pathsep)
    path_list = [x for x in path_list if x]
    
    if path_to_remove in path_list:
        os.environ['PYTHONPATH'] = ';'.join([x for x in path_list if x != path_to_remove])    
    print('new python path:', os.environ['PYTHONPATH'])    

def append_to_python_path(path_addendum):

    # path_addendum = r'C:\my_local_folder\my_apps\my_python\xx' 
    # ^^^ leave commented out
    
    import os
    import sys
    
    python_path = os.environ['PYTHONPATH']
    print('old python path:', python_path)
    
    path_list = python_path.split(os.pathsep)    
    path_list = [x for x in path_list if x]
        
    if not path_addendum in path_list:
        os.environ['PYTHONPATH'] = python_path + ';' + path_addendum    
    print('new python path:', os.environ['PYTHONPATH'])