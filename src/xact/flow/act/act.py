from __future__ import annotations

import copy
import json

from typing import Dict, List


from xact.flow.tool.tool import tool, Tool
from xact.utils.gen import gen_uuid
from xact.log.config import log_manager
from xact.router.router import RouteData, Router
from xact.llm.llm import LLM
from xact.llm.openai_client import llm_client as base_llm_client, OpenAI



log = log_manager.init(__name__)



class Action:
    _instances = {}
    route_tools = RouteData()
    llm = LLM()

    def __new__(cls, name=None, *args, **kwargs):
        if name is None and "func" in kwargs and callable(kwargs["func"]):
            name = kwargs[
                "func"
            ].__name__  # Auto-assign function name if `name` is not provided

        if name in cls._instances:
            return cls._instances[name]  # Return existing instance

        if name:
            instance = super().__new__(cls)
            cls._instances[name] = instance  # Register instance
            return instance
        else:
            raise "no name or function proviede"

    def __init__(
        self,
        func: callable = None,
        name: str = None,
        description: str = None,
        llm_client: OpenAI = base_llm_client,
        model: str = None,
    ):
        if not hasattr(self, "name"):  # Ensure __init__ only runs once per instance
            if func:
                self.func = func
                self.tool = tool(description=description, func=func)
                self.name = name or self.tool.fun_schema["function"]["name"]
                self.description = self.tool.fun_schema["function"]["description"]
                self.uid = gen_uuid()

                self.route_tools.embed(data_list=[self.tool])
                self.llm = LLM(llm_client=llm_client, model=model)

                self._instances[self.name] = self

    @classmethod
    def get_actions(cls):
        return cls._instances  # Return all registered instances

    def act(
        self,
        prompt: str = None,
        messages: List[Dict] = None,
        model: str = None,
        loop: bool = False,
        kwargs: dict = None,
    ):
        log.info(f"executing action : {self.name}")
        act_res = self.nact(
            prompt=prompt,
            messages=messages,
            model=model,
            tools=[self.tool],
            top_n=1,
            llm=self.llm,
            kwargs=kwargs,
            loop=loop,
        )
        return act_res

    @staticmethod
    def nact(
        prompt: str = None,
        messages: List[Dict] = None,
        model: str = None,
        action_list: List[Action] = None,
        func_list: List[callable] = None,
        tools: List[Tool] = None,
        route_tools: RouteData = None,
        top_n: int = 5,
        llm: LLM = None,
        loop: bool = False,
        kwargs: dict = {},
    ):
        prompt=prompt or ""
        messages = messages or [
            {
                "role": "system",
                "content": "you are given with tools based on user request choose a tool if there is no tool for the user requst say no tool your request",
            },
            {"role": "user", "content": prompt.strip()},
        ]
        prompt = prompt or messages[-1]["content"]

        tools_schema = []
        input_tools = []
        need_llm_out = True

        if action_list:
            tools = []
            for action in action_list:
                tools.append(action.tool)
        elif func_list:
            tools = []
            for func in func_list:
                tools.append(tool(func=func))

        base_tools = []
        if tools:
            if not len(tools) == 1:
                route_tools = RouteData()
                route_tools.embed(data_list=tools)
                base_tools = route_tools.data_list
            else:
                base_tools = tools

        if not (base_tools or route_tools):
            if Action.route_tools.data_list:
                route_tools = Action.route_tools
                base_tools = route_tools.data_list
            else:
                return "no actions in registery"

        if not len(base_tools) == 1:

            route_res = Router.route_vector(prompt=prompt, route_data=route_tools)

            input_tools = route_res.data[0:top_n]
            input_tools.reverse()

        else:
            function_args = base_tools[0].fun_schema["function"]["parameters"][
                "properties"
            ]
            if not function_args:
                need_llm_out = False
                try:
                    fun_res = base_tools[0].run()
                    return fun_res
                except Exception as e:
                    return str(e)
            else:

                copy_route_tools = copy.deepcopy(base_tools)
                for k, v in function_args.items():
                    if k in kwargs:
                        if (
                            k
                            in base_tools[0].fun_schema["function"]["parameters"][
                                "required"
                            ]
                        ):
                            copy_route_tools[0].fun_schema["function"]["parameters"][
                                "required"
                            ].remove(k)

                if not copy_route_tools[0].fun_schema["function"]["parameters"][
                    "required"
                ]:
                    need_llm_out = False

                else:

                    need_llm_out = True

                input_tools = copy_route_tools

        for tool_obj in input_tools:
            tools_schema.append(tool_obj.get_schema())

        tool_calls_function_name = input_tools[0].fun_schema["function"]["name"]
        toot_calls_function_args = kwargs
        if need_llm_out:

            llm = llm or Action.llm
            llm_out = llm.generate(model=model, messages=messages, tools=tools_schema)

            tool_calls = llm_out.completion.choices[0].message.tool_calls
            if not tool_calls:
                content = llm_out.completion.choices[0].message.content
                return content if content else "action is not executed"
            tool_calls_function_name = tool_calls[0].function.name
            toot_calls_function_args = json.loads(tool_calls[0].function.arguments)
            for k, v in kwargs.items():
                # if k in toot_calls_function_args:
                #     toot_calls_function_args[k] = v
                toot_calls_function_args[k] = v

        for tool_obj in input_tools:
            if tool_obj.fun_schema["function"]["name"] == tool_calls_function_name:
                try:
                    fun_res = tool_obj.run(**toot_calls_function_args)
                    return fun_res
                except Exception as e:
                    return str(e)