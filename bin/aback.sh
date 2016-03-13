#!/bin/bash

print_help(){
	cat << EOF
 usage : $0 [-r] <file move to>
         $0 [-r] <file wich move> <file move to>
EOF
}

replace=false;
dir=;
while getopts 'rd:' opt; do
	case $opt in
		r)
			replace=true;;
		d)
			dir="${OPTARG}/";;
		?)
			print_help; exit 1;;
	esac
done

((cc=OPTIND-1));
((n=$#-cc));
args=($@);

mt=;
wm=fort;
if(( n==1 )); then
	mt=${args[$cc]};
fi
if(( n==2 )); then
	wm=${args[$cc]};
	((++cc));
	mt=${args[$cc]};
fi
if((n>2 || n==0)); then
	echo " error : too many arguments";
	echo;
	print_help;
fi

for k in b s d; do
	if [[ -f ${dir}${k}.${mt} ]] && ! $replace; then
		echo " error : file \`${dir}${k}.${mt}' already exist";
		echo "   use '-r' for replace";
		exit -1;
	fi
done

if [[ "$wm" == "fort" ]]; then
	mv -v ${dir}fort.7 ${dir}b.${mt};
	mv -v ${dir}fort.8 ${dir}s.${mt};
	mv -v ${dir}fort.9 ${dir}d.${mt};
else
	for k in b s d; do
		mv -v ${dir}${k}.${wm} ${dir}${k}.${mt};
	done
fi
