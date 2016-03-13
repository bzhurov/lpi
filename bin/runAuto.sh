#!/bin/bash

print_help()
{
cat << EOF

 bash script for running auto for any model
 
 usage : $0 [OPTIONS]
	
 	-d <dir>	auto base dir
 	-w <dir>	auto work dir
 	-c <file>	file with runtime parameters
 	-t <dir>	dir with auto templates
 	-p <parName>=<parValue>	single parameter implementation
 	-r <rtpName>=<rtpValue>	technical parameter implementation
 	-i <varName>=<varValue> initial values of variables
 	-g <graph>	draw graph
 	-n <name>	prefix for calculations name
EOF
}

echo $0 $@;

inp_bdir=;
inp_wdir=;
inp_conf=;
inp_temp=;
inp_log=;
inp_graph=;
inp_name=;
inp_parnames=();
inp_parvals=();
inp_rtpnames=();
inp_rtpvals=();
inp_varnames=();
inp_varvals=();

while getopts "d:w:c:t:p:r:i:g:n:" OPTION; do
	case $OPTION in
		d)
			inp_bdir=$OPTARG;
			;;
		w)
			inp_wdir=$OPTARG;
			;;
		c)
			inp_conf=$OPTARG;
			;;
		t)
			inp_temp=$OPTARG;
			;;
		n)
			inp_name=$OPTARG;
			;;	
		p)
			tmp_name=`echo $OPTARG | cut -d '=' -f 1`;
			tmp_val=`echo $OPTARG | cut -d '=' -f 2`;
			inp_parnames+=(${tmp_name});
			inp_parvals+=(${tmp_val});
			;;
		r)
			tmp_tname=`echo $OPTARG | cut -d '=' -f 1`;
			tmp_tval=`echo $OPTARG | cut -d '=' -f 2`;
			inp_rtpnames+=(${tmp_tname});
			inp_rtpvals+=(${tmp_tval});
			;;
		i)
			tmp_iname=`echo $OPTARG | cut -d '=' -f 1`;
			tmp_ival=`echo $OPTARG | cut -d '=' -f 2`;
			inp_varnames+=(${tmp_iname});
			inp_varvals+=(${tmp_ival});
			;;
		g)
			inp_graph=$OPTARG;
			;;
		?)
			print_help;
			exit 1
			;;
	esac
done

#initialize input parameters############################################################################################
baseDir=
workDir=
tempDir=
autoLog=
calcPrefix=
calcName=
parPrefix=
rtpPrefix=
varPrefix=
parNames=()
parVals=()
rtpNames=()
rtpVals=()
varNames=()
varVals=()
#read config from config file###########################################################################################
if [[ "${inp_conf}" != "" ]]; then
	if [[ ! -f "${inp_conf}" ]]; then
		echo " error : cant find config file \`${inp_conf}'";
		exit -1;
	fi
	
	for rwline in `cat ${inp_conf}`; do
		ltype=`echo $rwline | cut -d ';' -f 1`;
		lvalue=`echo $rwline | cut -d ';' -f 2`;
		#templates directory#############
		if [[ "$ltype" == "tdir" ]]; then
			tempDir=${lvalue};
			continue;
		fi
		#work directory##################
		if [[ "$ltype" == "wdir" ]]; then
			workDir=${lvalue};
			continue;
		fi
		#base directory##################
		if [[ "$ltype" == "bdir" ]]; then
			baseDir=${lvalue};
			continue;
		fi
		#auto csv log file###############
		if [[ "$ltype" == "log" ]]; then
			autoLog=${lvalue};
			continue;
		fi
		#auto name prefix################
		if [[ "$ltype" == "name" ]]; then
			calcPrefix=$lvalue;
			continue;
		fi
		#parameters######################
		if [[ "$ltype" == "par" ]]; then
			tmp_pname=`echo ${lvalue} | cut -d '=' -f 1`;
			tmp_pval=`echo ${lvalue} | cut -d '=' -f 2`;
			if [[ "${tmp_pname}" == "" || "${tmp_pval}" == "" ]]; then
				echo " error : <parName> and <parValue> must be non-empty";
				exit -1;
			fi
			if echo ${parNames[@]} | grep " ${tmp_pname} " &>/dev/null; then
				echo " error : redefinition of variable ${tmp_pname}";
				exit -1;
			fi
			parNames+=(${tmp_pname});
			parVals+=(${tmp_pval});
		fi
		#run time parameters#############
		if [[ "$ltype" == "rtp" ]]; then
			tmp_rtpname=`echo ${lvalue} | cut -d '=' -f 1`;
			tmp_rtpval=`echo ${lvalue} | cut -d '=' -f 2`;
			if [[ "${tmp_rtpname}" == "" || "${tmp_rtpval}" == "" ]]; then
				echo " error : <rtpName> and <rtpValue> must be non-empty";
				exit -1;
			fi
			if echo ${rtpNames[@]} | grep " ${tmp_rtpname} " &>/dev/null; then
				echo " error : redefinition of variable ${tmp_rtpname}";
				exit -1;
			fi
			rtpNames+=(${tmp_rtpname});
			rtpVals+=(${tmp_rtpval});
		fi
		#initial var values##############
		if [[ "$ltype" == "init" ]]; then
			tmp_varname=`echo ${lvalue} | cut -d '=' -f 1`;
			tmp_varval=`echo ${lvalue} | cut -d '=' -f 2`;
			if [[ "${tmp_varname}" == "" || "${tmp_varval}" == "" ]]; then
				echo " error : <varName> and <varValue> must be non-empty";
				exit -1;
			fi
			if echo ${valNames[@]} | grep " ${tmp_varname} " &>/dev/null; then
				echo " error : redefinition of variable ${tmp_varname}";
				exit -1;
			fi
			varNames+=(${tmp_varname});
			varVals+=(${tmp_varval});
		fi
	done
