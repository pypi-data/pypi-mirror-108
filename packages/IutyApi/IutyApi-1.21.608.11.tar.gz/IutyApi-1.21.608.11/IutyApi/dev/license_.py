from IutyLib.database.mysql import MySql
from IutyLib.database.dbbase import *
from flask import session,request,send_from_directory
from flask_restful import Resource
import datetime,os


dbg = os.path.exists("./debug")
if dbg:
    mysql = MySql('139.9.137.187','root','fastcorp','dev',8510)
else:
    mysql = MySql('localhost','root','fastcorp','license')

class mac_info(mysql.Model):
    
    
    def queryByInfo(self,appname,projectname):
        data = self.query(where=r"appname = '{}' and projectname = '{}'".format(appname,projectname))
        return data
    
    def updateInfo(self,id,cpuid,boardid,pcname):
        self.update(value=[{"cpuid":cpuid,"boardid":boardid,"pcname":pcname}],where=r"id='{}'".format(id))
        pass
    
    def deleteInfo(self,id):
        self.update(value=[{"cpuid":null,"boardid":null,"pcname":null}],where=r"id='{}'".format(id))
        pass
    
    pass

class proj_info(mysql.Model):
    
    
    def queryByInfo(self,appname,projectname):
        data = self.query(where=r"appname = '{}' and projectname = '{}'".format(appname,projectname))
        return data
    
    
    pass

    
class LicenseApi(Resource):
    def addLicense():
        rtn = {"success":False}
        
        appname = request.form.get('appname')
        if not appname:
            rtn["error"] = "appname is nesserary"
            return rtn
        
        projectname = request.form.get('projectname')
        if not projectname:
            rtn["error"] = "projectname is nesserary"
            return rtn
        
        cpuid = request.form.get('cpuid')
        if not cpuid:
            rtn["error"] = "cpuid is nesserary"
            return rtn
        
        boardid = request.form.get('boardid')
        if not boardid:
            rtn["error"] = "boardid is nesserary"
            return rtn
        
        pcname = request.form.get('pcname')
        if not pcname:
            rtn["error"] = "pcname is nesserary"
            return rtn
        db = mac_info()
        data = db.queryByInfo(appname,projectname)
        
        
        
        for d in data:
            if d["pcname"] == null:
                db.updateInfo(d["id"],cpuid,boardid,pcname)
                
                db1 = proj_info()
                rdata = db1.queryByInfo(appname,projectname)
                rtn["success"] = True
                rtn["data"] = datetime.datetime.strftime(rdata[0]["date"],'%Y-%m-%d')
                return rtn
        
        rtn["error"] = "no null data exists in license"
        return rtn
    
    def updateLicense():
        rtn = {"success":False}
        
        appname = request.form.get('appname')
        if not appname:
            rtn["error"] = "appname is nesserary"
            return rtn
        
        projectname = request.form.get('projectname')
        if not projectname:
            rtn["error"] = "projectname is nesserary"
            return rtn
        
        cpuid = request.form.get('cpuid')
        if not cpuid:
            rtn["error"] = "cpuid is nesserary"
            return rtn
        
        boardid = request.form.get('boardid')
        if not boardid:
            rtn["error"] = "boardid is nesserary"
            return rtn
        
        pcname = request.form.get('pcname')
        if not pcname:
            rtn["error"] = "pcname is nesserary"
            return rtn
        db = mac_info()
        data = db.queryByInfo(appname,projectname)
        
        
        
        for d in data:
            if (d["cpuid"] == cpuid) & (d['boardid'] == boardid):
                db.updateInfo(d["id"],cpuid,boardid,pcname)
                
                db1 = proj_info()
                rdata = db1.queryByInfo(appname,projectname)
                rtn["success"] = True
                rtn["data"] = datetime.datetime.strftime(rdata[0]["date"],'%Y-%m-%d')
                return rtn
        
        rtn["error"] = "no exists data exists in license"
        return rtn
    
    def removeLicense():
        rtn = {"success":False}
        
        appname = request.form.get('appname')
        if not appname:
            rtn["error"] = "appname is nesserary"
            return rtn
        
        projectname = request.form.get('projectname')
        if not projectname:
            rtn["error"] = "projectname is nesserary"
            return rtn
        
        cpuid = request.form.get('cpuid')
        if not cpuid:
            rtn["error"] = "cpuid is nesserary"
            return rtn
        
        boardid = request.form.get('boardid')
        if not boardid:
            rtn["error"] = "boardid is nesserary"
            return rtn
        
        
        db = mac_info()
        data = db.queryByInfo(appname,projectname)

        
        for d in data:
            if (d["cpuid"] == cpuid) & (d['boardid'] == boardid):
                db.deleteInfo(d["id"])
                
                
                rtn["success"] = True
                return rtn
        
        rtn["error"] = "no exists data exists in license"
        return rtn

    
    def post(self):
        _cmd = request.form.get('cmd')
        if _cmd == 'getApis':
            return ApiApi.getApis()
        
        if _cmd == 'getApiInfo':
            return ApiApi.getApiInfo()
        
        if _cmd == 'getNamespaces':
            return ApiApi.getNamespaces()
        
        if _cmd == 'updateApiInfo':
            return ApiApi.updateApiInfo()
        
        if _cmd == 'deleteApiInfo':
            return ApiApi.deleteApiInfo()
        
        if _cmd == 'getApiParam':
            return ApiApi.getApiParam()
        
        if _cmd == 'updateApiParam':
            return ApiApi.updateApiParam()
        
        if _cmd == 'deleteApiParam':
            return ApiApi.deleteApiParam()
        
        if _cmd == 'updateExample':
            return ApiApi.updateExample()
        
        if _cmd == 'getExample':
            return ApiApi.getExample()
        
        if _cmd == 'deleteExample':
            return ApiApi.deleteExample()
        
        if _cmd == 'updateExampleParam':
            return ApiApi.updateExampleParam()
        
        if _cmd == 'getExampleParam':
            return ApiApi.getExampleParam()
        
        if _cmd == 'testExample':
            return ApiApi.testExample()
        
        if _cmd == 'getJqCode':
            return ApiApi.getJqCode()
    pass

if __name__ == "__main__":
    pass

