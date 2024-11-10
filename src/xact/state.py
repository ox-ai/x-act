import json
from datetime import datetime


from xact.db.db import db_client
# from xact.socket_instance import emit_agent
from xact.settings import config


class AgentStateModel:
    def __init__(self, project: str, state_stack: list):
        self.project = project
        self.state_stack = state_stack

    def to_dict(self):
        return {
            "project": self.project,
            "state_stack": self.state_stack
        }

    @staticmethod
    def from_dict(data):
        return AgentStateModel(
            project=data.get("project"),
            state_stack=data.get("state_stack", [])
        )


class AgentState:
    def __init__(self):
        self.client = db_client
        # self.db = self.client[config.get_database_name()]
        # Modify the database access in AgentState
        self.db = self.client.get_database(config.get_database_name())

        self.collection = self.db["agent_state"]

    def new_state(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "internal_monologue": '',
            "browser_session": {"url": None, "screenshot": None},
            "terminal_session": {"command": None, "output": None, "title": None},
            "step": 1,
            "message": None,
            "completed": False,
            "agent_is_active": True,
            "token_usage": 0,
            "timestamp": timestamp
        }

    def create_state(self, project: str):
        new_state = self.new_state()
        new_state["internal_monologue"] = "I'm starting the work..."
        agent_state = AgentStateModel(project=project, state_stack=[new_state])
        self.collection.insert_one(agent_state.to_dict())
        # emit_agent("agent-state", [new_state])

    def delete_state(self, project: str):
        self.collection.delete_many({"project": project})

    def add_to_current_state(self, project: str, state: dict):
        agent_state = self.collection.find_one({"project": project})
        if agent_state:
            state_stack = agent_state["state_stack"]
            state_stack.append(state)
            self.collection.update_one(
                {"_id": agent_state["_id"]},
                {"$set": {"state_stack": state_stack}}
            )
        else:
            agent_state = AgentStateModel(project=project, state_stack=[state])
            self.collection.insert_one(agent_state.to_dict())
        # emit_agent("agent-state", state_stack)

    def get_current_state(self, project: str):
        agent_state = self.collection.find_one({"project": project})
        return agent_state["state_stack"] if agent_state else None

    def update_latest_state(self, project: str, state: dict):
        agent_state = self.collection.find_one({"project": project})
        state_stack = None
        if agent_state:
            state_stack = agent_state["state_stack"]
            state_stack[-1] = state
            self.collection.update_one(
                {"_id": agent_state["_id"]},
                {"$set": {"state_stack": state_stack}}
            )
        else:
            agent_state = AgentStateModel(project=project, state_stack=[state])
            self.collection.insert_one(agent_state.to_dict())
        # emit_agent("agent-state", state_stack)

    def get_latest_state(self, project: str):
        agent_state = self.collection.find_one({"project": project})
        return agent_state["state_stack"][-1] if agent_state else None

    def set_agent_active(self, project: str, is_active: bool):
        agent_state = self.collection.find_one({"project": project})
        if agent_state:
            state_stack = agent_state["state_stack"]
            state_stack[-1]["agent_is_active"] = is_active
            self.collection.update_one(
                {"_id": agent_state["_id"]},
                {"$set": {"state_stack": state_stack}}
            )
        else:
            new_state = self.new_state()
            new_state["agent_is_active"] = is_active
            agent_state = AgentStateModel(project=project, state_stack=[new_state])
            self.collection.insert_one(agent_state.to_dict())
        # emit_agent("agent-state", state_stack)

    def is_agent_active(self, project: str):
        agent_state = self.collection.find_one({"project": project})
        return agent_state["state_stack"][-1]["agent_is_active"] if agent_state else None

    def set_agent_completed(self, project: str, is_completed: bool):
        agent_state = self.collection.find_one({"project": project})
        if agent_state:
            state_stack = agent_state["state_stack"]
            state_stack[-1]["internal_monologue"] = "Agent has completed the task."
            state_stack[-1]["completed"] = is_completed
            self.collection.update_one(
                {"_id": agent_state["_id"]},
                {"$set": {"state_stack": state_stack}}
            )
        else:
            new_state = self.new_state()
            new_state["completed"] = is_completed
            agent_state = AgentStateModel(project=project, state_stack=[new_state])
            self.collection.insert_one(agent_state.to_dict())
        # emit_agent("agent-state", state_stack)

    def is_agent_completed(self, project: str):
        agent_state = self.collection.find_one({"project": project})
        return agent_state["state_stack"][-1]["completed"] if agent_state else None

    def update_token_usage(self, project: str, token_usage: int):
        agent_state = self.collection.find_one({"project": project})
        if agent_state:
            state_stack = agent_state["state_stack"]
            state_stack[-1]["token_usage"] += token_usage
            self.collection.update_one(
                {"_id": agent_state["_id"]},
                {"$set": {"state_stack": state_stack}}
            )
        else:
            new_state = self.new_state()
            new_state["token_usage"] = token_usage
            agent_state = AgentStateModel(project=project, state_stack=[new_state])
            self.collection.insert_one(agent_state.to_dict())

    def get_latest_token_usage(self, project: str):
        agent_state = self.collection.find_one({"project": project})
        return agent_state["state_stack"][-1]["token_usage"] if agent_state else 0
