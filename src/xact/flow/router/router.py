


import copy
import json
import types
from typing import List, Literal, Set, Union

from xact.config.config import ConfigVar
from xact.config.gen import config
from xact.data.data import DataX
from xact.flow.tool.tool import Tool,gen_function_schema
from xact.search.vector import VectorModel
from xact.search.string import string_search
from xact.types.search import SearchMDResponse



route_datalist=List[Union[DataX,Tool,str]]

class RouteData:
    def __init__(self,embed_model=config.XACT_LLM_EMBEDDING_MODEL):
        self.embed_model = embed_model
        self.vecmd = VectorModel(embed_model=embed_model)
        self.data_embd = []
        self.data_list = []
        self.data_embd_str=[]


    def embed(self,data_list:route_datalist,):
        data_embd_str = []
        up_data_list = []
        
       
        for data in data_list:
            if isinstance(data,DataX):
                data:DataX = data
                if data.content:

                    data_embd_str.append(data.content)
                    up_data_list.append(data)

            elif isinstance(data,Tool):
                data:Tool = data
                fun_schema =  data.get_schema()
                if fun_schema:

                    data_str = json.dumps(fun_schema)
                    name = fun_schema["function"]["name"]
                    description = fun_schema["function"]["description"]
                    embd_str  = f"{name} description : {description} function : [{data_str.strip()}]"
                    
                    data_embd_str.append(embd_str)
                    up_data_list.append(data)

            elif isinstance(data,str):
                if data :

                    data_embd_str.append(data.strip())
                    up_data_list.append(data)

            elif isinstance(data,types.FunctionType):
                data:Tool = data
                fun_schema =  gen_function_schema(data)
                if fun_schema:

                    data_str = json.dumps(fun_schema)
                    name = fun_schema["function"]["name"]
                    description = fun_schema["function"]["description"]
                    embd_str  = f" {name} description : {description} function : [{data_str.strip()}]"
                    
                    data_embd_str.append(embd_str)
                    up_data_list.append(data)

        data_embd = self.vecmd.generate(data=data_embd_str,model=self.embed_model)
        self.data_embd +=data_embd
        self.data_embd_str +=data_embd_str
        self.data_list +=up_data_list

    def re_embed(self,):
        self.data_embd =[]
        self.data_embd_str =[]
        old_data_list =  copy.copy(self.data_list)
        self.data_list = []
        self.embed(data_list=old_data_list)

            


class Router:
    @staticmethod
    def route(prompt:str, route_data:RouteData,weights:set=(45,50,5))->SearchMDResponse:
        
        rout_vec = Router.route_vector(prompt=prompt,route_data=route_data)
        rout_str = Router.route_string(prompt=prompt,route_data=route_data)

        results = []
        for i,data in enumerate(route_data.data_list):
            vidx = rout_vec.idx.index(i)
            sidx = rout_str.idx.index(i)

            score = weights[0]*rout_vec.score[vidx] + weights[1]*0 + weights[2]*rout_str.score[sidx]
            results.append((i,data,score))
            

        # Sort results by score (descending)
        results.sort(key=lambda x: x[2], reverse=True)

        # Single loop to construct return dictionary
        res = SearchMDResponse()
        for i, d, sc in results:
            res.idx.append(i)
            res.data.append(d)
            res.score.append(sc / 100)

        return res
    
    @staticmethod
    def route_vector(prompt:str, route_data:RouteData)->SearchMDResponse:
        vecmd = VectorModel(embed_model=route_data.embed_model)
        return vecmd.search(query_embed=prompt,data=route_data.data_list,data_embed=route_data.data_embd)
    
    @staticmethod
    def route_string(prompt:str, route_data:RouteData)->SearchMDResponse:
        return string_search(promt=prompt,data_list=route_data.data_embd_str)
        
    @staticmethod
    def route_llm(prompt:str, route_data:RouteData):
        pass
        
    