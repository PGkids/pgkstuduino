# -*- coding: utf-8 -*-

from pgkstuduino import *

j1 = mkjob(print,'hello')
j2 = mkjob(print,'world')
j3 = mkjob(sleep,0.5)

job = lim(rep(par(seq(j1,j3,j2,j3.cp()),
                  seq(j2.cp(),j3.cp(),j1.cp(),j3.cp())),
              1),
          5,
          False)



job.start()
job.join()

    
