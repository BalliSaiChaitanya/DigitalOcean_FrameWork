#!/home/gitam/mypython/bin/python
from dcrypt import dc
import ConfigParser as cp
import paramiko
from scp import SCPClient
import getpass
import datetime
import argparse as ap
import subprocess
import sys
import time
import os
import os.path
import signal
import time
import csv
import requests
import json

def conf_initiator(conf_file):
        config = cp.ConfigParser()
        config.read(conf_file)          #       change this to invoke inner modules
        config._sections
        developer = dict(config._sections)
        return  developer


class droplet:

    #__________________init_________________
    def __init__(self,name,conf):
        self.name=name
        self.conf=conf
        signal=dc('None')
        self.header = {'user-agent': 'my-app/0.0.1','Content-Type': 'application/json','Authorization': 'Bearer '+signal}
        print(self.header)
        #'Bearer '+signal
    #user=1:user,user=2:system
    #__________________list_a_single_node__________________
    def get_node(self,user):
        r = requests.get('https://api.digitalocean.com/v2/droplets', headers=self.header)
        #print r.text

        result =json.loads(r.text)
        #single_node
        if user==1:
            print '-----------------------------------------'
            print '|Node-Name     :     nodeID    :   status|'
            print '-----------------------------------------'
        for i in range(0,len(result['droplets'])):
            if result['droplets'][i]['name'] == self.name:
                nodeID=result['droplets'][i]['id']
                nodeIP=result['droplets'][i]['networks']['v4'][0]['ip_address']
                if user==1:
                    print str(name)+'  :  '+str(nodeID)+'  :  '+str(result['droplets'][i]['status'])+'  :  '+str(result['droplets'][i]['memory'])
                    return
                elif user==2:
                    return nodeID
                elif user==3:
                    return nodeIP

     #_________________list_all_nodes__________________
    def get_nodes(self,user):
        datestring = time.strftime("%Y%m%d", time.localtime()) 
	f = open("publiciplist"+datestring,"w+")
        f1= open("publicip"+datestring,"w+")
	r = requests.get('https://api.digitalocean.com/v2/droplets', headers=self.header)
        #print r.text
        nodeIDS=[]
        nodenames=[]
        nodeIPS=[]
	nodestatus=[]  #here
        result =json.loads(r.text)
        if user==1:
            print '-------------------------------------------------'
            print '|Node-Name   :    nodeID    :  status    :  ip   |'
            print '-------------------------------------------------'
        for i in range(0,len(result['droplets'])):
            nodeID=result['droplets'][i]['id']
            nodename=result['droplets'][i]['name']
            nodeIP=result['droplets'][i]['networks']['v4'][0]['ip_address']
	    nodestate=str(result['droplets'][i]['status'])	#here
	    f.write(str(nodename)+"="+str(nodeIP)+"\n")
	    f1.write(str(nodeIP)+"\n")
            if user==1:
                print str(nodename)+'  :  '+str(nodeID)+'  :  '+str(result['droplets'][i]['status'])+'  :  '+str(nodeIP)
            elif user==2:
                nodeIDS.append(nodeID)
                nodenames.append(nodename)
            elif user==3:
                nodenames.append(nodename)
                nodeIPS.append(nodeIP)
	    elif user==4:	#here
		nodestatus.append(nodestate)
        if user==2:
            return nodeIDS,nodenames
        elif user==1:
            return
        elif user==3:
            return nodeIPS,nodenames
	elif user==4:		#here
	    for i in nodestatus:
		print i

	f.close()
	f1.close()

    #_________________list_node_snapshots__________________
    def get_snapshot(self,user,imageID):
        if imageID:
            r = requests.get('https://api.digitalocean.com/v2/images/'+str(imageID), headers=self.header)
            #print r.text
            result =json.loads(r.text)
            #print result
            if user==1:
                print 'Node-Name'+'   :   '+'snapshotID'
            try:
                snapshotID=result['image']['id']
            except:
                print result

            snapshotName=result['image']['name']
            if user==1:
                print str(snapshotName)+' :   '+str(snapshotID)
            elif user==2:
                return snapshotID
        
        else:
            nodeID = self.get_node(2)
            r = requests.get('https://api.digitalocean.com/v2/droplets/'+str(nodeID)+'/snapshots?page=1&per_page=1', headers=self.header)
            snaps=[] 
            result =json.loads(r.text) 
            if user==1:
                print 'Node-Name'+'   :   '+'nodeID'+'    :    '+'snapshot_name'+'  :snapshotID'
            try:
                length=len(result['snapshots'])
            except:
                raise Exception('please enter the name of active-nodes')
            for i in range(0,length):
                snapshotID=result['snapshots'][i]['id']
                snapshotname=result['snapshots'][i]['name']
                if user==1:
                    print str(self.name)+'  :  '+str(nodeID)+'  :  '+str(snapshotname)+'  :  '+str(snapshotID)
                elif user==2:
                    snaps.append(snapshotID)
            if user==1:
                return
            elif user==2:
                return snaps

    '''
    #_________________list_all_nodes_snapshots__________________
    def get_snapshots(self,user):
        nodeIDS,nodenames = self.get_nodes(2)
        snaps=[]
        for i in range(0,len(nodeIDS)):
            nodeID=nodeIDS[i]
            nodename=nodenames[i]
            r = requests.get('https://api.digitalocean.com/v2/droplets/'+str(nodeID)+'/snapshots?page=1&per_page=10', headers=self.header)
            result =json.loads(r.text)
            print result
            for i in range(0,len(result['snapshots'])):
                snapshotID=result['snapshots'][i]['id']
                snapshotName=result['snapshots'][i]['name']
                if user==1:
                    print str(nodename)+'  :  '+str(nodeID)+'  :  '+str(snapshotName)+' :  '+str(snapshotID)
                elif user==2:
                    snaps.append(snapshotID)
        if user==2:
            return snaps
        elif user==1:
            return
    '''

    #_________________list_all_nodes_snapshots__________________
    def get_snapshots(self,user):
        r = requests.get('https://api.digitalocean.com/v2/snapshots?page=1&per_page=100', headers=self.header)
        result =json.loads(r.text)
        #print result
        if user==1:
            print '---------------------------------------------------------'
            print '|nodeID    :  snapshot_name    :  snap_id   :  created_on|'
            print '---------------------------------------------------------'
        for i in range(0,len(result['snapshots'])):
            snapshotID=result['snapshots'][i]['id']
            snapshotName=result['snapshots'][i]['name']
            nodeID=result['snapshots'][i]['resource_id']
            created_at=result['snapshots'][i]['created_at']
            if user==1:
                print str(nodeID)+'  :  '+str(snapshotName)+'  :  '+str(snapshotID)+'   :   '+str(created_at)
            elif user==2:
                snaps.append(snapshotID)
        if user==2:
            return snaps
        elif user==1:
            return

    #__________________create_a_node___________________
    def create_node(self,user,snapID):
        if not snapID:
            with open(self.conf,'r') as f:
                data = json.load(f)
            data['name']=self.name
            data = json.dumps(data)
            r = requests.post('https://api.digitalocean.com/v2/droplets/', data=data, headers=self.header)
            if r.status_code == 202:
                print "created"
            
        else:
            with open(self.conf,'r') as f:
                data = json.load(f)
            #query_database    
            data["image"] = snapID
            #print(data)
            data["name"]=self.name
            print data['name']
            #data['ssh_keys'] =[data['ssh_keys']]
            #print data['ssh_keys']
            data = json.dumps(data)

                
            r = requests.post('https://api.digitalocean.com/v2/droplets/', data=data, headers=self.header)
            if r.status_code == 202:
                print 'created'
            else:
                print r.text

        result =json.loads(r.text)
        try:
            nodeID = result['droplet']['id']
        except:
            print result
        name = result['droplet']['name']
        ###
        ###
        #time.sleep(60)
        ###
        ###
        if user==1:
            print str(name)+'  :  '+str(nodeID)
        elif user==2:
            return name,nodeID
        

    #__________________create_nodes__________________
    def create_nodes(self,user,count,snapID):
        if not snapID:
            with open(self.conf,'r') as f:
                data = json.load(f)
            count1=int(count)
            for i in range(0,count1):
                data['names'].append('node'+str(i))
            print(data)
            data = json.dumps(data)
            #print(data,type(data))

            r = requests.post('https://api.digitalocean.com/v2/droplets/', data=data, headers=self.header)
            if r.status_code == 202:
                print "created"
            
        else:
            with open(self.conf,'r') as f:
                data = json.load(f)
            for i in range(0,int(count)):
                if i==0:
                    data['name'].append('node-master')
                else:
                    data['name'].append('node'+str(i))
            data['image']=snapID
            print(data)
            data = json.dumps(data)
            #print(data,type(data))
         
            r = requests.post('https://api.digitalocean.com/v2/droplets/', data=data, headers=self.header)
            if r.status_code == 202:
                print "created"
            
        result =json.loads(r.text)
        nodeIDS=[]
        nodenames=[]
        for i in range(0,int(count)):
            try:
                nodeIDS.append(result['droplets'][i]['id'])
            except:
                print result
            nodenames.append(result['droplets'][i]['name'])
            
        if user==1:
            for i in range(0,len(nodenames)):
                print str(nodenames[i])+'  :  '+str(nodeIDS[i])
        ###
        ###
        #time.sleep(60)
        ###
        ###
        if user==1:
            return
        elif user==2:
            return nodeIDS,nodenames


    #__________________delete_single_node__________________
    def delete_node(self):
        nodeID = self.get_node(2)
        r = requests.delete('https://api.digitalocean.com/v2/droplets/'+str(nodeID), headers=self.header)
        if r.status_code ==204:
            print str(nodeID)+'  :  '+'deleted'
        return


    #__________________delete_all_nodes__________________
    def delete_nodes(self):
        nodeIDS,nodeName = self.get_nodes(2)
        for nodeID in nodeIDS:
           r = requests.delete('https://api.digitalocean.com/v2/droplets/'+str(nodeID), headers=self.header)
           print('https://api.digitalocean.com/v2/droplets/'+str(nodeID), self.header)
           if r.status_code ==204:
               print str(nodeID)+'  :  '+'deleted'
           else:
               print("unable to delete nodes  ",nodeID)
        return


    #__________________delete_single_snapshot__________________
    def delete_snapshot(self,imageID):
        if imageID:
            r = requests.delete('https://api.digitalocean.com/v2/images/'+str(imageID), headers=self.header)
            if r.status_code ==204:
                print str(imageID)+'    : deleted'
            return
        else:
            snapID=self.get_snapshot(2,None)
            print('https://api.digitalocean.com/v2/images/'+str(snapID), self.header)
            if r.status_code ==204:
                print str(snapID)+' :   deleted'
            return


    #__________________delete_all_snapshots__________________
    def delete_snapshots(self):
        snaps=self.get_snapshots(2)
        for snapID in snaps:
            r = requests.delete('https://api.digitalocean.com/v2/images/'+str(snapID), headers=self.header)
            if r.status_code ==204:
                print('deleted')
        return



    #__________________snapshot_master_node__________________
    def snapshot(self,user,string=""):
        masterID = self.get_node(2)
	#print masterID
	     
	data ={
                  "type": "snapshot",
                  "name": 'st_'+str(self.name)+str(string)+str(datetime.datetime.now()) 
         }
        data=json.dumps(data)

        r = requests.post('https://api.digitalocean.com/v2/droplets/'+str(masterID)+'/actions', data=data, headers=self.header)
        if r.status_code == 201:
            print "taken snapshot"

        result =json.loads(r.text)
        #print result
        if user==1:
            print 'nodeName     :snapshotName'
            print str(self.name)+'  :st_'+str(self.name)+str(string)
            return
        elif user==2:
            return
	

    #__________________shutdown_single_node___________________
    def shutdown_node(self):
        nodeID = self.get_node(2)
        data = {
            "type": "shutdown"
        }
        data = json.dumps(data)
        r = requests.post('https://api.digitalocean.com/v2/droplets/'+str(nodeID)+'/actions', data=data, headers=self.header)
        if r.status_code == 201:
            print str(nodeID)+'  :  '+"shutdown"
        return


    #__________________shutdown_all_nodes__________________
    def shutdown_nodes(self):
        nodeIDS,NodeName = self.get_nodes(2)
        data = {
            "type": "shutdown"
        }
        data = json.dumps(data)
        for nodeID in nodeIDS:
            r = requests.post('https://api.digitalocean.com/v2/droplets/'+str(nodeID)+'/actions', data=data, headers=self.header)
            if r.status_code == 201:
                print str(nodeID)+'  :  '+"shutdown"
        return
   
    #__________________power_off_node__________________
    def power_off_node(self):
        nodeID = self.get_node(2)
        data = {
             "type": "power_off"
         }
        data = json.dumps(data)
        r = requests.post('https://api.digitalocean.com/v2/droplets/'+str(nodeID)+'/actions', data=data, headers=self.header)
        if r.status_code == 201:
            print str(nodeID)+'  :  '+"power_off"
        return

    #__________________power_off_nodes__________________
    def power_off_nodes(self):





        nodeIDS,nodeName = self.get_nodes(2)
        data = {
             "type": "power_off"
         }
        data = json.dumps(data)
        for nodeID in nodeIDS:
            r = requests.post('https://api.digitalocean.com/v2/droplets/'+str(nodeID)+'/actions', data=data, headers=self.header)
            if r.status_code == 201:
                print str(nodeID)+'  :  '+"power_off"
        return

    #__________________power_on_node___________________
    def power_on_node(self):
        nodeID = self.get_node(2)
        data = {
             "type": "power_on"
        }
        data = json.dumps(data)
        r = requests.post('https://api.digitalocean.com/v2/droplets/'+str(nodeID)+'/actions', data=data, headers=self.header)
        if r.status_code == 201:
            print str(nodeID)+'  :  '+"power_on"
        return
 
    #__________________power_on_nodes__________________
    def power_on_nodes(self):
        nodeIDS,nodeName = self.get_nodes(2)
        data = {
            "type": "power_on"
        }
        data = json.dumps(data)
        for nodeID in nodeIDS:
            r = requests.post('https://api.digitalocean.com/v2/droplets/'+str(nodeID)+'/actions', data=data, headers=self.header)
            if r.status_code == 201:
                print str(nodeID)+'  :  '+"power_on"
        return

    def health_check(self,cmd,user,passwd):
        if self.name:
            ip=self.get_node(3)
            self.ssh_connect(ip,cmd,user,1,passwd)
            return
        else:
            ips,names=self.get_nodes(3)
            for i in range(0,len(ips)):
                self.ssh_connect(ip[i],cmd,user,1,passwd)
            return

    def ssh_connect(self,ip,cmd,user,i,passwd):
        port = 22
        username = user
        #password = getpass.getpass(('enter password for '+str(username)+':'))            
        password = passwd
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,port,username,password)

        '''
        SCP operations....Copying the .sh  TO REMOTE
        with SCPClient(ssh.get_transport()) as scp:
        scp.put('shell.sh')
        scp.get('shell.sh')......For multiple commands
        '''
        #Executing Shell script
        #stdin,stdout,stderr=ssh.exec_command('python /opt/woclo/bin/ip.py')
        stdin,stdout,stderr=ssh.exec_command(cmd)
        outlines=stdout.readlines()
        badlines=stderr.readlines()
        resp=''.join(outlines)
        resp1=''.join(outlines)
        ssh.close()
        if i==1:
            if resp:
                print (resp)
            else:
                print(resp1)
            return
        elif i==2:
            if resp:
                print resp
            else:
                print resp1
            return resp

    def etc_hosts(self,cmd,user,passwd):
        ips,names=self.get_nodes(3)
        pvt_ip=[]
        for i in range(0,len(ips)):
            pvt_ip.append(self.ssh_connect(ips[i],cmd,user,2,passwd))
        host='hosts.'+str(datetime.datetime.now())[:10]
        #print host
        host1=host.replace('-','')
        with open(host1,'w') as f:
            for i in range(0,len(names)):
                p=[]
                p.append(pvt_ip[i].strip())
                p.append(names[i])
                pq=' '.join(p)
                print pq
                f.write(pq+'\n')
        host='iplist'+str(datetime.datetime.now())[:10]
        host2=host.replace('-','')
        with open(host2,'w') as f:
            for i in range(0,len(names)):
                p=[]
                p.append(names[i].replace('-','').strip())
                p.append('='.strip())
                p.append(pvt_ip[i].strip())
                pq=''.join(p)
                print pq
                f.write(pq+'\n')
        for i in range(0,len(ips)):
            os.system('scp '+str(host2)+' '+str(user)+'@'+str(ips[i])+':/opt/woclo/bin/ip_list/')
            os.system('scp '+str(host1)+' '+str(user)+'@'+str(ips[i])+':~/')
        return

        

    def name_to_ip_map(self):
        if self.name:
            ip=self.get_node(3)
            p=str(self.name)+':'+str(ip)
            print p
            return
        else:
            ips,names=self.get_nodes(3)
            for i in range(0,len(ips)):
                print str(names[i])+':'+str(ips[i])
            return



    #__________________list_floating_ip__________________
    def get_floating_ips(self,user,ip):
        print "IP=",ip
        if 'all' not in ip:
            r = requests.get('https://api.digitalocean.com/v2/floating_ips/'+str(ip),headers=self.header)
            if r.status_code == 200:
                print r.text
                print 'done'
            result =json.loads(r.text)
            if user==1:
                print '----------------------------'
                print '|floating_ip   :  node_name|'
                print '----------------------------'
            print "Amar2",result
            ip=result['floating_ip']['ip']
            try:
                name=result['floating_ip']['droplet']['name']
            except:
                 name="Not assigned"
            if user==1:
                print str(ip)+'  :  '+str(name)
            elif user==2:
                if name==self.name:
                    return ip
            return
        else:    
            r = requests.get('https://api.digitalocean.com/v2/floating_ips',headers=self.header)
            if r.status_code == 200:
                print 'done'
            result =json.loads(r.text)
            if user==1:
                print '----------------------------'
                print '|floating_ip   :  node_name|'
                print '----------------------------'
            for i in range(0,len(result['floating_ips'])):
                ip=result['floating_ips'][i]['ip']
                try:
                    name=result['floating_ips'][i]['droplet']['name']
                except:
                    name='NULL'
                if user==1:
                    print str(ip)+'  :  '+str(name)
                elif user==2:
                    if name==self.name:
                        return ip
            return


    #__________________create_floating_ip_for_droplet____
    def create_floating_ips(self):
        nodeID,nodeName = self.get_node(2)
        data ={
                "droplet_id" : nodeID,
         }
        data=json.dumps(data)
        r = requests.post('https://api.digitalocean.com/v2/floating_ips',data=data,headers=self.header)
        if r.status_code == 202:
            print 'created'
            print r.text
        else:
            print r.text
        result =json.loads(r.text)
        print '----------------------------'
        print '|floating_ip   :  node_name|'
        print '----------------------------'
        for i in range(0,len(result['floating_ip'])):
            ip=result['floating_ip']['ip']
            name=result['floating_ip']['droplet']['name']
            print str(ip)+'  :  '+str(name)
        return


    #__________________delete_floating_ip__________________
    def delete_floating_ips(self,float_ip):
        if not float_ip:
            float_ip=self.get_floating_ips(2,None)
        r = requests.delete('https://api.digitalocean.com/v2/floating_ips/'+str(float_ip),headers=self.header)
        if r.status_code == 204:
            print str(self.name)+'s ip '+str(float_ip)+' is deleted'
        
        return
    #__________________assigning_floating_ip__________________
    def assign_floating_ips(self,float_ip):
        nodeID = self.get_node(2)
        data ={
                "type" : "assign",
                "droplet_id" : str(nodeID)
         }
        data=json.dumps(data)
        r = requests.post('https://api.digitalocean.com/v2/floating_ips/'+str(float_ip)+'/actions',data=data,headers=self.header)
        if r.status_code == 201:
            print 'assigned'
            print r.text
        else:
            print r.text
        result =json.loads(r.text)
        print result['action']['status']
        return
    #__________________unassigning_floating_ip__________________
    def unassign_floating_ips(self,float_ip):
        data ={
                "type" : "unassign",
         }
        data=json.dumps(data)
        r = requests.post('https://api.digitalocean.com/v2/floating_ips/'+str(float_ip)+'/actions',data=data,headers=self.header)
        if r.status_code == 201:
            print 'unassigned'
            print r.text
        else:
            print r.text
        result =json.loads(r.text)
        print result['action']['status']
        return
    #__________________actions_floating_ip__________________


    """def create_node(self,user,snapID):
        if not snapID:
            with open(self.conf,'r') as f:
                data = json.load(f)
            data['name']=self.name
            data = json.dumps(data)
            r = requests.post('https://api.digitalocean.com/v2/droplets/', data=data, headers=self.header)
            if r.status_code == 202:
                print "created"
            
        else:
            with open(self.conf,'r') as f:
                data = json.load(f)
            #query_database    
            data["image"] = snapID
            #print(data)
            data["name"]=self.name
            print data['name']
            #data['ssh_keys'] =[data['ssh_keys']]
            #print data['ssh_keys']
            data = json.dumps(data)

                
            r = requests.post('https://api.digitalocean.com/v2/droplets/', data=data, headers=self.header)
            if r.status_code == 202:
                print 'created'
            else:
                print r.text

        result =json.loads(r.text)
        try:
            nodeID = result['droplet']['id']
        except:
            print result
        name = result['droplet']['name']
        ###
        ###
        #time.sleep(60)
        ###
        ###
        if user==1:
            print str(name)+'  :  '+str(nodeID)
        elif user==2:
            return name,nodeID"""


    def create_nodes_multi(self,user):

        with open(self.conf,'r') as f:
            data = json.load(f)
        list = self.name.split (",")
        data['names']=list
        data = json.dumps(data)
        print(data)
        count=len(list)
        #data = json.dumps(data)
        #print(data,type(data))

        r = requests.post('https://api.digitalocean.com/v2/droplets/', data=data, headers=self.header)
        if r.status_code == 202:
            print "created"

        result =json.loads(r.text)
        nodeIDS=[]
        nodenames=[]
        for i in range(0,count):
            try:
                nodeIDS.append(result['droplets'][i]['id'])
            except:
                print result
            nodenames.append(result['droplets'][i]['name'])
        
        with open(self.conf,'r') as f:
            data = json.load(f)
        list = []
        data['name']=list
        data= json.dumps(data)
            
        if user==1:
            for i in range(0,len(nodenames)):
                print str(nodenames[i])+'  :  '+str(nodeIDS[i])
        ###
        ###
        #time.sleep(60)
        ###
        ###
        if user==1:
            return
        elif user==2:
            return nodeIDS,nodenames
    
    def delete_nodes_multi(self):
        lis = self.name.split (",")
        count=len(lis)
        for i in range(0,count):
            del_nodes=droplet(lis[i],None)
            nodeID = del_nodes.get_node(2)
            r = requests.delete('https://api.digitalocean.com/v2/droplets/'+str(nodeID), headers=self.header)
            if r.status_code ==204:
                print str(nodeID)+'  :  '+'deleted'
        return