fi

#read parameters from cmd###############################################################################################
if [[ "${inp_bdir}" != "" ]]; then
	baseDir=${inp_bdir};
fi
if [[ "${inp_wdir}" != "" ]]; then
	workDir=${inp_wdir};
fi
if [[ "${inp_temp}" != "" ]]; then
	tempDir=${inp_temp};
fi
if [[ "${inp_log}" != "" ]]; then
	autoLog=${inp_log};
fi 
if [[ "${inp_name}" != "" ]]; then
	calcPrefix=${inp_name};
fi
#system parameters
num_inpar=${#inp_parnames[@]};
for((i = 0; i < ${num_inpar}; ++i)); do
	numPar=${#parNames[@]};
	isCurrParExist=false;
	for((j = 0; j < $numPar; ++j)); do
		if [[ "${parNames[$j]}" == "${inp_parnames[$i]}" ]]; then
			parVals[$j]=${inp_parvals[$i]};
			isCurrParExist=true;
			break;
		fi
	done
	if ! $isCurrParExist; then
		parNames+=(${inp_parnames[$i]});
		parVals+=(${inp_parvals[$i]});
	fi
done
#run time parameters
num_inrtp=${#inp_rtpnames[@]};
for((i = 0; i < ${num_inrtp}; ++i)); do
	numRtp=${#rtpNames[@]};
	isCurrRtpExist=false;
	for((j = 0; j < $numRtp; ++j)); do
		if [[ "${rtpNames[$j]}" == "${inp_rtpnames[$i]}" ]]; then
			rtpVals[$j]=${inp_rtpvals[$i]};
			isCurrRtpExist=true;
			break;
		fi
	done
	if ! $isCurrRtpExist; then
		rtpNames+=(${inp_rtpnames[$i]});
		rtpVals+=(${inp_rtpvals[$i]});
	fi
done
#variables initialization
num_invar=${#inp_varnames[@]};
for((i = 0; i < ${num_invar}; ++i)); do
	numVar=${#varNames[@]};
	isCurrVarExist=false;
	for((j = 0; j < $numRtp; ++j)); do
		if [[ "${varNames[$j]}" == "${inp_varnames[$i]}" ]]; then
			rtpVals[$j]=${inp_varvals[$i]};
			isCurrVarExist=true;
			break;
		fi
	done
	if ! $isCurrVarExist; then
		varNames+=(${inp_varnames[$i]});
		varVals+=(${inp_varvals[$i]});
	fi
done
#calc length of pars and rtp massives###################################################################################
numPar=${#parNames[@]};
if [[ "$numPar" == "" ]]; then numPar=0; fi
numRtp=${#rtpNames[@]};
if [[ "$numRtp" == "" ]]; then numRtp=0; fi
numVar=${#varNames[@]};
if [[ "$numVar" == "" ]]; then numVar=0; fi
#check input parameters#################################################################################################
if [[ "$baseDir" == "" && "$workDir" == "" ]]; then
	echo " error : baseDir or workDir must be specified" 1>&2;
	print_help;
	exit -1;
fi
if [[ "$tempDir" == "" ]]; then
	echo " error : tempDir must be specified" 1>&2;
	print_help;
	exit -1;
fi
if [[ "$autoLog" == "" ]]; then
	autoLog='auto.log';
fi
if [[ "$parPrefix" == "" ]]; then
	parPrefix='PAR';
fi
if [[ "$rtpPrefix" == "" ]]; then
	rtpPrefix='RTP';
fi
if [[ "$varPrefix" == "" ]]; then
	varPrefix='INIT';
fi
#processing templates###################################################################################################
auto_src_file=`ls ${tempDir}/*.auto.template 2>/dev/null`;
c_src_file=`ls ${tempDir}/*.c.template 2>/dev/null`;
cnstr_src_files=`ls ${tempDir}/c.*.* 2>/dev/null`;

if [[ "${auto_src_file}" == "" ]]; then
	echo " error : can't find file *.auto.template";
	exit -1;
fi
if [[ "${c_src_file}" == "" ]]; then
	echo " error : can't find file *.c.template";
	exit -1;
fi
if [[ "${cnstr_src_files}" == "" ]]; then
	echo " error : can't find config files c.*.*";
	exit -1;
fi
input_files="${auto_src_file} ${c_src_file} ${cnstr_src_files}";
for file in ${input_files}; 
do
	if [[ ! -f "${file}" ]]; then
		echo "error : can't find file $file";
	fi
done
#prepare Name###########################################################################################################
if [[ "$workDir" != "" && "$calcPrefix" == "" ]]; then
	calcName=`basename $workDir`;
else
	if [[ "$calcPrefix" != "" ]]; then
		calcName=`echo ${calcPrefix} | cut -d '+' -f 1`;
	else
		calcName='model';
	fi
	for((i = 0; i < $numPar; ++i)); do
		if echo ${calcPrefix} | grep "+${parNames[$i]}+" &>/dev/null; then
			calcName="${calcName}_${parNames[$i]}=${parVals[$i]}";
		fi
	done
	if [[ ! -d ${baseDir} ]]; then
		echo " error : base dir \`${baseDir}' doesn't exist";
		exit -1;
	fi
	workDir=${baseDir}/${calcName};
fi
#check dirs & make subdirs##############################################################################################
if [[ ! -d ${workDir} ]]; then
	mkdir ${workDir} || { echo " error : can't create dir ${workDir}"; exit -1; };
fi
if [[ ! -d ${workDir}/auto ]]; then
	mkdir ${workDir}/auto || { echo " error : can't create config dir ${workDir}/auto"; exit -1; };
fi
#write input info#######################################################################################################
#echo " Read parameters:";
#echo "baseDir: $baseDir";
#echo "workDir: $workDir";
#echo "tempDir: $tempDir";
#echo "temp files: ${input_files}";
#echo "auto log file: $autoLog";
#echo "parameters prefix: $parPrefix";
#echo "system parameters:";
#for((i = 0; i < $numPar; ++i)); do
#	echo "${parNames[$i]}=${parVals[$i]}";
#done
#echo "run time parameters:"
#for((i = 0; i < $numRtp; ++i)); do
#	echo "${rtpNames[$i]}=${rtpVals[$i]}";
#done
#echo "initial variables values:"
#for((i = 0; i < $numVar; ++i)); do
#	echo "${varNames[$i]}=${varVals[$i]}";
#done
#save config and prepare parameters files###############################################################################
#save config
(
	echo "bdir;${baseDir}";
	echo "wdir;${workDir}";
	echo "tdir;${tempDir}";
	echo "log;${autoLog}";
	echo "name;${calcPrefix}";
	for((i = 0; i < $numPar; ++i)); do
		echo "par;${parNames[$i]}=${parVals[$i]}";
	done
	for((i = 0; i < $numRtp; ++i)); do
		echo "rtp;${rtpNames[$i]}=${rtpVals[$i]}";
	done
	for((i = 0; i < $numVar; ++i)); do
		echo "init;${varNames[$i]}=${varVals[$i]}";
	done
) &> ${workDir}/runAuto.config;
#save parameners and inits fo templates replacements
(
	for((i = 0; i < $numPar; ++i)); do
		echo "${parPrefix}_${parNames[$i]}_${parPrefix}	${parVals[$i]}";
	done
	for((i = 0; i < $numVar; ++i)); do
		echo "${varPrefix}_${varNames[$i]}_${varPrefix}	${varVals[$i]}";
	done
) &> ${workDir}/auto/par_replace;
#save rtp for replacements
(
	for((i = 0; i < $numRtp; ++i)); do
		echo "${rtpPrefix}_${rtpNames[$i]}_${rtpPrefix}	${rtpVals[$i]}";
	done
) &> ${workDir}/auto/rtp_replace;

#prepare auto files#################################################################################
####################################################################################################

cp ${auto_src_file} ${workDir}/auto/`basename ${auto_src_file} .template`;

autoFile=${workDir}/auto/`basename ${auto_src_file} .template`;

cat ${c_src_file} | /data/Dropbox/programs/4auto/macrosub.py ${workDir}/auto/par_replace > ${workDir}/auto/`basename ${c_src_file} .template`;

for file in ${cnstr_src_files}; do 
	cat $file | /data/Dropbox/programs/4auto/macrosub.py ${workDir}/auto/rtp_replace > ${workDir}/auto/`basename $file`;
done


cd ${workDir}/auto;
pwd;
echo `pwd`/0_auto.log;
start_time=`date +%s`;
(
date;
/data/Programs/auto/07p/bin/auto ${autoFile};
) &> 0_auto.log;
end_time=`date +%s`
((dt=end_time-start_time))
echo "TIME;${dt};ok"
if [[ -f auto.log ]]; then
	cat auto.log;
else
	echo " warning : no summury log found" 1>&2;
fi

if [[ "${inp_graph}" != "" ]]; then
	/data/Dropbox/Programs/4auto/parses s.${inp_graph} ${inp_graph} all
	/data/Dropbox/Programs/scripts/gplot/gplot.py -f ${inp_graph}_part_00 2 6 -o graph -v
fi
