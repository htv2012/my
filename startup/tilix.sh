# Fix for issue https://gnunn1.github.io/tilix-web/manual/vteconfig/

if [ $TILIX_ID ] || [ $VTE_VERSION ]; then
    . $(ls -1 /etc/profile.d/vte*.sh | sort | tail -n1)
fi

