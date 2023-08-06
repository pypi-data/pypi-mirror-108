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
        self.update(value=[{"cpuid":None,"boardid":None,"pcname":None}],where=r"id='{}'".format(id))
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
            
            if d["pcname"] == None:
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
        if _cmd == 'addLicense':
            return LicenseApi.addLicense()
        
        if _cmd == 'updateLicense':
            return LicenseApi.updateLicense()
        
        if _cmd == 'removeLicense':
            return LicenseApi.removeLicense()
        
        
    pass

if __name__ == "__main__":
    pass

