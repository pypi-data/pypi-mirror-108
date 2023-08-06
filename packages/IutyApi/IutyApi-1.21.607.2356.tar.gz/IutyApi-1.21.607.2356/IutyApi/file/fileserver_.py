from flask import session,request,send_from_directory,Response
from flask_restful import Resource
import datetime,os,time,base64,json

fileserverpath = r"/dbdisk/fileserver"

def createDir():
    t = time.time()
    t = str(int(t*100))
    dirname = base64.encodebytes(t.encode('utf8'))
    dirname = str(dirname,encoding="utf-8").strip()
    
    dirpath = os.path.join(fileserverpath,dirname)
    os.mkdir(dirpath)
    
    return dirname

def getIndexTag(index,tag = None):
    obj_index = loadIndex(index)
    if not obj_index:
        raise Exception("index {} is not exists".format(index))
        
    if tag:
        if tag in obj_index:
            return obj_index[tag]
    
    obj_tag = None
    
    for idx in obj_index:
        if not obj_tag:
            obj_tag = obj_index[idx]
            continue
        if obj_tag["update"] < obj_index[idx]["update"]:
            obj_tag = obj_index[idx]
    
    if obj_tag["update"] == 0:
        raise Exception("json have no records")
    return obj_tag

def getIndexList(index,tag=None):
    
    dirname = getIndexTag(index,tag)["path"]
    
    ls = []
    rootpath = os.path.join(fileserverpath,dirname)
    for mdir,sdirs,fs in os.walk(rootpath):
        if len(fs) > 0:
            for f in fs:
                ls.append(os.path.join(mdir,f).replace(rootpath,"")[1:])
    
    data = {"dirname":dirname,"filelist":ls}
    
    return data

def setUpdate(item_index):
    item_index["update"] = int(time.time())
    pass

def loadIndex(index):
    path_index = os.path.join(fileserverpath,"index","{}.json".format(index))
    if not os.path.exists(path_index):
        return None
    f = open(path_index,"r",encoding='utf-8')
    obj_index = json.load(f)
    f.close()
    return obj_index

def saveIndex(index,obj_index):
    path_index = os.path.join(fileserverpath,"index","{}.json".format(index))
    f = open(path_index,"w+",encoding='utf-8')
    json.dump(obj_index,f,indent=4)
    f.close()
    pass

def push(index,tag = None,mode="-n"):
    if mode == "-n":
        dirname = createDir()
    obj_index = loadIndex(index)
    if not obj_index:
        obj_index = {}
    
    if not tag:
        tag = dirname
    obj_index[tag] = {"path":dirname}
    setUpdate(obj_index[tag])
    
    saveIndex(index,obj_index)
    return dirname

def setTag(index,tag,tagname):
    obj_index = loadIndex(index)
    
    if tag in obj_index:
        edittag = obj_index.pop(tag)
        obj_index[tagname] = edittag
        setUpdate(obj_index[tagname])
        saveIndex(index,obj_index)
    else:
        raise Exception("tag {} is not exists".format(tag))
    pass

def listIndex():
    data = os.listdir(os.path.join(fileserverpath,"index"))
    
    data = [d[:-5] for d in data if d[-5:] == ".json"]
    return data

def listTag(index):
    obj_index = loadIndex(index)
    if not obj_index:
        raise Exception("index is not exists")
    return list(obj_index.keys())


def append(dirname,filename,stream,start,mode):
    fullpath = os.path.join(fileserverpath,dirname,filename)
    reldirname = os.path.dirname(fullpath)
    if not os.path.exists(reldirname):
        os.makedirs(reldirname)
    if start:
        if os.path.exists(fullpath):
            if "-r" == mode:
                os.remove(fullpath)
            else:
                return
    #f = open(fullpath,"wb")
    #f.write(stream)
    #f.close()
    stream.save(fullpath)
    pass
    
def fetch(dirname,filename):
    """
    abort and instead of get method
    """
    fullpath = os.path.join(fileserverpath,dirname,filename)
    
    if not os.path.exists(fullpath):
        raise Exception("{}/{} is not exists".format(dirname,filename))
    
    f = open(fullpath,"rb")
    stream = f.read()
    
    #stream = base64
    #data = {"dirname":dirname,"filename":filename,"stream":stream}
    response = Response(stream, content_type='application/octet-stream')
    response.headers["Content-disposition"] = 'attachment; filename=%s' % filename
    return response
    

class FileServerApi(Resource):
    """
    File Server reply a file resource service
    No Usr confirm
    No Git
    """
    
    def push():
        """
        push directory to remote
        create a new directory
        """
        index = request.form.get("index")
        tag = request.form.get("tag")
        mode = request.form.get("mode")
        if not index:
            raise Exception("index is nesserary")
        
        if not mode:
            mode = "-n"
        dirname = push(index,tag,mode)
        return dirname
    
    def pull():
        """
        pull directory from remote
        """
        index = request.form.get("index")
        tag = request.form.get("tag")
        
        if not index:
            raise Exception("index is nesserary")
        
        
        return getIndexList(index,tag)
        
    
    def append():
        """
        append a file to [tag/last]
        """
        dirname = request.form.get("dirname")
        if not dirname:
            raise Exception("dirname is nesserary")
        
        filename = request.form.get("filename")
        if not filename:
            raise Exception("filename is nesserary")
        
        stream = request.files.get("file")
        
        if not stream:
            raise Exception("stream is nesserary")
        
        start = request.form.get("start")
        mode = request.form.get("mode")
        if mode != "-r":
            mode = "-s"
        
        append(dirname,filename,stream,start,mode)
        
        pass
    
    def fetch():
        """
        fetch a file from [tag/last]
        """
        dirname = request.args.get("dirname")
        if not dirname:
            raise Exception("dirname is nesserary")
        
        filename = request.args.get("filename")
        if not filename:
            raise Exception("filename is nesserary")
        
        return fetch(dirname,filename)
        pass
    
    def tag():
        """
        set tag to resource
        """
        index = request.form.get("index")
        tag = request.form.get("tag")
        tagname = request.form.get("tagname")
        
        if not index:
            raise Exception("index is nesserary")
        
        if not tag:
            raise Exception("tag is nesserary")
        
        if not tagname:
            raise Exception("tagname is nesserary")
            
        setTag(index,tag,tagname)
        pass
    
    def lists():
        """
        list resource
        """
        index = request.form.get("index")
        
        if not index:
            return listIndex()
        else:
            return listTag(index)
        pass
    
    def response_post():
        cmd = request.form.get('cmd')
        if not cmd:
            raise Exception("cmd is nesserary")
            
        if "push" == cmd:
            return FileServerApi.push()
        
        if "pull" == cmd:
            return FileServerApi.pull()
        
        if "append" == cmd:
            return FileServerApi.append()
        
        if "tag" == cmd:
            return FileServerApi.tag()
        
        if "list" == cmd:
            return FileServerApi.lists()
    
    def response_get():
        
        cmd = request.args.get('cmd')
        
        if "fetch" == cmd:
            res = FileServerApi.fetch()
            return res
            
    
    def post(self):
        rtn = {"success":False}
        
        try:
            data = FileServerApi.response_post()
            rtn["success"] = True
            if data:
                rtn["data"] = data
            
                
        except Exception as err:
            rtn["error"] = str(err)
            #raise err
        return rtn
    
    def get(self):
        res = FileServerApi.response_get()
        
        return res

if __name__ == "__main__":
    print(getNewDirName())