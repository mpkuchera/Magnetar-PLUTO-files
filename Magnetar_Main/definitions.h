#define  PHYSICS                        MHD
#define  DIMENSIONS                     3
#define  COMPONENTS                     3
#define  GEOMETRY                       SPHERICAL
#define  BODY_FORCE                     POTENTIAL
#define  FORCED_TURB                    NO
#define  COOLING                        NO
#define  RECONSTRUCTION                 WENO3
#define  TIME_STEPPING                  RK3
#define  DIMENSIONAL_SPLITTING          NO
#define  NTRACER                        0
#define  USER_DEF_PARAMETERS            0

/* -- physics dependent declarations -- */

#define  EOS                            IDEAL
#define  ENTROPY_SWITCH                 NO
#define  DIVB_CONTROL                   DIV_CLEANING
#define  BACKGROUND_FIELD               NO
#define  AMBIPOLAR_DIFFUSION            NO
#define  RESISTIVITY                    NO
#define  HALL_MHD                       NO
#define  THERMAL_CONDUCTION             NO
#define  VISCOSITY                      NO
#define  ROTATING_FRAME                 NO

/* -- user-defined parameters (labels) -- */


/* [Beg] user-defined constants (do not change this line) */

#define  UNIT_DENSITY                   1.e8
#define  UNIT_LENGTH                    1.e10
#define  UNIT_VELOCITY                  1.e10
#define  VTK_VECTOR_DUMP                YES
#define  VTK_TIME_INFO                  YES
#define  WARNING_MESSAGES               NO
#define  INTERNAL_BOUNDARY              YES
#define  RMAX                           2.00
#define  RMIN                           0.00
#define  RGRID                          100



/* [End] user-defined constants (do not change this line) */
