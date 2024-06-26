#!/bin/false
# to use this script just source it
getflagids() {
	[[ "$#" -lt 2 ]] \
		&& echo "Usage: $0 [service name] [team ip]" >&2 \
		&& return 1

	if [ "$3" = "-d" ];then
		set -x
	fi
	dry=0
	if [ "$3" = "-n" ];then
		dry=1
	fi
	if [ "$3" = "-dn" ] || [ "$3" = "-nd" ];then
		set -x
		dry=1
	fi
	service="$1"
	team="$2"

	# for ip and port set 'SYSTEM_ID_FLAGS_IP' and 'SYSTEM_ID_FLAGS_PORT' in DestructiveFarm's config.py
	# they will be set automatically by (our) start_sploit.py
	# set them manually (or use default values) for use not with (our) DestructiveFarm
	ip="${IDFIP:-10.10.0.1}"
	port="${IDFPORT:-8081}"

	# tput setaf 3: yellow (or cyan) (`man terminfo`)
	# tput sgr0: reset https://stackoverflow.com/a/73483287/12206923
	if [ -z "$IDFIP" ];then
		echo $(tput setaf 3)WARN: \$IDFIP not set, using default $ip$(tput sgr0) >&2
	fi
	if [ -z "$IDFPORT" ];then
		echo $(tput setaf 3)WARN: \$IDFPORT not set, using default $port$(tput sgr0) >&2
	fi

	url=http://"$ip":"$port"/flagIds\?service\="$service"\&team\="$team"
	if [ "$dry" -eq 1 ];then
		echo "$url" >&2
	else
		# json will be printed to stdout, use jq or whatever to process it
		data=$(curl $url)
		echo $data | jq --arg k "$service" --arg k2 "$team" '.[$k][$k2]' -c
	fi

	if [ "$3" = "-d" ];then
		set +x
	fi
}
