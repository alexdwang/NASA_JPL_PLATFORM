'''
Library.py is used to store the values of npn and lpnp under pre_rad, 20k or 50k
Values in this file are constant and should not be modified at any time
'''
CONST_LIBRARY = {'pre_rad': ['* npn prerad off ctp 3b',
                             '.model QNMOD NPN (',
                             '+ IS = 1.68208E-16',
                             '+ BF = 84.058    NF = 0.986787 VAF = 351.9861415',
                             '+ IKF = 9.86E-3  NK = 0.47574  ISE = 7.1029E-15',
                             '+ NE = 2.06453   BR = 0.697    NR = 2',
                             '+ VAR = 100      IKR = 0.1     ISC = 1E-17',
                             '+ NC = 2         RB = 140.86   IRB = 1E-3',
                             '+ RBM = 50       RE = 2        RC = 250.75)',
                             '',
                             '*lpnp prerad off ctp 3b',
                             '.model QLPMOD PNP (',
                             '+ IS = 8.70964E-16',
                             '+ BF = 786.9		NF = 0.99                           VAF = 36.3423711',
                             '+ IKF = 6.30957E-5       NK = 0.52                           ISE = 9.54993E-17',
                             '+ NE = 1.27089           BR = 0.697                          NR = 2',
                             '+ VAR = 100              IKR = 0.1                           ISC = 1E-17',
                             '+ NC = 2                 RB = 758.578                        IRB = 3.6E-5',
                             '+ RBM = 100              RE = 4.096                           RC = 1)'
                             ],


                 '20k': ['* npn 2e4 off ctp 3b',
                         '.model QNMOD NPN  (                      ',
                         '+ IS     = 1.68208E-16',
                         '+ BF     = 45.95           NF     = 0.986787        VAF    = 345.2016293',
                         '+ IKF    = 0.0229087       NK     = 0.47574         ISE    = 1.122018E-14',
                         '+ NE     = 1.65            BR     = 0.697           NR     = 2',
                         '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                         '+ NC     = 2               RB     = 140.86          IRB    = 1E-3',
                         '+ RBM    = 50              RE     = 2               RC     = 250.75)',
                         '',
                         '* lpnp 2e4 off ctp 3b',
                         '.model QLPMOD PNP (',
                         '+ IS     = 8.70964E-16',
                         '+ BF     = 264.9           NF     = 0.99            VAF    = 35.8970174',
                         '+ IKF    = 9.549926E-5     NK     = 0.52            ISE    = 5.495409E-14',
                         '+ NE     = 1.42            BR     = 0.697           NR     = 2',
                         '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                         '+ NC     = 2               RB     = 1E3             IRB    = 3.6E-5',
                         '+ RBM    = 100             RE     = 4.096           RC     = 1)'
                         ],


                 '50k': ['* npn 5e4 off ctp 3b',
                         '.model QNMOD NPN  (',
                         '+ IS     = 1.684E-16',
                         '+ BF     = 38.7            NF     = 0.986787        VAF    = 342.7968454',
                         '+ IKF    = 0.0251189       NK     = 0.47574         ISE    = 1.41254E-13',
                         '+ NE     = 1.82            BR     = 0.697           NR     = 2',
                         '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                         '+ NC     = 2               RB     = 170.83          IRB    = 1E-3',
                         '+ RBM    = 50              RE     = 2               RC     = 366.4)',
                         '',
                         '* lpnp 5e4 off ctp 3b',
                         '.model QLPMOD PNP (',
                         '+ IS     = 1E-15',
                         '+ BF     = 47.4            NF     = 0.99            VAF    = 34.9777903',
                         '+ IKF    = 1.09648E-4      NK     = 0.37            ISE    = 1.65959E-13',
                         '+ NE     = 1.44            BR     = 0.697           NR     = 2',
                         '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                         '+ NC     = 2               RB     = 1.90546E3       IRB    = 3.16228E-5',
                         '+ RBM    = 57.544          RE     = 7.093           RC     = 1)'
                         ]}