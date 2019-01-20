# -*- coding: utf-8 -*-

from pgkstuduino import *

j1 = mkjob(print,'hello')
j2 = mkjob(print,'world')
j3 = mkjob(sleep,0.5)

job = timedjob(
    loopjob(
        parjob(ordjob(j1,j3,j2,j3.clone()),
               ordjob(j2.clone(),j3.clone(),j1.clone(),j3.clone())),
        1),
    5)

job.start()
job.join()

    
