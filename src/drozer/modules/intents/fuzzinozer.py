
# Fuzzinozer - intent fuzzer module
#
# Copyright (C) 2015 Intel Corporation
# Author: Cristina Stefania Popescu <cristina.popescu@intel.com>
#
# Licensed under the 3-clause BSD license, see LICENSE and LICENSE.drozer for details


from drozer.modules import Module,common
from commands import *
import os,string
import re
from drozer import android
import random
import sys
import shutil
import itertools
import subprocess
import time
actions = [     'android.intent.action.MAIN',
                    'android.intent.action.VIEW',
                    'android.intent.action.ATTACH_DATA',
                    'android.intent.action.EDIT',
                    'android.intent.action.PICK',
                    'android.intent.action.CHOOSER',
                    'android.intent.action.GET_CONTENT',
                    'android.intent.action.DIAL',
                    'android.intent.action.CALL',
                    'android.intent.action.SEND',
                    'android.intent.action.SENDTO',
                    'android.intent.action.ANSWER',
                    'android.intent.action.INSERT',
                    'android.intent.action.DELETE',
                    'android.intent.action.RUN',
                    'android.intent.action.SYNC',
                    'android.intent.action.PICK_ACTIVITY',
                    'android.intent.action.SEARCH',
                    'android.intent.action.WEB_SEARCH',
                    'android.intent.action.FACTORY_TEST',
                    'android.intent.action.TIME_TICK',
                    'android.intent.action.TIME_CHANGED',
                    'android.intent.action.TIMEZONE_CHANGED',
                    'android.intent.action.BOOT_COMPLETED',
                    'android.intent.action.PACKAGE_ADDED',
                    'android.intent.action.PACKAGE_CHANGED',
                    'android.intent.action.PACKAGE_REMOVED',
                    'android.intent.action.PACKAGE_RESTARTED',
                    'android.intent.action.PACKAGE_DATA_CLEARED',
                    'android.intent.action.UID_REMOVED',
                    'android.intent.action.BATTERY_CHANGED',
                    'android.intent.action.ACTION_POWER_CONNECTED',
                    'android.intent.action.ACTION_POWER_DISCONNECTED',
                    'android.intent.action.ACTION_SHUTDOWN' ] 
categories = [  'android.intent.category.DEFAULT',
                    'android.intent.category.BROWSABLE',
                    'android.intent.category.TAB',
                    'android.intent.category.ALTERNATIVE',
                    'android.intent.category.SELECTED_ALTERNATIVE',
                    'android.intent.category.LAUNCHER',
                    'android.intent.category.INFO',
                    'android.intent.category.HOME',
                    'android.intent.category.PREFERENCE',
                    'android.intent.category.TEST',
                    'android.intent.category.CAR_DOCK',
                    'android.intent.category.DESK_DOCK',
                    'android.intent.category.LE_DESK_DOCK',
                    'android.intent.category.HE_DESK_DOCK',
                    'android.intent.category.CAR_MODE',
                    'android.intent.category.APP_MARKET' ]
extra_keys = [  'android.intent.extra.ALARM_COUNT',
                    'android.intent.extra.BCC',
                    'android.intent.extra.CC',
                    'android.intent.extra.CHANGED_COMPONENT_NAME',
                    'android.intent.extra.DATA_REMOVED',
                    'android.intent.extra.DOCK_STATE',
                    'android.intent.extra.DOCK_STATE_HE_DESK',
                    'android.intent.extra.DOCK_STATE_LE_DESK',
                    'android.intent.extra.DOCK_STATE_CAR',
                    'android.intent.extra.DOCK_STATE_DESK',
                    'android.intent.extra.DOCK_STATE_UNDOCKED',
                    'android.intent.extra.DONT_KILL_APP',
                    'android.intent.extra.EMAIL',
                    'android.intent.extra.INITIAL_INTENTS',
                    'android.intent.extra.INTENT',
                    'android.intent.extra.KEY_EVENT',
                    'android.intent.extra.ORIGINATING_URI',
                    'android.intent.extra.PHONE_NUMBER',
                    'android.intent.extra.REFERRER',
                    'android.intent.extra.REMOTE_INTENT_TOKEN',
                    'android.intent.extra.REPLACING',
                    'android.intent.extra.SHORTCUT_ICON',
                    'android.intent.extra.SHORTCUT_ICON_RESOURCE',
                    'android.intent.extra.SHORTCUT_INTENT',
                    'android.intent.extra.STREAM',
                    'android.intent.extra.SHORTCUT_NAME',
                    'android.intent.extra.SUBJECT',
                    'android.intent.extra.TEMPLATE',
                    'android.intent.extra.TEXT',
                    'android.intent.extra.TITLE',
                    'android.intent.extra.UID' ]
