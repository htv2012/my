# Ruby and friends
GEM_HOME="$HOME/.local/share/gems"
export GEM_HOME
PATH=$(append_if_exists $PATH "$GEM_HOME/bin")
export path

