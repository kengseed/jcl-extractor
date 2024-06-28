//IAMFT001 JOB (KRUNGSRI),'FTP-AML             ',CLASS=4,               00030003
//         MSGLEVEL=(1,1),MSGCLASS=Y,TIME=1440,REGION=0M                00031000
//* --------------------------------------------------------------------
//S00001    EXEC PGM=DMBATCH,PARM=(YYSLYNN)
//STEPLIB   DD DSN=CONNECT.LINKLIB,DISP=SHR
//DMPUBLIB  DD DSN=PBAY.CONNECT.PROCESS,DISP=SHR
//          DD DSN=CONNECT.PROCESS,DISP=SHR
//DMNETMAP  DD DSN=CONNECT.NETMAP,DISP=SHR
//DMMSGFIL  DD DSN=CONNECT.MSG,DISP=SHR
//DMPRINT   DD SYSOUT=*
//SYSPRINT  DD SYSOUT=*
//SYSIN     DD *
 SIGNON  USERID=(MF2SI,CDIRECT)
  SUBMIT PROC=MF2SITRA CASE=YES -
      &FR1=PAML.DBAT2.SAMF.AMLXML03.DAILY.D%NYMDT0D           -
      &TO1=h13100_amlfxml_103_daily.xml                       -
      NEWNAME=%ESPAPJOB                                       -
      &JOBNM=%ESPAPJOB                                        -
      &SBLANKS=YES
 SIGNOFF
