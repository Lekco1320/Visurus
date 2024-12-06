#!/bin/bash

function install_env_ubuntu() {
	sudo apt install python3
	sudo apt install python3-pip
	sudo apt install python3-tk
}

function install_env_centos() {
	sudo yum install python3
	sudo yum install python3-pip
	sudo yum install python3-tkinter
}

function install_env_darwin() {
	local option
	read -p "安装操作使用\`Homebrew\`包管理器，是否继续？[[是]/否] " option

	if [[ $option == "否" ]]; then
		echo "安装已终止."
		exit 1
	fi

	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	brew install python
	python3 -m ensurepip --upgrade
	brew install tcl-tk
}

function install() {
	case $OS in
	Ubuntu)
		install_env_ubuntu
		;;
	CentOS)
		install_env_centos
		;;
	Darwin)
		install_env_darwin
		;;
	esac

	python3 -m venv ./venv
	source ./venv/bin/activate
	pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
}

function run() {
	source ./venv/bin/activate
	python3 ./main.py
}

function main() {
	OS=$(uname)
	if   [[ $OS == "Linux" ]]; then
		if   grep -iq "ubuntu" /etc/os-release; then
			OS="Ubuntu"
		elif grep -iq "centos" /etc/os-release; then
			OS="CentOS"
		else
			echo "无法识别操作系统."
			exit 1
		fi
	elif [[ $OS == "Darwin" ]]; then
		OS="Darwin"
	else
		echo "无法识别操作系统."
		exit 1
	fi

	echo "操作系统：${OS}"
	echo "请选择执行的目标操作："
	echo "  I) 安装并运行"
	echo "  R) 仅运行"
	read -p "> " option

	case ${option^^} in
	I)
		install
		run
		;;
	R)
		run
		;;
	*)
		echo "非法输入."
		exit 1
		;;
	esac
}

main