if __name__ ==  '__main__':

    parser = ap.ArgumentParser()
    parser.add_argument('-n', '--name',action='store', dest='name', help='Specify --name of droplet', required=False)
    parser.add_argument('-c', '--conf',action='store', dest='create_conf', help='Specify --create_conf file location', required=False)
    parser.add_argument('-im', '--image_id',action='store', dest='imageID', help='Specify --image_id for deletion', required=False)
    parser.add_argument('-sid', '--snapshot_id',action='store', dest='snapID', help='Specify --snapshot_id for creation', required=False)
    parser.add_argument('-cmd', '--command',action='store', dest='command', help='Specify --command for execution', required=False)
    parser.add_argument('-usr', '--user',action='store', dest='user', help='Specify --user for execution', required=False)
    parser.add_argument('-pwd', '--password',action='store', dest='passwd', help='Specify --password for connection', required=False)
    parser.add_argument('-fip', '--float_ip',action='store', dest='float_ip', help='Specify --float_ip for retrieval', required=False)
    parser.add_argument('-aid', '--action_id',action='store', dest='action_id', help='Specify --action_id for retrieval', required=False)
  


    parser.add_argument('-ln', '--list_node',action='store', dest='lnode', help='Specify --list_node type:single for single,all for all', required=False)
    parser.add_argument('-ls', '--list_snapshot',action='store', dest='lsnap', help='Specify --list_snapshot type:imageid for image,single for single,all for all of droplets', required=False)
    parser.add_argument('-cn', '--create_node',action='store', dest='cnode', help='Specify --create_node type:1 for single,count for all', required=False)
    parser.add_argument('-cs', '--create_snapshot',action='store', dest='csnap', help='Specify --create_snapshot name of the droplet to be used', required=False)
    parser.add_argument('-dn', '--delete_node',action='store', dest='dnode', help='Specify --delete_node type:single for single,all for all', required=False)
    parser.add_argument('-ds', '--delete_snapshots',action='store', dest='dsnap', help='Specify --delete_snapshots type:imageID for direct-deletion,single for a single droplet,all for all', required=False)
    parser.add_argument('-pon', '--power_on_node',action='store', dest='poweron', help='Specify --power_on_node type:single for single,all for all', required=False)
    parser.add_argument('-pfn', '--power_off_node',action='store', dest='poweroff', help='Specify --power_off_node type:single for single,all for all', required=False)
    parser.add_argument('-rdm', '--random_string',action='store', dest='random_str', help='Specify --random_string', required=False)
    parser.add_argument('-sn', '--shutdown_node',action='store', dest='shutdown', help='Specify --shutdown_node type:single for single,all for all', required=False)
    parser.add_argument('-ns', '--node_status',action='store', dest='nstatus', help='Specify --node_status type:single for single,all for all', required=False)
    parser.add_argument('-hc', '--health_nodes',action='store', dest='health', help='Specify --health as check :single for single,all for all', required=False)
    parser.add_argument('-ipn', '--ip_nodes',action='store', dest='know_ip', help='Specify --ip_nodes type: single for single,all for all', required=False)
    parser.add_argument('-etc', '--etc_hosts',action='store', dest='pvt_ip', help='Specify --etc_hosts count of the nodes', required=False)
    parser.add_argument('-lf', '--list_floating_ips',action='store', dest='float_ip', help='Specify --list_floating_ips all', required=False)
    parser.add_argument('-cf', '--create_floating_ip',action='store', dest='create_float', help='Specify --create_floating_ips name of the droplet', required=False)
    parser.add_argument('-df', '--delete_floating_ip',action='store', dest='delete_float', help='Specify --delete_floating_ips name of the droplet or floating_ip to delete', required=False)
    parser.add_argument('-af', '--assign_floating_ip',action='store', dest='assign_float', help='Specify --assign_floating_ips name of the droplet and floating_ip to assign to a droplet', required=False)
    parser.add_argument('-uf', '--unassign_floating_ip',action='store', dest='unassign_float', help='Specify --unassign_floating_ips floating_ip to unassign to a droplet', required=False)
    parser.add_argument('-sf', '--status_float_action',action='store', dest='status_action', help='Specify --status_float_action floating_ip to know the status of actions or with action_id for specific_action', required=False)
    results = parser.parse_args()


    if results.name:
        name=results.name

    if results.imageID:
        imageID=results.imageID


    if results.passwd:
        passwd=results.passwd
    #print name
    if results.create_conf:
        conf=results.create_conf
    elif results.cnode=='single':
        conf="/home/harigopal/Woclo/conf_files/create_single.conf"
    elif results.pvt_ip:
        conf="/home/harigopal/Woclo/conf_files/hosts"
    else:
        conf="/home/harigopal/Woclo/conf_files/create_all.conf"
    
    if results.float_ip:
        float_ip=results.float_ip
    else:
        float_ip=None


    if results.action_id:
        action_id=results.action_id


    if results.lnode:
        if results.lnode=='all':
            drop=droplet(None,None)
            drop.get_nodes(1)
        else:
            if name:
                drop=droplet(name,None)
                drop.get_node(1)
            else:
                raise Exception('please enter the droplet name')

    if results.lsnap:
        if results.lsnap=='all':
            drop=droplet(None,None)
            drop.get_snapshots(1)
        elif results.lsnap=='imageid':
            if imageID:
                drop=droplet(None,None)
                drop.get_snapshot(1,imageID)
            else:
                raise Exception('please provide an imageID to proceed')
        elif results.lsnap=='single':
            if name:
                drop=droplet(name,None)
                drop.get_snapshot(1,None)
            else:
                raise Exception('please provide a name to proceed')

    if results.nstatus:
        if results.nstatus=='all':
            drop=droplet(None,None)
            drop.get_nodes(4)
        else:
            if name:
                drop=droplet(name,None)
                drop.get_node(4)
            else:
                raise Exception('please enter the droplet name')

    if results.cnode:
        if results.cnode=='single':
            if results.snapID:
                drop=droplet(name,conf)
                drop.create_node(1,results.snapID)

            else:
                drop=droplet(name,conf)
                drop.create_node(1,None)

        elif results.cnode=='multi':
            drop=droplet(name,conf)
            drop.create_nodes_multi(1)
        
        else:
            drop=droplet(None,conf)
            drop.create_nodes(1,results.cnode,results.snapID)

    if results.dnode:
        if results.dnode=='all':
            drop=droplet(None,None)
            drop.delete_nodes()
        
        elif results.dnode=='multi':
            drop=droplet(name,None)
            drop.delete_nodes_multi()
        else:
            if name:
                drop=droplet(name,None)
                drop.delete_node()
            else:
                raise Exception('please provide name to proceed')


    if results.csnap:
	if results.random_str:
		string=results.random_str
        	drop=droplet(name,None)
	        drop.snapshot(1,string)
        else: 
        	drop=droplet(name,None)
        	drop.snapshot(1)

    if results.poweron:
        if results.poweron=='all':
            drop=droplet(None,None)
            drop.power_on_nodes()
        else:
            drop=droplet(name,None)
            drop.power_on_node()
    
    if results.poweroff:
        if results.poweroff=='all':
            drop=droplet(None,None)
            drop.power_off_nodes()
        else:
            drop=droplet(name,None)
            drop.power_off_node()
    
    
    
    if results.shutdown:
        if results.shutdown=='all':
            drop=droplet(None,None)
            drop.shutdown_nodes()
        else:
            drop=droplet(name,None)
            drop.shutdown_node()
           

    if not results.user:
        results.user='woir'

    if results.health:
        if results.health=='single':
            drop = droplet(name,None)
            drop.health_check(results.command,results.user,passwd)
        else:
            drop = droplet(None,None)
            drop.health_check(results.command,results.user,passwd)


    if results.dsnap:
        if results.dsnap=='imageID':
            drop=droplet(None,None)
            if imageID:
                drop.delete_snapshot(imageID)
            else:
                raise Exception('please provide imageID')
        elif results.dsnap=='all':
            drop=droplet(None,None)
            drop.delete_snapshots()
        else:
            drop=droplet(name,None)
            drop.delete_snapshot(None)


    if results.know_ip:
        if results.know_ip=='single':
            drop=droplet(name,None)
            drop.name_to_ip_map()
        else:
            drop=droplet(None,None)
            drop.name_to_ip_map()

    if results.pvt_ip:
        drop=droplet(None,conf)
        drop.etc_hosts(results.command,results.user,passwd)

    if results.float_ip:
        if float_ip:
            drop=droplet(None,None)
            print "Amar"
            drop.get_floating_ips(1,float_ip)
        else:
            drop=droplet(None,None)
            drop.get_floating_ips(1,None)


    if results.create_float: 
        drop=droplet(name,None)
        drop.create_floating_ips()

    if results.delete_float:
        if float_ip:
            drop=droplet(None,None)
            drop.delete_floating_ips(float_ip)
        else:
            drop=droplet(name,None)
            drop.delete_floating_ips(None)


    if results.assign_float:
        if float_ip:
            drop=droplet(name,None)
            drop.assign_floating_ips(float_ip)


    if results.unassign_float:
        if float_ip:
            drop=droplet(None,None)
            drop.unassign_floating_ips(float_ip)

    if results.status_action:
        if results.action_id:
            drop=droplet(None,None)
            drop.get_float_ip_actions(float_ip,action_id)
        else:
            drop=droplet(None,None)
            drop.get_float_ip_actions(float_ip,None)
