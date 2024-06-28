//IFTGPG23 JOB (KRUNGSRI),'FTP-IM              ',CLASS=4,
//         MSGLEVEL=(1,1),MSGCLASS=Y,TIME=1440,REGION=300M
//* --------------------------------------------------------------------
//*   JOB SEND FILE PSP6 TO BAYSCQ FOR ENCRIPT DATA TO USER
//*   PUT FILE TO BAYSCQ ** 192.168.3.4 ** SQ
//*   AFTER JOB IIMMUSC0 SCHEDULE LAST DAY OF MONTH
//* --------------------------------------------------------------------
//DELDSN   EXEC PGM=IEFBR14,COND=(0,NE)
//DD0      DD DSN=PPTF.CD.IFTGPG23.D%NYMDP7D,
//         DISP=(MOD,DELETE,DELETE),
//         UNIT=SYSDA,SPACE=(TRK,0)
//         DD DSN=PPTF.CD.IFTGPG23.D%NYMDT0D,
//         DISP=(MOD,DELETE,DELETE),
//         UNIT=SYSDA,SPACE=(TRK,0)
//*
//PUTFILE  EXEC PGM=DMBATCH,PARM=(YYSLYNN),COND=(0,NE)
//STEPLIB  DD DSN=CONNECT.LINKLIB,DISP=SHR
//DMPUBLIB DD DSN=PBAY.CONNECT.PROCESS,DISP=SHR
//         DD DSN=CONNECT.PROCESS,DISP=SHR
//DMNETMAP DD DSN=CONNECT.NETMAP,DISP=SHR
//DMMSGFIL DD DSN=CONNECT.MSG,DISP=SHR
//DMPRINT  DD SYSOUT=*
//SYSPRINT DD SYSOUT=*
//SYSIN    DD *
 SIGNON  USERID=(CDSADMIN,DIRECT)
     SUBMIT PROC=MF2SW1   PNODE=BAY2                             -
                          SNODE=BAYSCQ                           -
      &FR1=PSP6.IM.IM.B00.IMXGRP.SYUS12.D%NYMDT0D                -
      &TO1=\'C:\\encryption\\logistic\\data\\\   ||              -
           \csp_ca_stmt_grouping.d%nymdt0d'\                     -
      CASE=YES                                                   -
      NEWNAME=IFTGPG23                                           -
      &JOBNM=IFTGPG23                                            -
      &SBLANKS=NO                                                -
      &TRIDSN=PPTF.CD.IFTGPG23.D%NYMDT0D
 SIGNOFF
//*