extra_types = [ 'boolean',                 
                    'integer',
                    'string' ]
flags = [       'ACTIVITY_BROUGHT_TO_FRONT',
                    'ACTIVITY_CLEAR_TASK',
                    'ACTIVITY_CLEAR_TOP',
                    'ACTIVITY_CLEAR_WHEN_TASK_RESET',
                    'ACTIVITY_EXCLUDE_FROM_RECENTS',
                    'ACTIVITY_FORWARD_RESULT',
                    'ACTIVITY_LAUNCHED_FROM_HISTORY',
                    'ACTIVITY_MULTIPLE_TASK',
                    'ACTIVITY_NEW_TASK',
                    'ACTIVITY_NO_ANIMATION',
                    'ACTIVITY_NO_HISTORY',
                    'ACTIVITY_NO_USER_ACTION',
                    'ACTIVITY_PREVIOUS_IS_TOP',
                    'ACTIVITY_REORDER_TO_FRONT',
                    'ACTIVITY_RESET_TASK_IF_NEEDED',
                    'ACTIVITY_SINGLE_TOP',
                    'ACTIVITY_TASK_ON_HOME',
                    'FLAG_DEBUG_LOG_RESOLUTION',
                    'FROM_BACKGROUND',
                    'GRANT_READ_URI_PERMISSION',
                    'GRANT_WRITE_URI_PERMISSION',
                    'RECEIVER_REGISTERED_ONLY' ]


def log_in_logcat(log,device):
    '''
    Function which make an entry in the Android system logcat with the running intent
    ''' 
    if device is not "":
        print device
        getoutput("adb -s %s logcat -c " % ( str(device)))
        log_command = "adb -s %s shell  log -p f -t %s" % ( str(device), str(log))
        getoutput(log_command)
    else:
        getoutput("adb logcat -c ")
        log_command = "adb shell log -p f -t %s" % (str(log))
        getoutput(log_command)


 
def save_logcat(fuzz_type,package,component,device,current_dir):
    '''
    Function for saving the system logcat after every intent generated
    '''    
    result_folder = str(current_dir) + "/Results_"+str(fuzz_type)+"_"+str(package)
    if not (os.path.isdir(str(result_folder))):
        os.mkdir(result_folder) 
    file_name=result_folder+"/logcat_"+str(component)+".txt"
    if device is not "":
        event="adb -s %s shell input keyevent 66"%(str(device))
        logcat_cmd = "adb -s %s logcat -d "%(str(device))
    else:
        event="adb shell input keyevent 66"
        logcat_cmd = "adb logcat -d *:E "
    getoutput(event)
    getoutput(event)
    logcat = getoutput(logcat_cmd)
    with open(file_name,'a+') as f:
        f.write(str(logcat))
        f.close()

    parse_logcat(file_name,str(fuzz_type),str(component),str(package),current_dir)
    

def parse_logcat(file_name,fuzz_type,component,package,current_dir):
    '''
    Function for parsing the system logcat and for generating seed files
    '''    
    session=""
    exception_line=""
    lines=[]
    with open(file_name,'r') as f:
        lines = f.readlines()
        found_exception=False
        if lines is not None:
            for line in lines:
                if (line.startswith("F/") & ("type" in line)):
                    with open("all_intents.txt",'a+') as intents_files:
                        session=line.split("):")
                        intents_files.write(session[1])
                if (line.startswith("E/") & ("Caused by" in line)) :
                    found_exception=True
                    exception_line=line
                    exception=exception_line.split(":")[2].strip()
                    new_file_name = str(current_dir) + "/Results_"+str(fuzz_type)+"_"+str(package)+"/seedfile_"+str(component)+"_"+exception+".txt"
                    if os.path.isfile("all_intents.txt"):
                        shutil.copy2("all_intents.txt", new_file_name)
        if not(found_exception):
            os.remove(file_name)
        

