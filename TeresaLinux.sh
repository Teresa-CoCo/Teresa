#!/bin/bash

# Check python3-full
if ! dpkg -s python3-full &> /dev/null; then
    echo "python3-full is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3-full
fi

# Activate virtual environment if exists or create a new one
activate_virtualenv() {
    # Check if .venv
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    # Activate virtual environment
    source .venv/bin/activate
}

activate_virtualenv

# Check websocket-client
if ! pip show websocket-client &> /dev/null; then
    echo "websocket-client is not installed. Installing..."
    pip install -r requirements.txt
fi

# Check whiptail
if ! command -v whiptail &> /dev/null; then
    echo "whiptail is not installed. Please install whiptail to proceed."
    exit 1
fi

execute_whiptail() {
    #!/bin/bash
    result_file="results.txt"
    touch "$result_file"
    while true; do
        # 使用whiptail显示输入框获取用户输入
        input=$(whiptail --inputbox "请输入一些内容：" 10 40 --title "Teresa Linux" 3>&1 1>&2 2>&3)

        if [ $? -eq 0 ]; then
            result=$(echo "$input" | python3 TeresaLinux.py)
            echo "$result" >> "$result_file"
            records=$(cat "$result_file" | awk '{printf "%s\\n", $0}')
            # --scrolltext选项来显示更多的回复内容
            whiptail --msgbox "$records" 15 60 --scrolltext --title "Teresa Linux"
        else
            echo "您取消了输入。"
            break
        fi
    done
}

execute_whiptail

ask_keep_records() {
    if whiptail --yesno "Do you want to keep the records?" 10 40 --title "Keep Records" ; then
        echo "Records will be kept."
    else
        echo "Records will be deleted."
        # Perform actions to delete records here
        # For demonstration, we will delete the virtual environment
        rm -rf results.txt  # Remove virtual environment directory
        echo "Records deleted."
    fi
}
ask_keep_records

echo "运行结束"
