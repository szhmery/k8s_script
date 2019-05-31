import json
import sys
import os
import time
import subprocess
import shlex
import re
import argparse

sys.path.append('..')

import pexpect

CISCOCM = '4458.2945.45c4'
INTELCM = "0050.f112.decc"

def get_sfid_sid(mac):

    curl = "curl -X GET http://127.0.0.1:32307/v1/sf/cm/" + mac
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
    print "CM:" + mac + " Secondary SFID: " + str(sfid) + " Primary SID: " + str(sid)
    return {"sid": str(sid), "sfid": str(sfid)}

def set_pgs(sfid):

    print '******** Enable PGS ********'
    print 'kubectl get pods -o wide | grep ussche'
    cmd1 = 'kubectl get pods -o wide | grep ussche'
    p = subprocess.Popen(cmd1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result_txt = p.stdout.read()
    print result_txt
    ip_list = re.findall(r'([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*)', result_txt)
    ussche_ip = str(ip_list[0])
    #The same regular rule
    #print re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', result_txt)
    print "usscheduler container IP:" +ussche_ip
    pgs_enable_cli = "curl -X PUT -d '{\"sf_type\":\"pgs\",\"grant_interval\":1000,\"grant_jitter\":0,\"grant_size\":100,\"gpi\":1,\"poll_interval\":2000,\"poll_jitter\":0}' --noproxy "
    pgs_enable_cli = pgs_enable_cli + ussche_ip + " " + ussche_ip +":8080/test/pgs/0/0/" + sfid
    print pgs_enable_cli
    p = subprocess.Popen(pgs_enable_cli, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result_txt = p.stdout.read()
    print result_txt
    if "sucessfully" not in result_txt:
        print "Set PGS failed!"

def set_bwr_for_ussche(switch, sid, sfid):
    print '*********** Enable BWR on cmts-rt-usscheduler **************'
    print 'kubectl get pods -o wide | grep ussche'
    cmd1 = 'kubectl get pods -o wide | grep ussche'
    p = subprocess.Popen(cmd1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result_txt = p.stdout.read()
    print result_txt
    ip_list = re.findall(r'([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*)', result_txt)
    ussche_ip = str(ip_list[0])
    #The same regular rule
    #print re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', result_txt)
    print "usscheduler container IP:" +ussche_ip
    bwr_enable_cli = "curl -X PUT -d '{\"switch\":\"" + switch+ "\",\"sid\":"+sid+"}' --noproxy "
    bwr_enable_cli = bwr_enable_cli + ussche_ip + " " + ussche_ip +":8080/test/bwr/0/0/" + sfid
    print bwr_enable_cli
    p = subprocess.Popen(bwr_enable_cli, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result_txt = p.stdout.read()
    print result_txt
    if "sucessfully" not in result_txt:
        print "Set bwr failed!"

def set_bwr_dp(switch, sid,sfid):
    print '2) Enable BWR'
    print 'kubectl exec -it cmts-dp-macl3vpp-0 vppctl'
    cmd2 = "kubectl exec -it cmts-dp-macl3vpp-0 vppctl"

    child = pexpect.spawn(cmd2)
    # print child.before
    child.expect('vpp-dp#')
    debug_main = 'usmac log set disable main'
    debug_disp = 'usmac log set disable disp'
    debug_mcast = 'usmac log set disable mcast'
    enable_cli = 'usmac test set bwr ' + switch + ' sg 0 md 0 sfid ' + sfid + ' sid ' + sid
    child.sendline(debug_main)
    print child.before
    child.expect('vpp-dp#')
    child.sendline(debug_disp)
    print child.before
    # time.sleep(1)
    child.expect('vpp-dp#')
    child.sendline(debug_mcast)
    print child.before
    # time.sleep(1)
    child.expect('vpp-dp#')
    child.sendline(enable_cli)
    # time.sleep(1)
    print child.before
    child.expect('vpp-dp#')
    print child.before

def main():
    parser = argparse.ArgumentParser(description="set BWR script")
    parser.add_argument("--bwr",default="disable",help="Enable or disable BWR",required=False)
    parser.add_argument("--pgs", default="disable", help="whether set PGS", required=False)
    parser.add_argument("--dp",default="no",help="whether set DP",required=False)
    parser.add_argument("--ussche", default="no", help="whether set ussche", required=False)
    parser.add_argument("--cm", default="cisco", help="choose cm type", required=False)

    args = parser.parse_args()

    bwr_switch = args.bwr
    set_ussche = args.ussche
    set_dp = args.dp
    pgs_switch = args.pgs
    cm_type = args.cm

    CM_MAC = CISCOCM  # default CM is cisco CM

    if cm_type == 'cisco':
        CM_MAC = CISCOCM
    elif cm_type == 'intel':
        CM_MAC = INTELCM
    else:
        print 'Input cable modem type is not right. It should be cisco or intel.'
        exit(0)

    print 'bwr_switch: ' + bwr_switch
    print 'set_ussche: ' + set_ussche
    print 'set_dp: ' + set_dp
    print 'pgs_switch: ' + pgs_switch
    print 'cm_type: ' + cm_type

    # info = {"sid":"0","sfid":"0"}
    info = get_sfid_sid(CM_MAC)

    if set_ussche == "yes":
        set_bwr_for_ussche(bwr_switch, info["sid"], info["sfid"])

    if set_dp == "yes":
        set_bwr_dp(bwr_switch, info["sid"], info["sfid"])

    if pgs_switch == "enable":
        set_pgs(info["sfid"])

if __name__ == "__main__":
    main()
