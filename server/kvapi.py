from typing import List, Dict, Any

keyvalue_Record: List[Dict[str, Dict[Any]]] = []
selected_Record: str = "None"

def readKeysfromRecord(recordName: str) -> Dict[str, Any]:
    for rec in keyvalue_Record:
        if rec.get("recordName") == recordName:
            return rec
    return {"message": f"Record '{recordName}' not found."}

def addRecord(recordName: str):
    new_record = {
        "recordName": recordName,
        "keys": {}
    }
    keyvalue_Record.append(new_record)
    return {"message": f"Record '{recordName}' added successfully."}

def delRecord(recordName: str):
    global keyvalue_Record
    keyvalue_Record = [rec for rec in keyvalue_Record if rec.get("recordName") != recordName]
    return {"message": f"Record '{recordName}' deleted successfully."}

def listRecords() -> List[str]:
    return [rec.get("recordName") for rec in keyvalue_Record]

def selectRecord(recordName: str):
    for rec in keyvalue_Record:
        if rec.get("recordName") == recordName:
            global selected_Record
            selected_Record = recordName
            return {"message": f"Record '{recordName}' selected successfully."}
    
    selected_Record = "None"
    return {"message": f"Record '{recordName}' not found."}

def listKeysfromRecord() -> List[str]:
    for rec in keyvalue_Record:
        if rec.get("recordName") == selected_Record:
            return list(rec["keys"].keys())
    return {"message": f"Record '{selected_Record}' not found."}

def addKeytoRecord(key: str, value: Any):
    for rec in keyvalue_Record:
        if rec.get("recordName") == selected_Record:
            rec["keys"][key] = value
            return {"message": f"Key '{key}' added to record '{selected_Record}' successfully."}
    return {"message": f"Record '{selected_Record}' not found."}

def delKeyfromRecord(key: str):
    for rec in keyvalue_Record:
        if rec.get("recordName") == selected_Record:
            if key in rec["keys"]:
                del rec["keys"][key]
                return {"message": f"Key '{key}' deleted from record '{selected_Record}' successfully."}
            else:
                return {"message": f"Key '{key}' not found in record '{selected_Record}'."}
    return {"message": f"Record '{selected_Record}' not found."}

def readKeyfromRecord(key: str) -> Dict[str, Any]:
    for rec in keyvalue_Record:
        if rec.get("recordName") == selected_Record:
            if key in rec["keys"]:
                return {"message": f"Key '{key}' read from record '{selected_Record}' successfully.", "value": rec["keys"][key]}
            else:
                return {"message": f"Key '{key}' not found in record '{selected_Record}'."}
    return {"message": f"Record '{selected_Record}' not found."}

def writeKeytoRecord(key: str, value: Any):
    for rec in keyvalue_Record:
        if rec.get("recordName") == selected_Record:
            rec["keys"][key] = value
            return {"message": f"Key '{key}' updated in record '{selected_Record}' successfully."}
    return {"message": f"Record '{selected_Record}' not found."}