# .bashrc

# Set the prompt to include the current directory
PS1='\u@\h:\w\$ '

# Define some aliases for convenience
alias ll='ls -alF'
alias cls='clear'

# Add your custom environment variables or commands below
# export MY_VARIABLE="Hello, World!"

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi