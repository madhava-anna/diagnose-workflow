from workers import WorkerEntrypoint, Response
from langflow import run_flow_from_json
import os
import uuid
import time

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return Response("Hello World!")
    async def fetch_(self, request):
        diag_flow_path = "src/RAG_DIAGNOSTICS_ONE.json"
        diag_tweaks = {
            "OpenAIModel-GYKyg":{    
                "api_key": {
                    "load_from_db": False,
                    "value":os.environ.get("CLOUDFLARE_API_TOKEN"),
                }
            },
            "TextInput-kWctb":{},
            "Prompt Template-lsGZe":{},
            "TextOutput-A0Umd":{},
            "Chroma-bquBo":{
                "persist_directory": {
                    "load_from_db": False,
                    "value": os.environ.get("CHROMA_PS_LOCATION"),
                },
                "collection_name": {
                    "load_from_db": False,
                    "value": os.environ.get("CHROMA_COLLECTION"),
                },
            },
            "CloudflareWorkersAIEmbeddings-njrtX":{
                "account_id": {
                    "load_from_db": False,
                    "value":os.environ.get("CLOUDFLARE_ACCOUNT_ID"),
                },
                "api_token": {
                    "load_from_db": False,
                    "value":os.environ.get("CLOUDFLARE_API_TOKEN"),
                },
                "model_name": {
                    "load_from_db": False,
                    "value":os.environ.get("CLOUDFLARE_EMBEDDING_MODEL"),
                },
            },
            
            "DataFrameOperations-tjU81":{},
            "ParserComponent-1W8ul":{},
            }


        uid = str(uuid.uuid4())
        diag_tweaks["TextInput-kWctb"]["input_value"] = request.query.get("query", "What is Langflow?")
        response = run_flow_from_json(flow=diag_flow_path, 
                                        input_value="", 
                                        tweaks=diag_tweaks, 
                                        log_file= "/tmp/langflow.log", 
                                        log_level="ERROR", session_id=uid, 
                                        fallback_to_env_vars=True)
        return Response(response[0].outputs[0].results['text'].data['text'].strip())
