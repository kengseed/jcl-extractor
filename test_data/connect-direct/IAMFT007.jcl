//IAMFT007 JOB (KRUNGSRI),'RESERVE BY NUTT     ',CLASS=4,
//         MSGLEVEL=(1,1),MSGCLASS=Y,TIME=1440,REGION=0M
//******************************************
//* THIS JOB MOVE TO PDSI.JCLLIB.MASTER.AM *
//* THIS JOB MOVE TO PDSI.JCLLIB.MASTER.AM *
//* THIS JOB MOVE TO PDSI.JCLLIB.MASTER.AM *
//* THIS JOB MOVE TO PDSI.JCLLIB.MASTER.AM *
//******************************************
//
//**********************************************************************
//** BY PASS JOB WHEN PNSI.ANY.DBAT2.SAMF.SMS.F*.D%NYMDT0D ARE EMPTY
//**********************************************************************
//JOBLIB   DD DISP=SHR,DSN=SYS2.ESP.LOAD
//*
//BYPASS   EXEC PGM=ESP,PARM='SUBSYSTEM(ESP5)'
//SYSPRINT DD SYSOUT=*
//SYSIN    DD *
 AJ IAMFT007.WAITCD COMPLETE APPL(PASIAM.0)
//*
