import os,re,psycopg2

def saveData(filename):
        conn=psycopg2.connect(database='report',user='yuchengjie',password='xg09214515',host='127.0.0.1',port='5432')
        cur=conn.cursor()
        j=[]
        for line in open(filename,'r'):
            info=re.search(r'(.*);(.*);(\d+).*;(.*)',line)
            if info!=None:
                jobid=info.group(3)
                j.append(jobid)
        joblist=list(set(j))
        for jobid in joblist:
            dict = {'jobid': jobid}
            cur.execute('SELECT * FROM "Job" WHERE jobid = %d'%int(dict['jobid']))
            jobIs=cur.fetchall()

            if jobIs==[]:
                cur.execute('INSERT INTO "Job" (jobid) VALUES (%d)'%int(dict['jobid']))
            for line in open(filename, 'r'):
                qinfo = re.search(r'(.*);Q;(%s).*;(.*)' % jobid, line)

                sinfo = re.search(r'(.*);S;(%s).*;(.*)' % jobid, line)
                einfo = re.search(r'(.*);E;(%s).*;(.*)' % jobid, line)
                if qinfo:
                    qtime = qinfo.group(1)
                    queue = re.search(r'queue=(\S+)', qinfo.group(3)).group(1)
                    dict['qtime'] = qtime
                    dict['queue'] = queue
                if sinfo:
                    stime = sinfo.group(1)
                    jobname = re.search(r'jobname=(\S+)', sinfo.group(3)).group(1)
                    user = re.search(r'user=(\S+)', sinfo.group(3)).group(1)
                    nodes = re.search(r'Resource_List.neednodes=(\d+)', sinfo.group(3)).group(1)
                    ppn = re.search(r'ppn=(\d+)', sinfo.group(3))
                    if ppn:
                        ppn = ppn.group(1)
                    else:
                        ppn = 1
                    ncpu = int(nodes) * int(ppn)
                    dict['stime'] = stime
                    dict['username'] = user
                    dict['jobname'] = jobname
                    dict['ncpu'] = ncpu
                if einfo:
                    etime = einfo.group(1)
                    walltime = re.search(r'resources_used.walltime=(\S+)', einfo.group(3)).group(1)

                    dict['etime'] = etime
                    dict['walltime'] = walltime
                for key in dict.keys():
                    if key!='jobid':
                        cur.execute('''UPDATE "Job" set %s = '%s' WHERE jobid=%d'''%(key,dict[key],int(dict['jobid'])))
        conn.commit()
        conn.close()



if __name__=='__main__':

    filename='/Users/yuchengjie/Downloads/20180422.dms'
    saveData(filename)
