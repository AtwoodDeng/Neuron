# Automake file for the NEST simulation executable
#
# Marc-Oliver Gewaltig, July 2000
# Jochen Martin Eppler, February 2004
#
# Restructured June 2006, Hans Ekkehard Plesser:
#
# - libnest is now in separate directory nestkernel
# - neststartup has moved out of libnest, and is now part
#   of the nest_SOURCES.  Thus, libnest includes only code
#   truly pertaining to the kernel.  This is necessary to
#   allow other modules to link statically against libnest,
#   and the nest executable to be linked statically against
#   those module libs (example: libmodelmodule.a)
# - now specifying all library directories via LDFLAGS
# - LDADD includes only -l library specifications

defs= @SLI_THREAD_DEFS@ $defs
MAKEFLAGS= @MAKE_FLAGS@

bin_PROGRAMS= nest

nest_SOURCES= main.cpp neststartup.cpp neststartup.h

## make symbols inside nest known to dynamically linked modules via back-linking
nest_LDFLAGS= -export-dynamic 

## All libraries that belong to the NEST project must be listed here
## with explicit paths and as *.la files. This is necessary so that
## dependency tracking and automatic relinking will work. Only external
## libraries should be given with the -l switch. 
nest_LDADD= @LINKED_USER_MODULES@ \
		@LINKED_MODULES@ \
		$(top_builddir)/nestkernel/libnest.la \
		$(top_builddir)/librandom/librandom.la \
		$(top_builddir)/libnestutil/libnestutil.la \
		$(top_builddir)/sli/libsli.la \
		@SLI_LIBS@\
		@GSL_LIBS@\
		@MUSIC_LIBS@\
		@MPI_LIBS@

nest_DEPENDENCIES = @LINKED_MODULES@ \
		$(top_builddir)/nestkernel/libnest.la \
		$(top_builddir)/librandom/librandom.la \
		$(top_builddir)/libnestutil/libnestutil.la \
		$(top_builddir)/sli/libsli.la

AM_CPPFLAGS= -I$(top_srcdir)/libnestutil\
		-I$(top_srcdir)/librandom\
		-I$(top_srcdir)/sli\
		-I$(top_srcdir)/nestkernel\
		@GSL_CFLAGS@ @MUSIC_INCLUDE@ @MPI_INCLUDE@
