//%REX.CRFT068 JOB (KRUNGSRI),'ICRFT068           ',CLASS=4,
//         MSGLEVEL=(1,1),MSGCLASS=Y,TIME=1440,REGION=300M
//*
//  EXPORT SYMLIST=(REG)
//SETREG SET REG=%REG     /* REGION RUN */
//SETXEG SET XEG=%XEG     /* POINT TO ORGINAL MODEL */
//SETZEG SET ZEG=%ZEG     /* INTERFACE REGION RUN */
//*
//*---------------------------------------------------------------------
//*  AFTER JOB ICRCAP01
//*  PUT FILE TO SERVER BAY2PGUPAPP01 (192.168.23.7)
//*---------------------------------------------------------------------
//*
//DELDSN   EXEC PGM=IEFBR14,COND=(0,NE)
//DD0      DD DSN=&REG.PTF.CD.%ESPAPJOB..D%NYMDP7D,
//         DISP=(MOD,DELETE,DELETE),
//         UNIT=SYSDA,SPACE=(TRK,0)
//         DD DSN=&REG.PTF.CD.%ESPAPJOB..D%NYMDT0D,
//         DISP=(MOD,DELETE,DELETE),
//         UNIT=SYSDA,SPACE=(TRK,0)
//*
//PUTFILE  EXEC PGM=DMBATCH,PARM=(YYSLYNN),COND=(0,NE)
//STEPLIB  DD DSN=CONNECT.LINKLIB,DISP=SHR
//DMPUBLIB DD DSN=&REG.BAY.CONNECT.PROCESS,DISP=SHR
//         DD DSN=CONNECT.PROCESS,DISP=SHR
//DMNETMAP DD DSN=CONNECT.NETMAP,DISP=SHR
//DMMSGFIL DD DSN=CONNECT.MSG,DISP=SHR
//DMPRINT  DD SYSOUT=*
//SYSPRINT DD SYSOUT=*
//SYSIN    DD *,SYMBOLS=JCLONLY
 SIGNON  USERID=(CDSADMIN,DIRECT)
      SUBMIT PROC=MF2SU1  PNODE=BAY2                              -
                          SNODE=BAY2PGUPAPP01                     -
      &FR1=&REG.CLA.DBAT.SAMF.ASIAP.RSPTXN.D%NYMDT0D              -
      &TO1=\'/data/BAY/SettleServer/file/\               ||       -
           \CLK_settlement_result_%HDMAN1D..txt'\                 -
      CASE=YES                                                    -
      NEWNAME=%ESPAPJOB                                           -
      &JOBNM=%ESPAPJOB                                            -
      &SBLANKS=YES                                                -
      &TRIDSN=&REG.PTF.CD.%ESPAPJOB..D%NYMDT0D
 SIGNOFF
//*
