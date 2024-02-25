#!/bin/bash

# Define variables
DEBUG=false
TOUCHSCREEN_LOCK_DELAY=2
STYLUS_DEVICE_PATH="/dev/input/event4"  # Wacom sensor Pen
TOUCH_DEVICE_PATH="/dev/input/event5"  # Wacom sensor Finger


# Function to disable touch input
disable_touch() {
    if find_evtest_pid "$TOUCH_DEVICE_PATH"; then
        echo "Touch input already disabled."
        return
    fi
  
    # Run evtest --grab to grab the input device
    command="evtest --grab $TOUCH_DEVICE_PATH"
    if $DEBUG; then
        echo "Command: $command"
    fi
    $command > /dev/null 2>&1 &
    pid=$!
    sleep 0.5

    if [ "$pid" ]; then
        echo "Touch input has been disabled."
        echo "Evtest process ID: $pid"  # Output the PID of the started process
    else
        echo "Failed to disable touch input."
    fi
}


# Function to enable touch input
enable_touch() {
    # Find the process ID of the evtest command
    pid=$(find_evtest_pid "$TOUCH_DEVICE_PATH")
    # Kill the process
    if [ "$pid" ]; then
        if $DEBUG; then
            echo "Trying to kill process with ID $pid"
        fi
        kill "$pid"
        echo "Touch input has been enabled."
    else
        echo "Could not find a evtest process to terminate."
        echo "Probably the touchscreen is already active"
    fi
}


# Function to find the PID of the evtest process
find_evtest_pid() {
    local device_path="$1"
    for pid in $(pgrep -f "evtest --grab $device_path"); do
        if [ -d "/proc/$pid" ]; then
            echo "$pid"
            return
        fi
    done
}


# Function to check if stylus is close
stylus_is_close() {
    if [ "$(cat "$STYLUS_DEVICE_PATH")" ]; then
        echo "Stylus is close: true"
        return 0
    else
        echo "Stylus is close: false"
        return 1
    fi
}


# Function to handle stylus proximity
handle_stylus_proximity() {
    if stylus_is_close; then
        disable_touch
    else
        sleep "$TOUCHSCREEN_LOCK_DELAY"
        if ! stylus_is_close; then
            enable_touch
        fi
    fi
}


# Function to parse command line arguments
parse_args() {
    local debug=false
    local test_proximity=false

    while [ "$#" -gt 0 ]; do
        case "$1" in
            --debug)
                debug=true
                shift
                ;;
            --test-proximity)
                test_proximity=true
                shift
                ;;
            *)
                echo "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    echo "$debug"
    echo "$test_proximity"
}


# Main function
main() {
    local args
    args=$(parse_args "$@")

    while true; do
        if "$args"; then
            stylus_is_close test=true
        else
            handle_stylus_proximity
        fi
    done
}

# Call the main function with command line arguments
main "$@"

