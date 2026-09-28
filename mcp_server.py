import sys
import json
from client import BPlusTreeIndex

bpt = BPlusTreeIndex(order=4)

def handle_rpc(line):
    global bpt
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-b-tree-disk-storage-index-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "insert_record",
                    "description": "Insert key-value pair into B+ Tree index",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "key": {"type": "integer"},
                            "value": {"type": "string"}
                        },
                        "required": ["key", "value"]
                    }
                },
                {
                    "name": "range_query",
                    "description": "Perform range scan over B+ Tree leaves between min_key and max_key",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "min_key": {"type": "integer"},
                            "max_key": {"type": "integer"}
                        },
                        "required": ["min_key", "max_key"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "insert_record":
            bpt.insert(args.get("key"), args.get("value"))
            res = {"content": [{"type": "text", "text": json.dumps({"status": "inserted", "key": args.get("key")})}]}
        elif tool_name == "range_query":
            records = bpt.range_query(args.get("min_key"), args.get("max_key"))
            res = {"content": [{"type": "text", "text": json.dumps({"count": len(records), "records": records})}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
