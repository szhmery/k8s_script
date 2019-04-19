import json
import sys
import os
import time
import subprocess
import shlex

import pexpect

CISCOCM = '4458.2945.45c4'
INTELCM = "0050.f112.decc"

def main():
    if len(sys.argv) < 3:
        print "The parameters are not right. \n" \
              "Please add parameters, such as:\n" \
              "python bwr_dp.py enable cisco\n" \
              "python bwr_dp.py disable intel\n"
        exit(0)
    for i in range(1, len(sys.argv)):
        print sys.argv[i]
    global count
    global interv
    switch = sys.argv[1]
    cm_type = sys.argv[2]
    # print 'switch: ' + switch
    # print 'cm_type: ' + cm_type
    CM_MAC = ''
    sfid = 0
    sid = 0
    if cm_type == 'cisco':
        CM_MAC = CISCOCM
    elif cm_type == 'intel':
        CM_MAC = INTELCM
    else:
        print 'Input cable modem type is not right. It should be cisco or intel.'
        exit(0)
    curl = "curl -X GET http://127.0.0.1:32307/v1/sf/cm/"+CM_MAC
    p = subprocess.Popen(curl, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    result_txt = p.stdout.read()
    result_json = json.loads(result_txt)

    for sf in result_json:
        if sf['sfkeys']['sfdir'] == 'SF_DIR_US':
            if sf['sfkeys']['sftype'] == 'SF_TYPE_PRIMARY':
                sid = sf['sfkeys']['sid']
                continue
            if sf['sfkeys']['sftype'] == 'SF_TYPE_SECONDARY':
                sfid = sf['sfkeys']['sfid']
                continue
    print "CM:"+CM_MAC+" Secondary SFID: "+str(sfid)+" Primary SID: "+str(sid)

    print 'kubectl exec -it cmts-dp-macl3vpp-0 vppctl'
    cmd = "kubectl exec -it cmts-dp-macl3vpp-0 vppctl"

    child = pexpect.spawn(cmd)
    # print child.before
    child.expect('vpp-dp#')
    debug_main = 'usmac log set disable main'
    debug_disp = 'usmac log set disable disp'
    enable_cli = 'usmac test set bwr '+ switch + ' sfid ' + str(sfid) + ' sid ' + str(sid)
    child.sendline(debug_main)
    print child.before
    child.expect('vpp-dp#')
    child.sendline(debug_disp)
    print child.before
    # time.sleep(1)
    child.expect('vpp-dp#')
    child.sendline(enable_cli)
    # time.sleep(1)
    print child.before
    child.expect('vpp-dp#')
    print child.before


if __name__ == "__main__":
    main()
