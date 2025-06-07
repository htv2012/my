#!/usr/bin/env tclsh
# ssh and start tmux session
package require Expect

# Get the host
if {[llength $argv] != 1} {
    puts "Command requires a host name"
    exit 1
}
set host [lindex $argv 0]

# Use iTerm tmux integration if available
set flag ""
if {[array get ::env TERM_PROGRAM] == "TERM_PROGRAM iTerm.app"} {
    set flag "-CC"
}

# ssh and start tmux session
spawn ssh $host
expect "$" {
    send "tmux ${flag} attach || tmux ${flag}\r"
}
interact

