### RPM cms cmssw CMSSW_12_6_0_pre5_G4VECGEOM

Requires: cmssw-tool-conf

%define runGlimpse      yes
%define saveDeps        yes
%define branch          master
%define gitcommit       CMSSW_12_6_0_pre5
# build with debug symbols, and package them in a separate rpm
#subpackage debug disabledes

## INCLUDE cmssw-queue-override

%define source1         git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{gitcommit}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

## IMPORT scram-project-build
## SUBPACKAGE debug IF %subpackageDebug
