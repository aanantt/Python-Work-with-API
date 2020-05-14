# Python program to test
# internet speed

import speedtest

st = speedtest.Speedtest()

option = 3

if option == 1:

    print(st.download())

elif option == 2:

    print(st.upload())

elif option == 3:

    servernames = []

    st.get_servers(servernames)

    print(st.results.ping)

else:

    print("Please enter the correct choice !")
