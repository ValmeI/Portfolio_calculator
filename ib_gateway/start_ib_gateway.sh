#!/bin/bash

# Detect operating system
get_os() {
    uname -s
}

# Get IB Gateway path for macOS
get_macos_path() {
    local paths=(
        "$HOME/Applications/IB Gateway 10.34"
        "/Applications/IB Gateway 10.34"
        "$HOME/Applications/IB Gateway"
        "/Applications/IB Gateway"
    )
    
    for path in "${paths[@]}"; do
        if [ -d "$path" ]; then
            echo "$path"
            return 0
        fi
    done
    return 1
}

# Get IB Gateway path for Linux
get_linux_path() {
    local paths=(
        "/opt/ibgateway"
        "/usr/local/ibgateway"
        "$HOME/ibgateway"
    )
    
    for path in "${paths[@]}"; do
        if [ -d "$path" ]; then
            echo "$path"
            return 0
        fi
    done
    return 1
}

# Get installation path based on OS
get_install_path() {
    local os=$1
    local path
    
    case "$os" in
        Darwin)
            path=$(get_macos_path)
            ;;
        Linux)
            path=$(get_linux_path)
            ;;
        *)
            echo "❌ Unsupported operating system: $os (only Linux and macOS are supported)" >&2
            return 1
            ;;
    esac
    
    if [ -z "$path" ]; then
        return 1
    fi
    
    echo "$path"
    return 0
}

# Start IB Gateway on macOS
start_macos_gateway() {
    local path=$1
    local app_path="$path/IB Gateway 10.34.app"
    
    if [ ! -d "$app_path" ]; then
        echo "❌ IB Gateway app bundle not found at $app_path" >&2
        return 1
    fi
    
    open -a "$app_path" --args -nogui &
    return 0
}

# Start IB Gateway on Linux
start_linux_gateway() {
    local path=$1
    local binary_paths=(
        "$path/ibgateway"
        "$path/bin/ibgateway"
    )
    
    for binary in "${binary_paths[@]}"; do
        if [ -x "$binary" ]; then
            "$binary" -nogui &
            return 0
        fi
    done
    
    echo "❌ Could not find IB Gateway executable" >&2
    return 1
}

# Start IB Gateway based on OS
start_gateway() {
    local os=$1
    local path=$2
    
    case "$os" in
        Darwin)
            start_macos_gateway "$path"
            ;;
        Linux)
            start_linux_gateway "$path"
            ;;
    esac
    return $?
}

# Main execution
OS=$(get_os)
IB_GATEWAY_PATH=$(get_install_path "$OS")

if [ -z "$IB_GATEWAY_PATH" ]; then
    echo "❌ IB Gateway is not installed. Please run install_ib_gateway.sh first."
    exit 1
fi

echo "🚀 Starting IB Gateway..."

if ! start_gateway "$OS" "$IB_GATEWAY_PATH"; then
    exit 1
fi

# Function to check if IB Gateway is running
check_gateway_running() {
    local max_attempts=$1
    local attempt=1
    local process_name
    
    case "$OS" in
        Darwin)
            process_name="IB Gateway"
            ;;
        Linux)
            process_name="ibgateway"
            ;;
    esac
    
    while [ $attempt -le $max_attempts ]; do
        if pgrep -f "$process_name" > /dev/null; then
            echo "✅ IB Gateway is running!"
            return 0
        fi
        echo "⏳ Waiting for IB Gateway to start (attempt $attempt/$max_attempts)..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ Failed to start IB Gateway after $max_attempts attempts."
    echo "🔍 Please check:"
    echo "  1. Your IB Gateway installation is complete and valid"
    echo "  2. You have necessary permissions to run IB Gateway"
    echo "  3. There are no other instances of IB Gateway running"
    return 1
}

# Wait for IB Gateway to start (max 30 seconds)
if ! check_gateway_running 15; then
    exit 1
fi
