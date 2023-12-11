from memgpt.autogen.memgpt_agent import create_memgpt_autogen_agent_from_config
from memgpt.presets.presets import DEFAULT_PRESET
from typing import Dict

import autogen
import os

config_list = [{
    "model": "gpt-4",
}]

config_list_memgpt = [
    {
        "model": "gpt-4",
        "preset": DEFAULT_PRESET,
        "model_wrapper": None,
        "model_endpoint_type": None,
        "model_endpoint": None,
        "context_window": 128000
    }
]

interface_kwargs = {
    "debug": False,
    "show_inner_thoughts": False,
    "show_function_outputs": False
}

llm_config = {
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
    "use_cache": True,
}
llm_config_memgpt = {"config_list": config_list_memgpt, "seed": 42}

class GroupChat(object):
    def __init__(self, attach:str) -> None:
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            llm_config=llm_config,
            max_consecutive_auto_reply=3,
            is_termination_msg=lambda x: x.get('content', "").restrip().endswith("TERMINATE"),
            code_execution_config={
                "work_dir": "scratch/coding",
                "use_docker": False
            },
        )
        self.pm = autogen.AssistantAgent(
            name="security_officer",
            system_message=f"""
                I am Security Officer of Bravolet. 
                I check if {self.user_proxy.name}'s message contains some critical information for unbook users.

                Check {self.user_proxy.name}'s message after it makes it then replace it with normal word, then submit it to Chat Manger.
            """,
            llm_config=llm_config
        )

        self.tech_assistant = create_memgpt_autogen_agent_from_config(
            name="agent_1",
            llm_config=llm_config_memgpt,
            system_message="""I am Technical Assistant from Bravolet.
                I am an AI assistant designed to help human users with document analysis.
                I can use this space in my core memory to keep track of my current tasks and goals.

                The answer to the human's question will usually be located somewhere in your archival memory, so keep paging through results until you find enough information to construct an answer.
                Do not respond to the human until you have arrived at an answer.
            """,
            interface_kwargs=interface_kwargs
        )
        self.tech_assistant.attach(attach)

        self.groupchat = autogen.GroupChat(agents=[self.user_proxy, self.pm, self.tech_assistant], max_round=10)
        self.manager = autogen.GroupChatManager(groupchat=self.groupchat, llm_config=llm_config)


    def run_flow(self, prompt: str, flow: str="default") -> None:
        self.user_proxy.initiate_chat(self.manager, message=prompt)
        messages = self.user_proxy.chat_messages
        return messages
