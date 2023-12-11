from autogen_pool.groupchat import GroupChat

groupchat = GroupChat(attach="5d0e294352b75a0049ff76c3")

message = groupchat.run_flow("I am a booked user. How can I find key?")
print(message)