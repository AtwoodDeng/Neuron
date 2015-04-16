/* libnestutil/config.h.  Generated from config.h.in by configure.  */
/* libnestutil/config.h.in.  Generated from configure.ac by autoheader.  */

/* tics per ms in simulation */
/* #undef CONFIG_TICS_PER_MS */

/* tics per step in simulation */
/* #undef CONFIG_TICS_PER_STEP */

/* define if the compiler does not include *.h headers ISO conformant */
/* #undef HAVE_ALPHA_CXX_STD_BUG */

/* define if the compiler ignores cmath makros */
/* #undef HAVE_CMATH_MAKROS_IGNORED */

/* Define to 1 if you have the <dlfcn.h> header file. */
#define HAVE_DLFCN_H 1

/* Define to 1 if you have the `execv' function. */
#define HAVE_EXECV 1

/* "Define if expm1() is available" */
#define HAVE_EXPM1 1

/* Define to 1 if you have the `fork' function. */
#define HAVE_FORK 1

/* Is the GNU Science Library available (ver. >= 1.0)? */
/* #undef HAVE_GSL */

/* Is GSL Version >= 1.11? */
/* #undef HAVE_GSL_1_11 */

/* Is GSL Version >= 1.2? */
/* #undef HAVE_GSL_1_2 */

/* Do we have the inline macro in C? */
#define HAVE_INLINE 1

/* Define to 1 if you have the <inttypes.h> header file. */
#define HAVE_INTTYPES_H 1

/* define for istream */
#define HAVE_ISTREAM /**/

/* Havel libltdl, can load dynamic modules */
#define HAVE_LIBLTDL 1

/* define if we have usable long long type. */
#define HAVE_LONG_LONG 1

/* Define to 1 if you have the <memory.h> header file. */
#define HAVE_MEMORY_H 1

/* MPI is available. */
/* #undef HAVE_MPI */

/* MUSIC support enabled? */
/* #undef HAVE_MUSIC */

/* define if M_E is defined */
#define HAVE_M_E /**/

/* define if M_PI is defined */
#define HAVE_M_PI /**/

/* define for ostream */
#define HAVE_OSTREAM /**/

/* Define to 1 if you have the `pclose' function. */
#define HAVE_PCLOSE 1

/* Define to 1 if you have the `popen' function. */
#define HAVE_POPEN 1

/* pthreads are available */
/* #undef HAVE_PTHREADS */

/* define if the compiler ignores symbolic names in pthread.h */
/* #undef HAVE_PTHREAD_IGNORED */

/* define if pthread_setconcurrency is available */
/* #undef HAVE_PTHREAD_SETCONCURRENCY */

/* Use GNU libreadline */
#define HAVE_READLINE 1

/* Define to 1 if you have the `setenv' function. */
#define HAVE_SETENV 1

/* Define to 1 if you have the `sigaction' function. */
#define HAVE_SIGACTION 1

/* define if the compiler ignores symbolic signal names in signal.h */
/* #undef HAVE_SIGUSR_IGNORED */

/* define for sstream */
#define HAVE_SSTREAM /**/

/* define if the compiler fails on static template member declaration */
/* #undef HAVE_STATIC_TEMPLATE_DECLARATION_FAILS */

/* Define to 1 if you have the <stdint.h> header file. */
#define HAVE_STDINT_H 1

/* Define to 1 if you have the <stdlib.h> header file. */
#define HAVE_STDLIB_H 1

/* define for STL vector capacity base unity */
#define HAVE_STL_VECTOR_CAPACITY_BASE_UNITY /**/

/* define for STL vector capacity doubling strategy */
#define HAVE_STL_VECTOR_CAPACITY_DOUBLING /**/

/* Define to 1 if you have the <strings.h> header file. */
#define HAVE_STRINGS_H 1

/* Define to 1 if you have the <string.h> header file. */
#define HAVE_STRING_H 1

/* Define to 1 if you have the <sys/stat.h> header file. */
#define HAVE_SYS_STAT_H 1

/* Define to 1 if you have the <sys/types.h> header file. */
#define HAVE_SYS_TYPES_H 1

/* Tics per millisecond specified? */
/* #undef HAVE_TICS_PER_MS */

/* Tics per step specified? */
/* #undef HAVE_TICS_PER_STEP */

/* Define to 1 if you have the <unistd.h> header file. */
#define HAVE_UNISTD_H 1

/* Vampir support enabled? */
/* #undef HAVE_VAMPIR */

/* Configuring for Blue Gene/L */
/* #undef IS_BLUEGENE_L */

/* Configuring for Blue Gene/P */
/* #undef IS_BLUEGENE_P */

/* Configuring for Blue Gene/Q */
/* #undef IS_BLUEGENE_Q */

/* Configuring for K */
/* #undef IS_K */

/* Configuring for K interactive build */
/* #undef IS_K_INTERACTIVE */

/* Define to the sub-directory in which libtool stores uninstalled libraries.
   */
#define LT_OBJDIR ".libs/"

/* Name of package */
#define PACKAGE "nest"

/* Define to the address where bug reports for this package should be sent. */
#define PACKAGE_BUGREPORT "nest_user@nest-initiative.org"

/* Define to the full name of this package. */
#define PACKAGE_NAME "nest"

/* Define to the full name and version of this package. */
#define PACKAGE_STRING "nest 2.2.2"

/* Define to the one symbol short name of this package. */
#define PACKAGE_TARNAME "nest"

/* Define to the home page for this package. */
#define PACKAGE_URL ""

/* Define to the version of this package. */
#define PACKAGE_VERSION "2.2.2"

/* Use PS array construction semantics */
#define PS_ARRAYS 1

/* Define to 1 if you have the ANSI C header files. */
#define STDC_HEADERS 1

/* Enable extensions on AIX 3, Interix.  */
#ifndef _ALL_SOURCE
# define _ALL_SOURCE 1
#endif
/* Enable GNU extensions on systems that have them.  */
#ifndef _GNU_SOURCE
# define _GNU_SOURCE 1
#endif
/* Enable threading extensions on Solaris.  */
#ifndef _POSIX_PTHREAD_SEMANTICS
# define _POSIX_PTHREAD_SEMANTICS 1
#endif
/* Enable extensions on HP NonStop.  */
#ifndef _TANDEM_SOURCE
# define _TANDEM_SOURCE 1
#endif
/* Enable general extensions on Solaris.  */
#ifndef __EXTENSIONS__
# define __EXTENSIONS__ 1
#endif


/* Version number of package */
#define VERSION "2.2.2"

/* Define to 1 if on MINIX. */
/* #undef _MINIX */

/* Define to 2 if the system does not provide POSIX.1 features except with
   this defined. */
/* #undef _POSIX_1_SOURCE */

/* Define to 1 if you need to in order for `stat' and other things to work. */
/* #undef _POSIX_SOURCE */

/* Define as `__inline' or `__inline__' if that's what the
    C compiler calls it or to nothing if it is not supported. */
#ifndef __cplusplus
/* # undef inline */
#endif