def string_generator(size=8, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    '''
    Function for generating random strings and random URIs
    '''    
    return ''.join(random.choice(chars) for x in range(size))


domains=[".com",".org",".net",".int",".gov",".mil"]
def generate_random_uri():
    '''
    Function for generating random uri
    '''
    return random.choice(["http","https"])+"://"+str(string_generator(random.randint(1,100)))+random.choice(domains)
    
    

def random_value(extra_type):
    '''
    Function for generating random value for extra_value parameter according to the extra_type
    '''
    if extra_type=="boolean":
        return random.choice([True, False])
    elif extra_type=="integer":
        return random.randint(1, 1000)
    else:
        return string_generator(random.randint(10, 100))


class Fuzzinozer(Module,common.PackageManager):
    '''
    Intent_fuzzing module class
    '''

    name = "fuzzinozer"
    description = "Android intent fuzzing module "
    examples = ""
    author = "Popescu Cristina Stefania "
    date = "2015-10-08"
    license = "3 clause BSD"
    path = ["intents"]

    def add_arguments(self, parser):
        parser.add_argument("--package_name", help="specify name of package to test ")
        parser.add_argument("--test_all", action='store_true', help="test all packages")
        parser.add_argument("--broadcast_intent", action='store_true', help="send broadcast intent; you also need to select package_name or test_all params")
        parser.add_argument("--fuzzing_intent", action='store_true', help="send intent with random action,category,flag; you also need to select --package_name or --test_all params")
        parser.add_argument("--complete_test", action='store_true', help="test with all actions,categories,flags,extras existent in Android; you also need to select --package_name or --test_all params")
        parser.add_argument("--select_fuzz_parameters", help="give the parameters you want to fuzz (action,category,flag,extras); you also need to select --fuzzing_intent and--package_name or --test_all params")
        parser.add_argument("--save_state",action='store_true', help="save the running state from complete_test session")
        parser.add_argument("--reload", help="reload the running state parameters in terms of component,action,category,flag,key as indices")
        parser.add_argument("--run_seed", help="select the seed file you want to run")
        parser.add_argument("--device", help="used only for automated tests")
        parser.add_argument("--template_fuzz_parameters_number", help="give the number of the parameters you want to fuzz; you also need to select --fuzzing_intent and --package_name or --test_all params")
        parser.add_argument("--dos_attack", help="give the number of intents you want to test")
                        
    def execute(self, arguments):
        package_name=""
        fuzz_parameters=[]
        fuzz_number=7
        device=""
        intents=1


        if arguments.device:
            device=arguments.device
        test_all=0
        params=""

    #set results folder (~/fuzzinozer_results is implicit value); if you want to change it go to "~/.bashrc file"
        self.current_dir=""        
        pm=self.packageManager() 
        env=os.environ.get("FUZZ_RES")
        if env is None:
            os.environ["FUZZ_RES"]=os.path.expanduser("~")+"/fuzzinozer_results"
            env=os.environ.get("FUZZ_RES")
        self.current_dir=str(env) 
        if not os.path.isdir(env):
            getoutput("mkdir " + env)
        found=0  
        if arguments.select_fuzz_parameters:
            params=arguments.select_fuzz_parameters

        if arguments.template_fuzz_parameters_number:
            fuzz_number=int(arguments.template_fuzz_parameters_number)
            fuzz_parameters=self.generate_templates(fuzz_number)
            intents=len(fuzz_parameters)

        if arguments.dos_attack:
            found=1
            nr=int(arguments.dos_attack)
            self.dos(nr)
            total_intents=nr

        if arguments.complete_test:
            intents=len(actions)*len(flags)*len(extra_keys)*len(extra_types)*len(categories)
	    

        total_intents=0
        if arguments.test_all:
            test_all=1
            for package in self.packageManager().getPackages():
                packageNameString = package.applicationInfo.packageName
                activities=[]
                if arguments.fuzzing_intent:
                    activities=FuzzinozerPackageManager(self).getActivities(str(packageNameString))
                elif arguments.broadcast_intent:
                    activities=FuzzinozerPackageManager(self).getReceivers(str(packageNameString))
                if (activities is not None):
                    total_intents=total_intents+intents*len(activities)

        if arguments.package_name:
            activities=[]
            package_name=arguments.package_name
            if arguments.broadcast_intent:
                activities=FuzzinozerPackageManager(self).getReceivers(package_name)
            else:
                activities=FuzzinozerPackageManager(self).getActivities(package_name)
            if (activities is not None):
                total_intents=total_intents+intents*len(activities)
            print("Number of intents:"+ str(total_intents) + "\n")
        
       
        seed_file=""
        if arguments.run_seed:
            found=1
            seed_file=arguments.run_seed
            if seed_file is not "":
                print "RUN INTENTS FROM " +  seed_file
                total_intents=self.run_seed_file(seed_file,device)

        if arguments.package_name or arguments.test_all:
            if os.path.isfile("all_intents.txt"):
                os.remove("all_intents.txt")
                
            if arguments.broadcast_intent:
                for package in self.packageManager().getPackages():
                    packageNameString = str(package.applicationInfo.packageName)
                    if (packageNameString==package_name or test_all==1):
                       found=1
                       pm=self.packageManager()
                       receivers=[]
                       receivers=FuzzinozerPackageManager(self).getReceivers(packageNameString)
                       if (receivers is not None):
                            for val in receivers:
                                msg="broadcast_intent " + "type: broadcast"+" package: "+ packageNameString + " component: "+ str(val) + " " 
                                print msg
                                log_in_logcat(str(msg),device)
                                intent = android.Intent(component=(packageNameString,str(val)))
                                try:
                                    self.getContext().sendBroadcast(intent.buildIn(self)) 
                                except:
                                    pass
                                save_logcat("broadcast",packageNameString,val,device,self.current_dir)
                    result_folder = str(self.current_dir) + "/Results_"+str('broadcast')+"_"+str(packageNameString)
                    if os.path.isdir(result_folder):
                        if os.listdir(result_folder) == []:
                            shutil.rmtree(result_folder)
                
                                
            elif arguments.fuzzing_intent:
                for package in self.packageManager().getPackages():
                    packageNameString = str(package.applicationInfo.packageName)
                    if (packageNameString==package_name or test_all==1):
                        found=1
                        pm=self.packageManager()
                        activities=[]
                        activities=FuzzinozerPackageManager(self).getActivities(packageNameString)
                        if (activities is not None):
                            for val in activities:
                                #if template_fuzz_parameters_number run all the generated templates
                                if (fuzz_number<7):
                                    for temp in fuzz_parameters:
                                        print ("TEMPLATE:" + temp)
                                        extra_type=str(random.choice(extra_types))
                                        if temp[0]=="0":
                                            ac=random.choice(actions)
                                        else:
                                            ac=string_generator(random.randint(10, 100))
                                        if temp[1]=="0":
                                            cat=random.choice(categories)
                                        else:
                                            cat=string_generator(random.randint(10, 100))
                                        if temp[2]=="0":
                                            uri=string_generator(random.randint(10, 100))
                                        else:
                                            uri=string_generator(random.randint(10, 100))
                                        if temp[3]=="0":
                                            key=random.choice(extra_keys)
                                        else:
                                            key=string_generator(random.randint(10, 100))
                                        if temp[4]=="0":
                                            extra_value=str(random_value(extra_type))
                                        else:
                                            extra_value=string_generator(random.randint(10, 100))
                                        if temp[5]=="0":
                                            fl=random.choice(flags)
                                        else:
                                            fl=string_generator(random.randint(10, 100))
                                        self.run_intent(packageNameString,val,uri,ac,cat,fl,extra_type,key,extra_value,device)
                                        
                                else:
                                    uri=generate_random_uri()
                                    if "category" in params: 
                                        cat=string_generator(random.randint(10, 100))
                                    else:
                                        cat=random.choice(categories)
                                    if "action" in params: 
                                        ac=string_generator(random.randint(10, 100))
                                    else:
                                        ac=random.choice(actions)
                                    if "flag" in params: 
                                        fl=string_generator(random.randint(10, 100))
                                    else:
                                        fl=random.choice(flags)
                                    if "extra_key" in params: 
                                        key=string_generator(random.randint(10, 100))
                                    else:
                                        key=random.choice(extra_keys)
                                    extra_type=str(random.choice(extra_types))
                                    extra_value=str(random_value(extra_type))
                                    self.run_intent(packageNameString,val,uri,ac,cat,fl,extra_type,key,extra_value,device)                 
            elif arguments.complete_test:
                for package in self.packageManager().getPackages():
                    packageNameString = package.applicationInfo.packageName
                    if (packageNameString==package_name or arguments.test_all):
                        found=1
                        save_state=False
                        reload_option=False
                        aux_num=" "
                        if arguments.save_state:
                            save_state=True
                        if arguments.reload:
                            reload_option=True
                            aux_num=arguments.reload
                        self.test_all_possible(packageNameString,device,self.current_dir,save_state,reload_option,aux_num)
                        print("Total number of intents:"+ str(total_intents) + "\n")
            else:
                print "Wrong parameters!! run help to see the parameters"
        print("Total number of intents:"+ str(total_intents) + "\n")
        if (found==0):
            print ("Package not installed")
  
      

    def dos(self,intents):
        '''
        Function for generating intents of random sizes;
        '''
        print "DoS against BLUETOOTH"
        os.system("touch buffer.sh")
        fileName="buffer.sh"
	#hardcoded package activity
        pack_act = "com.android.bluetooth/.opp.BluetoothOppLauncherActivity"

        for i in range(intents):
            with open(fileName,"w+") as f:
                rand_int_f = random.randint(-2147483648,2147483647) #flag might be an integer between -2147483648 and 2147483647
                rand_size_a = random.randint(1,10)
                rand_size_c = random.randint(1,10)
                rand_size_d = random.randint(1,10)
                rand_size_ek = random.randint(1,10)
                rand_size_ev = random.randint(1,10)
                f.write("am start -n "+pack_act+" -f "+ str(rand_int_f)+ " -a "+string_generator(rand_size_a)+" -c "+string_generator(rand_size_c)+" -d "+string_generator(rand_size_d) +"-e "+string_generator(rand_size_ek)+" "+string_generator(rand_size_ev))
            os.system("chmod 777 "+fileName)
            os.system("adb push buffer.sh /data/local/tmp/buffer.sh")
            os.system("adb shell sh /data/local/tmp/buffer.sh")
            print str(rand_int_f) + " rand_int_f"
            print str(rand_size_a) + " rand_size_a"
            print str(rand_size_c) + " rand_size_c"
            print str(rand_size_d) + " rand_size_d"
            print str(rand_size_ek) + " rand_size_ek"
            print str(rand_size_ev) + " rand_size_ev"



    def test_all_possible(self,package_name,device,current_dir,save_state,reload_option,aux_num):
        '''
        Fuction for runing a complete test (with all categories,flags and actions) for a package
        '''
        activities=[]
        activities=FuzzinozerPackageManager(self).getActivities(package_name)
        aux_comp=0
        aux_cat=0
        aux_ac=0
        aux_fl=0
        aux_key=0
        if (reload_option):
            aux_comp=int(aux_num.split(" ")[0])
            if (aux_comp<0) or (aux_comp>len(activities)):
                aux_comp=0
            aux_ac=int(aux_num.split(" ")[1])
            if (aux_ac<0) or (aux_ac>len(actions)):
                aux_ac=0
            aux_cat=int(aux_num.split(" ")[2])
            if (aux_cat<0) or (aux_cat>len(categories)):
                aux_cat=0
            aux_fl=int(aux_num.split(" ")[3])
            if (aux_fl<0) or (aux_fl>len(flags)):
                aux_fl=0
            aux_key=int(aux_num.split(" ")[4])
            if (aux_key<0) or (aux_key>len(extra_keys)):
                aux_key=0
        if (activities is not None):
            for component in activities[aux_comp:]:
                for ac in actions[aux_ac:]:
                    for cat in categories[aux_cat:]:
                        for fl in flags[aux_fl:]:
                            for key in extra_keys[aux_key:]:
                                for extra_type in extra_types:
                                    extra_value=random_value(extra_type)
                                    uri=generate_random_uri()
                                    if (save_state):
                                        with open(str(current_dir+"/complete_test-saved.txt"),'w+') as f:
                                            f.write(str(activities.index(component))+ " " + str(actions.index(ac)) + " " +str(categories.index(cat)) + " " + str(flags.index(fl)) + " " + str(extra_keys.index(key)))
                                            f.close()
                                    self.run_intent(package_name,component,uri,ac,cat,fl,extra_type,key,extra_value,device)
  
                                  

    def run_seed_file(self,file_name,device):
        '''
        Fuction for runing all intents from a seed file
        '''	
        with open(file_name,'r') as f:
            lines = f.readlines()
            if lines is not None:
                intents=len(lines)
                print("Number of intents:"+ str(intents) + "\n")
                for line in lines:
                    parse_intent=line.split(" ")
                    intent_type=parse_intent[2]
                    package_name=parse_intent[4]
                    component=parse_intent[6]
                    if intent_type=='fuzzing':
                        uri=parse_intent[8]
                        cat=parse_intent[10]
                        ac=parse_intent[12]
                        fl=parse_intent[14]
                        extra_type=parse_intent[16]
                        key=parse_intent[18]
                        extra_value=parse_intent[20]
                        msg=intent_type + " " + package_name + " " + component + " " + uri + " " + cat + " " + ac + " " + fl+ " " + extra_type+ " " + key + " " + extra_value
                        print msg 
                        log_in_logcat(str(msg),device)	                        
                        try:
                            intent = android.Intent(component=(package_name ,str(component)),flags=[fl],data_uri=uri,category=cat,action=ac,extras=[(str(extra_type), str(key), str(extra_value))])
                            intent.flags.append("ACTIVITY_NEW_TASK")
                            self.getContext().startActivity(intent.buildIn(self))
                        except:
                            e = sys.exc_info()[0]
              
                    elif intent_type=='broadcast':
                        intent = android.Intent(component=(package_name,str(component)))
                        msg=intent_type + " " + package_name + " " + component
                        print msg
                        log_in_logcat(str(msg),device)    
                        try:
                            self.getContext().sendBroadcast(intent.buildIn(self))
                        except:
                            pass
            return intents
                            


    def generate_templates(self,number):
        '''
        Fuction for generating all the templates with a given number of parameters
        '''
        list=[]
        for el in itertools.product("01",repeat=6):
            elem="".join(el)
            list.append(elem)
        template_list=[elem for elem in list if elem.count("1")==number]
        return template_list



    def run_intent(self,package_name,component,uri,ac,cat,fl,extra_type,key,extra_value,device):
        '''
        Function for running fuzzy intent with parameters
        '''
        flag=[]
        msg="fuzzing_intent " +"type: fuzzing" +" package: "+ str(package_name)  + " component: "+ str(component)  + " data_uri: "+ str(uri) + " category: "+ str(cat) + " action: "+ str(ac) + " flag: "+ str(fl) +" extra_type: "+ str(extra_type) + " extra_key: "+ str(key) + " extra_value: "+ str(extra_value)
        print msg
        log_in_logcat(str(msg),device)
        try:
            intent = android.Intent(component=(package_name ,str(component)),flags=[fl],data_uri=uri,category=cat,action=ac,extras=[(str(extra_type), str(key), str(extra_value))])
            #you can't open an activity from another app without "ACTIVITY_NEW_TASK" flag
            intent.flags.append("ACTIVITY_NEW_TASK")
            self.getContext().startActivity(intent.buildIn(self))
        except:
            e = sys.exc_info()[0]
            #print e
        save_logcat("fuzzing",str(package_name),str(component),device,self.current_dir)
        

        

class FuzzinozerPackageManager(common.PackageManager.PackageManagerProxy):
   
    def getReceivers(self, packageNameString):
        """
	Get all Receivers from a package.
	"""
        receivers_array=[]
        receivers=[]
        receivers= self.packageManager().getPackageInfo(packageNameString , self.packageManager().GET_RECEIVERS).receivers
        if (str(receivers)=='null'):
            print ("No receivers found for " + packageNameString)             
        else:
            for pack in receivers:
                receivers_array.append(str(pack.name))
            return receivers_array


    def getActivities(self, packageNameString):
        """
        Get all Activities from a package.
        """
        activities=[]
        activities_array=[]
        activities= self.packageManager().getPackageInfo(packageNameString , self.packageManager().GET_ACTIVITIES).activities
        if (str(activities)=='null' or activities==[]):
            print ("No activities found for " + packageNameString)
        else:
            for activity in activities :
                activities_array.append(str(activity.name))
            return activities_array
