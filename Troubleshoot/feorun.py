from __future__ import print_function
import sys
sys.path.append("/projects/wagner/amunoz/mainline/utils/autogen")
sys.path.append("/projects/wagner/apps")
import xyz2crystal
import runcrystal
import runqwalk
import copy
import job_control
import os
import json
import yaml
import glob
import taub2

#now we define the job sequence
element_list=[]
element_list.append(xyz2crystal.Xyz2Crystal("/projects/wagner/apps/qwalk_src/utils/autogen/"))
#element_list.append(runcrystal.RunCrystal(
#	submitter = taub2.LocalTaubCrystalSubmitter(
#	nn = 1 ,time = "40:00:00",queue="wagner")))
element_list.append(runcrystal.RunProperties(
	submitter = taub2.LocalTaubPropertiesSubmitter(
	nn=1, np=1,time = "3:30:00",queue="secondary")))
element_list.append(runqwalk.Crystal2QWalk())
element_list.append(runqwalk.QWalkVarianceOptimize(
	submitter = taub2.LocalTaubQwalkSubmitter(
       	nn=1,time = "15:00:00",  queue="wagner")))
element_list.append(runqwalk.QWalkEnergyOptimize(
	submitter = taub2.LocalTaubQwalkSubmitter(
	nn=1, time = "20:00:00",queue="wagner")))
element_list.append(runqwalk.QWalkRunDMC(
	submitter =taub2.LocalTaubQwalkSubmitter(
	nn=2, time = "120:00:00",queue="wagner")))
element_list.append(runqwalk.QWalkRunPostProcess(
        submitter =taub2.LocalTaubQwalkSubmitter(
        nn=1, time = "4:00:00",queue="secondary")))
#element_list.append(runqwalk.QWalkRunMaximize(
#        submitter=taub2.LocalTaubQwalkSubmitter(
#        nn=1,time="10:00:00",queue="physics")))

orderings={"afm":[[1,0,-1],0],
           "fm":[[1,0,1],12] } 
alpha = [25]

results = []
structs=glob.glob("*.xyz")
for i in structs:
  for hyb in alpha:
    for order in orderings.keys():
      job_record=job_control.default_job_record(i)
      job_record['dft']['functional']['hybrid'] = hyb
      job_record['dft']['maxcycle'] = 300
      job_record['dft']['fmixing'] = 95
      job_record['dft']['broyden'] = [0.01,70,10]
      job_record['dft']['spin_polarized']=True
      job_record['dft']['initial_spin']=orderings[order][0]
      job_record['dft']['initial_charges']={'O':-2,'Fe':2}
      job_record['qmc']['dmc']['optimizer']=['energy']
      job_record['total_spin']=orderings[order][1]
      job_record['control']['id']=i+str(hyb)+str(order)
      job_record['qmc']['dmc']['timestep']=[0.01]
      job_record['qmc']['dmc']['target_error']=0.0005
      job_record['qmc']['dmc']['nblock']=4000
      job_record['qmc']['postprocess']['region_fluctuation'] = True      
#      job_record['qmc']['postprocess']['gr'] = True
      job_record['qmc']['postprocess']['density'] = True
      job_record['qmc']['maximize']['jastrow']=['none','twobody']
      job_record['qmc']['maximize']['optimizer']=['energy']
      job_record['qmc']['maximize']['nconfig']=[10000] 

#      job_record['qmc']['postprocess']['obdm'] = True
#      job_record['qmc']['postprocess']['basis'] = "../atomic.basis"
#      job_record['qmc']['postprocess']['orb'] = "../atomic.orb"
#      job_record['qmc']['postprocess']['lowdin'] = True

      results.append(job_control.execute(job_record,element_list))
   
#Save the data, either in JSON:
json.dump(results,open("data.json",'w'))
#or in YAML (which is easier to read for some)
yaml.dump(results,open("data.yaml",'w'),default_flow_style=False)

